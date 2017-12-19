# -*- coding: utf-8 -*-

#   scrapy_web
#    Copyright (C) 2016-2017 Matteo.Redaelli@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# usage:
#   scrapy crawl rengaskontti.fi -t jsonlines -o data/a.json -a width=265 -a height=70 -a diameter=16

import scrapy
import datetime, re
import utils, tyre_utils

class RengaskonttiFi(scrapy.Spider):
    name = "rengaskontti.fi"
    
    def __init__(self, *args, **kwargs):
        super(RengaskonttiFi, self).__init__(*args, **kwargs)
        self.allowed_domains = ["rengaskontti.fi"]
        self.brands = tyre_utils.load_brands()
        self.brands = [s.replace("-", "_").replace(" ", "_") for s in self.brands]
     
        self.start_urls = ['https://www.rengaskontti.fi/auton-renkaat/%s/' % x for x in self.brands] 
        #self.start_urls =                   ['https://www.rengaskontti.fi/mp-renkaat/%s/' % x for x in self.brands]

    def parse(self, response):

        for entry in response.xpath('//table[@class="rengastaulu clear"]//tr | //table[@class="rengastaulu"]//tr'):
            mydata = {}
            brand = entry.xpath('.//span[@class="merkki nobr"]/text()').extract_first()
            product = entry.xpath('.//span[@class="malli nobr"]/text()').extract_first()
            size = entry.xpath('.//span[@class="koko nobr"]/text()').extract_first()
            description = "%s %s %s" % (brand, product, size)
            labels = entry.xpath('.//img/@alt').extract()
            if labels and len(labels) >= 7:
                label_fuel = labels[2]
                if label_fuel:
                    label_fuel = label_fuel.split(": ")
                    if len(label_fuel) == 2:
                        mydata["label_fuel"] = label_fuel[1]
                label_wet = labels[4]
                if label_wet:
                    label_wet = label_wet.split(": ")
                    if len(label_wet) == 2:
                        mydata["label_wet"] = label_wet[1]
                label_noise = labels[6]
                if label_noise:
                    label_noise = label_noise.split(": ")
                    if len(label_noise) == 2:
                        mydata["label_noise"] = label_noise[1]                        
            mydata["brand"] = brand
            mydata["product"] = product
            mydata["size"] = size
            mydata["description"] = description
            url = entry.xpath('./td/a/@href').extract_first()
            url = response.urljoin(url)
            mydata["url"] = url
            mydata["seasonality"] = entry.xpath('./td[@class="tspeksi"]/img/@alt').extract_first()
            mydata["type"] = entry.xpath('./td[@class="tspeksi"]//span[@class="malli"]/text()').extract_first()
            mydata["price"] = entry.xpath('./td[@class="thinta"]//span/text()').extract_first()

            if not bool(re.findall("/OMA.+", url)):
                yield scrapy.Request(response.urljoin(url), callback=self.parse_tyre, meta={'mydata': mydata})
            
    def parse_tyre(self, response):
        mydata = response.meta['mydata']
        s = response.xpath('//meta[@name="description"]/@content').extract_first()
        if s is None:
            ## eancode does not exist
            return None
        
        s = s.split(" , ")
        if len(s) == 2:
            mydata["description2"] = s[0]
            mydata["price2"] = s[1]

        mydata['product2'] = response.xpath('//legend//text()').extract_first()

        keys = response.xpath('//fieldset[2]//p//strong//text()').extract()
        values = response.xpath('//fieldset[2]//p//strong/../text()[1]').extract()

        if keys and values and len(keys) == len(values):
            ## removing : at the end
            ##keys = map(lambda x: x.replace(":","").lower(), keys)
            keys = [x.replace(":","").lower() for x in keys]
            details = zip(keys, values)
            mydata.update(details)
            if "eu-rengasmerkinnät" in mydata:
                del mydata["eu-rengasmerkinnät"]

        ## eu labels
        values = response.xpath('//fieldset[2]//p//strong/../text()').extract()
        if len(values) >= 3:
            labels = utils.list2dict([values[-1], values[-2], values[-3]])
            mydata.update(labels)

        #mydata["id"] = mydata["EAN"]
        yield mydata
            
