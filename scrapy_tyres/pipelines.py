# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import re
import utils
import tyre_utils
#import pandas as pd
import csv

class StoreFieldsPipeline(object):
    def __init__(self):
        self.filenames = {
            'brand': "data/brands.csv",
            'product': "data/products.csv",
            'size': "data/sizes.csv"
            }
        self.data = {}
        
    def open_spider(self, spider):
        for f in self.filenames:
            with open(self.filenames[f], "r") as fd:
                lines = fd.read().splitlines()
                self.data[f] = set(lines)
            fd.closed

    def process_item(self, item, spider):
        for f in self.filenames:
            if f in item and item[f] not in self.data[f]:
                self.data[f].add(item[f])
                with open(self.filenames[f], "a+") as myfile:
                    myfile.write(item[f] + "\n")
                myfile.closed
        return item

    ##def close_spider(self, spider):
        ##for f in self.filenames:
        ##    with open(self.filenames[f], "w") as output:
        ##        output.write(str(list(self.data[f])))
        ##    output.closed

class MappingFieldsPipeline(object):
    def __init__(self):
        ## uf8 keys are converted .. not good!
        ## df = pd.read_csv("data/source-fields-mapping.csv")
        ## self.fields = dict(df.values)
        with open("data/source-fields-mapping.csv") as f:
            self.fields = dict(filter(None, csv.reader(f)))


    def process_item(self, item, spider):
        item_new = item
        for f in list(item.keys()):
            if f in self.fields:
                item_new[self.fields[f]] = item[f]
                item_new.pop(f)
        return item_new

class ScrapyTyresPipeline(object):
    def process_item(self, item, spider):
        return item

class DefaultFieldsPipeline(object):
    def process_item(self, item, spider):
        if "crawled" not in item:
            item["crawled"] = datetime.datetime.utcnow()
        if "source" not in item:
            item["source"] = spider.name
        ## currency could be understood ffrom the internet domain (.it, .de, ..) or $ in price values
        item["currency"] = "EUR"
        
        ## if ID is not defined, it will be taken from url
        if "id" not in item:
            m = re.findall(".+/(.+)$", item["url"])
            if m and len(m) > 0:
                item["id"] = m[0].replace(".html", "").replace("pneumatico-","").replace("/","")
        return item

class UppercasePipeline(object):
    def process_item(self, item, spider):
        for f in ['brand', 'description', 'label_fuel', 'label_wet', 'product', 'seasonality', "vehicle"]:
            if f in item and item[f] is not None:
                item[f] = item[f].upper()            
        return item

class CleanValuesPipeline(object):
    def process_item(self, item, spider):
        return utils.clean_dict(item)

class NormalizeCommonValuesPipeline(object):
    def process_item(self, item, spider):
        for f in item:
            item[f] = tyre_utils.normalizeCommonValues(item[f])
        return item
    
class NormalizeFieldsPipeline(object):
    def process_item(self, item, spider):
        if item:
            keys = item.keys()
            # brand must be normalized before product
            keys = list(keys).sort()
            for f in item.keys():
                if item[f]:
                    f_new = f.lower().replace(":","").strip()
                    if f != f_new:
                        item[f_new]=item[f]
                        del item[f]
                    f = f_new
                    function = "normalize_%s" % f
                    if hasattr(tyre_utils, function) and item[f] is not None:
                        function = "tyre_utils.%s(item)" % function
                        item = eval(function)
        return item

class ExtractDataFromDescriptionPipeline(object):
    def process_item(self, item, spider):
        if  "description" in item and item["description"] is not None:
            item2 = tyre_utils.extractAll(item["description"])
            item = tyre_utils.mergeItems(item2)
        return item

class PricesWriterPipeline(object):
    def open_spider(self, spider):
        self.file = open('data/prices.csv', 'a+')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if "price" in item and "id" in item:
            line = "%s,%s,%s,%s\n" % (item["crawled"].strftime("%Y%m%d"),item["source"], item["id"], item["price"])
            self.file.write(line)
        return item
