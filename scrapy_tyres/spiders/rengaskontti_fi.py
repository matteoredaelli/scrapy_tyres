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
import utils

class RengaskonttiFi(scrapy.Spider):
    name = "rengaskontti.fi"
    
    def __init__(self, ean, *args, **kwargs):
        super(RengaskonttiFi, self).__init__(*args, **kwargs)
        self.allowed_domains = ["rengaskontti.fi"]
        self.ean = ean
        self.start_urls = ['https://www.rengaskontti.fi/auton-renkaat/%s' % ean]
        
    def parse(self, response):
        mydata = {"url": response.url}
        s = response.xpath('//meta[@name="description"]/@content').extract_first()
        if not s:
            ## eancode does not exist
            return None
        
        s = s.split(" , ")
        if len(s) == 2:
            mydata["description"] = s[0]
            mydata["price"] = s[1]

        mydata['product'] = response.xpath('//legend//text()').extract_first()

        keys = response.xpath('//fieldset[2]//p//strong//text()').extract()
        values = response.xpath('//fieldset[2]//p//strong/../text()[1]').extract()

        if keys and values and len(keys) == len(values):
            ## removing : at the end
            ##keys = map(lambda x: x.replace(":","").lower(), keys)
            keys = [x.replace(":","").lower() for x in keys]
            details = zip(keys, values)
            mydata.update(details)
            del mydata["eu-rengasmerkinnät"]

        ## eu labels
        values = response.xpath('//fieldset[2]//p//strong/../text()').extract()
        if len(values) >= 3:
            labels = utils.list2dict([values[-1], values[-2], values[-3]])
            mydata.update(labels)
        yield mydata
            
