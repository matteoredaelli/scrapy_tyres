# -*- coding: utf-8 -*-
import scrapy
import datetime, re

class EuromasterPneumaticiItSpider(scrapy.Spider):
    name = "euromaster-pneumatici.it"
    allowed_domains = ["euromaster-pneumatici.it"]
    start_urls = [
            'https://www.euromaster-pneumatici.it/pneumatico'
            ]
    
    def parse(self, response):
        for url in response.xpath('//div[@class="marque"]/a/@href').extract():
            yield scrapy.Request(response.urljoin(url), callback=self.parse_brand)

    def parse_brand(self, response):
        # response.xpath('//div[@class="marque"]/a/@href').extract()
        for url in response.xpath('//ul[@class="listProfileDimension"]/li/a/@href').extract():
            yield scrapy.Request(response.urljoin(url), callback=self.parse_tyres)

    def parse_tyres(self, response):
        for item in response.xpath('//div[@data-idproduct="1"]'):
            
            brand = item.xpath('.//img[@class="produit-visu-manuf"]/@alt').extract_first()
            if not brand:
                continue
            brand = brand.strip()
            product = item.xpath('.//div[@class="produit-desc"]/strong/text()').extract_first().strip()
            
            season = item.xpath('.//div[@class="produit-desc"]/strong/img/@alt').extract_first().replace("Pneumatico ", "")
            match = re.match("^(.+) (.+)$", season)
            if not match:
                continue
            veycle = match.groups()[0]
            season = match.groups()[1]

            url = item.xpath('./a/@href').extract_first()
            description = " ".join(item.xpath('.//span[@class="produit-desc-ref"]//text()').extract())
            id = item.xpath('.//div[@class="produit-visu"]/img/@id').extract_first()
            match = re.match("^.+-(.+)$", id)
            if match:
                id = match.groups()[0]
            else:
                id=""

            price = item.xpath('.//div[@class="produit-prix "]/strong/text()').extract_first()
            
            yield {
                    "brand": brand,
                    "description": utils.clean_text(description),
                    "id": id,
                    "price": price,
                    "product": product,
                    "season": season,
                    "url": response.urljoin(url),
                    "type": veycle
                    }
