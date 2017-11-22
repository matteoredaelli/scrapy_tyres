# -*- coding: utf-8 -*-
import scrapy
import datetime, re

class NorautoItSpider(scrapy.Spider):
    name = "norauto.it"
    allowed_domains = ["norauto.it"]
    start_urls = ['https://www.norauto.it/0/0/0/0/0/0-0-0.html?PageNumber=1']

    def parse(self, response):
        for item in response.xpath('//div[@class="ws-seg blc-all"]//div[@class="product-item-visible"]'):
            brand = item.xpath('.//div[@class="brand-logo"]//img/@alt').extract_first() 
            product = item.xpath('.//div[@class="product-info"]//a/text()').extract_first().replace('Pneumatico', "").replace(brand,"")
            url = item.xpath('.//div[@class="product-info"]//a/@href').extract_first()
            size = item.xpath('.//div[@class="product-info"]//p/text()').extract_first()
            description = "%s %s %s" % (brand, product, size)
            season = item.xpath('.//div[@class="product-weather"]/a/span/@class').extract_first()
            price = item.xpath('.//div[@class="product-price"]//span[@itemprop="price"]/text()').extract_first()
            yield {
                    "brand": brand,
                    "description": description,
                    "product": product,
                    "price": price,
                    "size": size,
                    "seasonality": season,
                    "url": url,
                    }
        next_page = response.xpath('//a[@class="next"]/@href').extract_first()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)
