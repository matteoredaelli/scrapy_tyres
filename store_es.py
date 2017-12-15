
from elasticsearch import Elasticsearch
import logging
import store

# by default we connect to localhost:9200


class ES(store.Store):
    TYRE_DB = "tyre-db"

    def __init__(self, hostname):
        self.HOSTNAME=hostname
        self.es = Elasticsearch([self.HOSTNAME])
        self.es.indices.create(index=self.TYRE_DB, ignore=400)
        
    def add_source(self, source):
        index = "tyre-source-%s" % source
        self.es.indices.create(index=index, ignore=400)
    
    def saveTyreByID(self, id, item):
        self.es.index(index=self.TYRE_DB, doc_type="tyre", id=id, body=item)
        
    def getTyreByID(self, id):
        item = self.es.get(index=self.TYRE_DB, doc_type="tyre", id=id)["_source"]
        return item
