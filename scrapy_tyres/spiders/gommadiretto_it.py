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
#   scrapy crawl gommadiretto.it -t jsonlines -o data/a.json -a width=265 -a height=70 -a diameter=16

import scrapy
import datetime, re

sizes = [
     ["155","65","13"],
## ["155","65","13"],
## ["155","65","14"],
## ["155","70","13"],
## ["155","80","13"],
## ["165","60","14"],
## ["165","65","13"],
## ["165","65","14"],
## ["165","70","13"],
## ["165","70","14"],
## ["165","80","13"],
## ["165","80","14"],
## ["165","80","15"],
## ["175","50","14"],
## ["175","55","15"],
## ["175","60","13"],
## ["175","60","14"],
## ["175","60","15"],
## ["175","65","13"],
## ["175","65","14"],
## ["175","65","15"],
## ["175","70","13"],
## ["175","70","14"],
## ["175","80","14"],
## ["185","50","14"],
## ["185","50","16"],
## ["185","55","14"],
## ["185","55","15"],
## ["185","60","13"],
## ["185","60","14"],
## ["185","60","15"],
## ["185","65","13"],
## ["185","65","14"],
## ["185","65","15"],
## ["185","70","13"],
## ["185","70","14"],
## ["185","70","15"],
## ["185","75","14"],
## ["195","40","16"],
## ["195","40","17"],
## ["195","45","14"],
## ["195","45","15"],
## ["195","45","16"],
## ["195","50","15"],
## ["195","50","16"],
## ["195","55","13"],
## ["195","55","15"],
## ["195","55","16"],
## ["195","60","14"],
## ["195","60","15"],
## ["195","60","16"],
## ["195","65","14"],
## ["195","65","15"],
## ["195","65","16"],
## ["195","70","14"],
## ["195","70","15"],
## ["195","80","15"],
## ["205","40","16"],
## ["205","40","17"],
## ["205","45","16"],
## ["205","45","17"],
## ["205","50","15"],
## ["205","50","16"],
## ["205","50","17"],
## ["205","55","15"],
## ["205","55","16"],
## ["205","55","17"],
## ["205","60","13"],
## ["205","60","14"],
## ["205","60","15"],
## ["205","60","16"],
## ["205","65","15"],
## ["205","65","16"],
## ["205","70","14"],
## ["205","70","15"],
## ["215","35","17"],
## ["215","35","18"],
## ["215","35","19"],
## ["215","40","16"],
## ["215","40","17"],
## ["215","40","18"],
## ["215","45","16"],
## ["215","45","17"],
## ["215","45","18"],
## ["215","50","15"],
## ["215","50","16"],
## ["215","50","17"],
## ["215","55","16"],
## ["215","55","17"],
## ["215","55","18"],
## ["215","60","16"],
## ["215","60","17"],
## ["215","65","16"],
## ["215","70","15"],
## ["225","35","17"],
## ["225","35","18"],
## ["225","35","19"],
## ["225","40","14"],
## ["225","40","16"],
## ["225","40","17"],
## ["225","40","18"],
## ["225","40","19"],
## ["225","45","16"],
## ["225","45","17"],
## ["225","45","17"],
## ["225","45","18"],
## ["225","50","15"],
## ["225","50","16"],
## ["225","50","17"],
## ["225","50","18"],
## ["225","55","16"],
## ["225","55","17"],
## ["225","60","15"],
## ["225","60","16"],
## ["225","60","17"],
## ["225","60","18"],
## ["225","65","15"],
## ["225","65","16"],
## ["225","70","15"],
## ["225","70","16"],
## ["225","75","15"],
## ["235","35","18"],
## ["235","35","19"],
## ["235","40","17"],
## ["235","40","18"],
## ["235","40","19"],
## ["235","45","17"],
## ["235","45","18"],
## ["235","45","19"],
## ["235","50","17"],
## ["235","50","18"],
## ["235","55","17"],
## ["235","55","18"],
## ["235","60","15"],
## ["235","60","16"],
## ["235","60","18"],
## ["235","65","16"],
## ["235","70","15"],
## ["235","70","16"],
## ["245","35","19"],
## ["245","40","17"],
## ["245","40","18"],
## ["245","40","19"],
## ["245","45","16"],
## ["245","45","17"],
## ["245","70","16"],
# ["255","30","19"],
# ["255","35","18"],
# ["255","35","19"],
# ["255","40","17"],
# ["255","40","18"],
# ["255","40","19"],
# ["255","45","18"],
# ["255","50","19"],
# ["255","55","18"],
# ["255","60","15"],
# ["255","60","17"],
# ["255","60","18"],
# ["255","65","16"],
# ["255","65","17"],
# ["255","70","16"],
# ["265","70","15"],
#["265","70","16"]
    ]
    
class GommadirettoIt(scrapy.Spider):
    name = "gommadiretto.it"
    
    def __init__(self, width="195", height="65", diameter="15", details=0, *args, **kwargs):
        super(GommadirettoIt, self).__init__(*args, **kwargs)
        self.allowed_domains = ["gommadiretto.it"]
        self.details = int(details)
        self.start_urls = ['http://www.gommadiretto.it/cgi-bin/rshop.pl?s_p=&rsmFahrzeugart=PKW&s_p_=Tutti&dsco=130&tyre_for=&search_tool=&ist_hybris_orig=&with_bootstrap_flag=1&suchen=--Mostrare+tutti+gli+pneumatici--&m_s=3&x_tyre_for=&cart_id=88618236.130.22966&sowigan=&Breite=%s&Quer=%s&Felge=%s&Speed=&Load=&Marke=&kategorie=&filter_preis_von=&filter_preis_bis=&homologation=&Ang_pro_Seite=50' % (width, height, diameter) for [width, height, diameter] in sizes]
        
    def parse(self, response):
        for entry in response.xpath('//div[@class="artikelklotz ajax_artikelklotz ajax_suchergebnisliste_artikelklotz"]'):
            id = entry.xpath('.//a/@name').extract_first()
            brand = entry.xpath('.//div[@class="formcaddyfab"]//b/text()').extract_first()
            price1 = entry.xpath('.//div[@class="price"]//b/text()').extract_first()
            price2 = entry.xpath('.//div[@class="price"]//small/text()').extract_first()
            product = entry.xpath('.//div[@class="formcaddyfab"]//i/b/text()').extract_first()
            size = " ".join(entry.xpath('.//div[@class="t_size"]//b/text()').extract())
            ##description = " ".join(entry.xpath('.//div[@class="t_size"]//a/text()').extract())
            description = " ".join(entry.xpath('.//div[@class="t_size"]//text()').extract())
            season = entry.xpath('.//div[@class="divformcaddy"]/span/text()').extract_first()
            ##url = "http://www.gommadiretto.it/cgi-bin/rshop.pl?details=Ordern&typ=" + id
            url = "https://www.gommadiretto.it/rshop/Pneumatici/%s/%s/%s/%s" % (brand, product, size, id)
            url = "https://www.autopink-shop.it/pneumatici/%s/%s/%s/%s" % (brand, product, size.replace("/","-"), id)
            url = url.replace(" ", "-").lower()
            mydata =  {
                "brand": brand,
                "url": url,
                "product": product,
                "id": id,
                "price": price1 + price2,
                "seasonality": season,
                "description": "%s %s %s" % (brand, product, description),
                "size": size
            }
            if self.details == 0:
                yield mydata
            else:
                yield scrapy.Request(url, callback=self.parse_tyre_autopink, meta={'mydata': mydata})
     
        next_page = response.xpath('//a[@id="ajax_suchergebnisliste_goto_next"]/@href').extract_first()
        if next_page is not None:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

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
        
    def parse_tyre(self, response):
        ean = response.xpath('//div[@id="pdp_tb_info_ean"]//div[@class="pdp_tabC"]/text()').extract_first()
        description2 = response.xpath('//div[@class="container mainback"]//h1/text()').extract_first()
        mydata = response.meta['mydata']
        picture_url = response.xpath('//img[@id="zoom-reifenbild"]/@src').extract_first()
        mydata['ean'] = ean
        #mydata['description2'] = description
        mydata['picture_url'] = response.urljoin(picture_url)
        labels = response.xpath('//a[@class="hover_underline"]//text()').extract()
        mydata['description2'] = mydata['description']
        mydata['description'] = description2
        if len(labels) >=3:
            mydata['label_fuel'] = labels[0]
            mydata['label_wet'] = labels[1]
            mydata['label_noise'] = labels[2]
        yield mydata
            
