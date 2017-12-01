from datetime import datetime
from elasticsearch import Elasticsearch
import logging
import tyre_utils

# by default we connect to localhost:9200


class ES(object):
    TYRE_DB = "tyre-db"

    def __init__(self, hostname):
        self.HOSTNAME=hostname
        self.es = Elasticsearch([self.HOSTNAME])
        
    def add_source(self, source):
        index = "tyre-source-%s" % source
        self.es.indices.create(index=index, ignore=400)
        
    def setup(self):
        for index in [self.TYRE_DB]:
            # create an index in elasticsearch, ignore status code 400 (index already exists)
            self.es.indices.create(index=index, ignore=400)

    def getItemID(self, item):
        if "brand" in item and "ean" in item and "manufacturer_number" in item:
            id = "%s-%s-%s" % (item["brand"], item["ean"], item["manufacturer_number"])
        else:
            id = None
            
        return id
    
    def saveTyre(self, item):
        id = self.getItemID(item)
        if id:
            self.es.index(index=self.TYRE_DB, doc_type="tyre", id=id, body=item)
        else:
            logging.warning('Cannot save tyre: missing brand or ean or manufacturer_number')
        
    def getTyre(self, item):
        id = self.getItemID(item)
        if id:
            return self.es.get(index=self.TYRE_DB, doc_type="tyre", id=id)
        else:
            logging.warning('Cannot save tyre: missing brand or ean or manufacturer_number')
            return None
        
    def updateTyre(self, item):
        item1 = self.getTyre(item)
        if item1:
            item = tyre_utils.mergeItems(item1, item)
        else:
            logging.debug('adding new tyre')
        saveTyre(self, item)
