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
#   scrapy crawl autopink-shop.it -t jsonlines -o data/a.json -a width=265 -a height=70 -a diameter=16

import scrapy
import datetime, re
import tyre.utils
import utils

class AutoPinkShopIt(scrapy.Spider):
    name = "autopink-shop.it"
    
    def __init__(self, width="195", series="65", diameter="15", details=0, *args, **kwargs):
        super(AutoPinkShopIt, self).__init__(*args, **kwargs)
        self.allowed_domains = ["autopink-shop.it"]
        self.details = int(details)
        self.width = width
        self.series = series
        self.diameter = diameter
        self.start_urls = ['https://www.autopink-shop.it/search?vehicleTypes=PKW&vehicleTypes=RACE_PKW&vehicleTypes=LLKW&vehicleTypes=VINTAGE_PKW&vehicleTypes=OFF&priceCategory=recommended&season=&width=%s&profile=%s&size=%s&suchen=1' % (width, series, diameter)]
        
    def parse(self, response):
        for entry in response.xpath('//div[@class="row serp j-sr-item"]'):

            product = entry.xpath('.//div[@itemtype="http://schema.org/Product"]/a[@itemprop="name"]/text()').extract_first()
            url = entry.xpath('.//div[@itemtype="http://schema.org/Product"]/a[@itemprop="name"]/@href').extract_first()
            # id = entry.xpath('.//a/@name').extract_first()
            id = url.split("/")[-1]
            brand = entry.xpath('.//div[@itemtype="http://schema.org/Product"]/b/text()').extract_first()
            url = response.urljoin(url)
            description = entry.xpath('.//strong[@class="result-list-prod-size"]//text()').extract_first()
            season = entry.xpath('.//div[@class="col-xs-8 col-sm-8 col-md-3 serp_B result-list-prod-size-container"]/text()[4]').extract_first()
            price = entry.xpath('.//span[@itemprop="price"]/text()').extract_first()
            #price2 = entry.xpath('.//span[@itemprop="price"]/sup/text()').extract_first()
            mydata =  {
                "brand": brand,
                "url": url,
                "product": product,
                "id": id,
                "price": price,
                "seasonality": season,
                "width": self.width,
                "series": self.series,
                "diameter": self.diameter,
                "description": "%s %s %s" % (brand, product, description)
            }
            labels = entry.xpath('.//div[@class="j-icon-tooltip product-list-tire-label-tooltip"]//span/text()').extract()
            if labels is not None and len(labels) == 3:
                mydata["label_fuel"] = labels[0]
                mydata["label_wet"] = labels[1]
                mydata["label_noise"] = labels[2]

            if self.details == 0:
                yield mydata
            else:
                yield scrapy.Request(url, callback=self.parse_tyre_autopink, meta={'mydata': mydata})
     
        next_page = response.xpath('//ul[@class="pagination"]/li/a/@href').extract()[-2]

        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_tyre_autopink(self, response):
        ean = response.xpath('//tr[@class="ean-line"]//td/span/text()').extract_first()
        mydata = response.meta['mydata']
        mydata['ean'] = ean
        labels = response.xpath('//a[@class="hover_underline"]//text()').extract()
        if len(labels) >=3:
            mydata['label_fuel'] = labels[0]
            mydata['label_wet'] = labels[1]
            mydata['label_noise'] = labels[2]
        yield mydata
        
