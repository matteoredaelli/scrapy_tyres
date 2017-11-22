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
#   scrapy crawl reifentiefpreis.de -t jsonlines -o data/a.json -a width=265 -a height=70 -a diameter=16

import scrapy
import re

class ReifentiefpreisDe(scrapy.Spider):
    name = "reifentiefpreis.de"
    
    def __init__(self, *args, **kwargs):
        super(ReifentiefpreisDe, self).__init__(*args, **kwargs)
        self.allowed_domains = ["reifentiefpreis.de"]
        self.start_urls = ['https://www.reifentiefpreis.de']
        
    def parse(self, response):
        for url in response.xpath('//a[@class="MarkenLink"]/@href').extract():
            yield scrapy.Request(response.urljoin(url), callback=self.parse_brand)

    def parse_brand(self, response):
        for url in response.xpath('//div[@class="BoxICnt"]/a/@href').extract():
            yield scrapy.Request(response.urljoin(url), callback=self.parse_tyres)
            
    def parse_tyres(self, response):
        for url in response.xpath('//div[@class="TyreImage"]/a/@href').extract():
            yield scrapy.Request(response.urljoin(url), callback=self.parse_tyre)
            
    def parse_tyre(self, response):
        labels = response.xpath('//i[@class="icons-list biglogoicon-RLBG"]/text()').extract()
        values = response.xpath('//div[@class="grid2colh"]/div//text()').extract()
        mydata = dict(zip(values[0::2], values[1::2]))
        result = {
            'brand': mydata['Marke'],
            'vehicle': mydata['Rubrik'].split("-")[0],
            'size': mydata['Größe'],
            'product': mydata['Profil'],
            'manufacturer_number': mydata['ArtNr.'],
            'ean': mydata['EAN'],
            'url': response.url,
            'label_fuel': labels[0],
            'label_wet': labels[1],
            'label_noise': labels[2],
            'index': mydata['Index']
            }
        if 'Zusatz' in mydata:
            result['extra'] = mydata['Zusatz']
        else:
            result['extra'] = ""
        description = "%s %s %s %s %s" % (mydata['Marke'], mydata['Profil'], mydata['Größe'], mydata['Index'], result['extra'])
        result['description'] = description.strip()

        yield result
            
