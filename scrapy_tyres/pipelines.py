# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
import re
import utils
import tyre_utils
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
        ## if ID is not defined, it will be taken from url
        if not id in item:
            m = re.findall(".+/(.*)$", item["url"])
            if m and len(m) > 0:
                item["id"] = m[0].replace(".html", "").replace("pneumatico-","")
        return item

class UppercasePipeline(object):
    def process_item(self, item, spider):
        for f in ['brand', 'description', 'seasonality']:
            if f in item and item[f] is not None:
                item[f] = item[f].upper()            
        return item

class CleanValuesPipeline(object):
    def process_item(self, item, spider):
        return utils.clean_dict(item)

class NormalizeFieldsPipeline(object):
    def process_item(self, item, spider):
        if "brand" in item and item["brand"] is not None:
            item["brand"] = tyre_utils.normalizeBrand(item["brand"])
        if "seasonality" in item and item["seasonality"] is not None:
            item["seasonality"] = tyre_utils.normalizeSeasonality(item["seasonality"])
        return item

class ExtractDataFromDescriptionPipeline(object):
    def process_item(self, item, spider):
        if  "description" in item and item["description"] is not None:
            item2 = tyre_utils.extractAll(item["description"])
            #item = item2.update(item)
            for f in item2:
                if not f in item:
                    item[f] = item2[f]
        return item
