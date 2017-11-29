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

import scrapy
import datetime, re

class MikonaSK(scrapy.Spider):
    name = "mikona.sk"
    allowed_domains = ["mikona.sk"]
    start_urls = ['https://www.mikona.sk/e-shop/pneumatiky/1']
    
    def parse(self, response):
        for entry in response.xpath('//li[@itemtype="https://schema.org/Offer"]'):
            brand = entry.xpath('.//div[@class="box-list__producer-image"]/img/@alt').extract_first()
            product = entry.xpath('.//h2/a/text()').extract_first()
            description = entry.xpath('.//h2/a/@title').extract_first()
            price = entry.xpath('//span[@class="cenasdph"]/text()').extract_first()
            url = entry.xpath('.//h2/a/@href').extract_first()
            season = entry.xpath('.//div[@class="box-list__param-image"]/img/@title').extract_first()
            size = entry.xpath('.//h2/a/span/text()').extract_first()
            if size and season:
                size = size.replace(season, "")
            mydata = {"description": description,
                          "season": season,
                          "price": price,
                          "product": product,
                          "brand": brand,
                          "size": size,
                          "url": url,
                          }
            #yield mydata
            yield scrapy.Request(url, callback=self.parse_tyre, meta={'mydata': mydata})

        next_page = response.xpath('//a[@class="paging__arrow paging__arrow--right"]/@href').extract_first()
        yield scrapy.Request(next_page, callback=self.parse)

        
    def parse_tyre(self, response):
        brand = response.xpath('//div[@class="producer__title mt25"]//strong/text()').extract_first()
        season = response.xpath('.//dd[4]/a/@title').extract_first()
        id = response.xpath('.//dd[5]/text()').extract_first()
        mydata = response.meta['mydata']
        picture_url = response.xpath('.//div[@class="image"]/a/@href').extract_first()
        runflat = response.xpath('.//div[@class="in params-tab"]//dl[5]/dd/text()').extract_first()
        type = response.xpath('.//div[@class="in params-tab"]//dl[8]/dd/text()').extract_first()
        name = response.xpath('.//div[@class="in params-tab"]//dl[9]/dd/text()').extract_first()
        notes = response.xpath('.//div[@class="in params-tab"]//dl[10]/dd/text()').extract_first()
        #mydata['brand'] = brand
        #mydata['season'] = season
        mydata['manufacturer_number'] = id
        #mydata['name'] = name
        mydata['extra'] = notes
        #mydata['picture_url'] = picture_url
        #mydata['runflat'] = runflat
        #mydata['type'] = type
        yield mydata
            
            
