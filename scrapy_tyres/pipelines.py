# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
import utils
import pandas as pd



class MappingFieldsPipeline(object):
    df = pd.read_csv("data/source-fields-mapping.csv")
    fields = dict(df.values)
    def process_item(self, item, spider):
        for f in item:
            if f in self.fields:
                item[self.fields[f]] = item[f]
                del item[f]
        return item

class ScrapyTyresPipeline(object):
    def process_item(self, item, spider):
        return item

class DefaultFieldsPipeline(object):
    def process_item(self, item, spider):
        item["crawled"] = datetime.utcnow()
        item["source"] = spider.name
        return item

class UppercasePipeline(object):
    def process_item(self, item, spider):
        if "brand" in item and item['brand'] is not None:
            item['brand'] = item['brand'].upper()
        if "model" in item and item['model'] is not None:
            item['model'] = item['model'].upper()    
        if "description" in item and item['description'] is not None:
            item['description'] = item['description'].upper()            
        return item

class CleanValuesPipeline(object):
    def process_item(self, item, spider):
        return utils.clean_dict(item)

