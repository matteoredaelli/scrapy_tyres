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

# scrapy crawl autoparti.it -a width=195 -a height=65 -a diameter=15

import scrapy
import datetime, re

def clean_text(text):
    if text is None or text == "":
        return text

    t = re.sub('[\n\t\r]', '', text)
    return re.sub('  +', ' ', t).strip()
    
class AutopartiIt(scrapy.Spider):
    name = "autoparti.it"

    def __init__(self, width="195", height="65", diameter="15", *args, **kwargs):
        super(AutopartiIt, self).__init__(*args, **kwargs)
        self.allowed_domains = ["autoparti.it"]
        self.today = datetime.date.today().strftime("%Y-%m-%d")
        #self.start_urls = ["http://www.autoparti.it/pneumatici?Width=%s&CrossSections=%s&Size=%s&Season=&page=1" % (width, height, diameter)]
        self.start_urls = ['http://www.autoparti.it/pneumatici/%d-pollici?page=1' % n for n in [10,12,13,14,15,16,17,18,19,20,21,22,23,24,40,365,390,415]]

    def parse(self, response):
        for entry in response.xpath('//div[@class="item tyre_item"]'):
            description = entry.xpath('.//a[@class="prod_link"]/text()').extract_first()
            extra = " ".join(entry.xpath('.//div[@class="nr"]/text()').extract())

            #description = entry.xpath('.//span[@class="nam_model"]/text()').extract_first()
            ean = entry.xpath('.//div[@class="nr"]/span/text()').extract_first().replace("EAN: ","")
            id  = entry.xpath('.//div[@class="nr"]/span/text()').extract()[1].replace("MPN: ","")
            picture_url = entry.xpath('.//img[@class="tires_item_image"]/@src').extract_first()
            product_url = entry.xpath('.//a[@class="prod_link"]/@href').extract_first()
            price = entry.xpath('.//div[@class="price"]/text()').extract_first()
            season = entry.xpath('.//div[contains(@class, "tires_season")]/@class').extract_first()#.replace("tires_season ","")
            params = entry.xpath('.//ul[@class="product_params"]/li//text()').extract()
            values=list(
                filter(lambda x: x!= '',
                           map(lambda x: x.replace(":","").strip(), params)
                           )
                )
            mydata = dict(zip(values[0::2], values[1::2]))
            mydata["manufacturer_number"] = id
            mydata["description"] = description
            mydata["ean"] = ean
            mydata["extra"] = extra
            mydata["picture_url"] = picture_url
            mydata["product_url"] = product_url
            mydata["price"] = price
            mydata["season"] = season
            mydata["source"] = self.name
            mydata['day'] = self.today
                        
            yield mydata

        next_page = response.xpath('//span[@class="next"]/a/@href').extract_first()
        if next_page != None:
            yield scrapy.Request(next_page, callback=self.parse)
            
            



