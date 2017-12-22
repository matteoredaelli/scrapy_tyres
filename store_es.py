
from elasticsearch import Elasticsearch
import logging
import store
import config

# by default we connect to localhost:9200


class ES(store.Store):

    def __init__(self, hostname=config.STORE_ES_SERVER):
        self.HOSTNAME=hostname
        self.es = Elasticsearch([self.HOSTNAME])
        self.es.indices.create(index=self.TYRE_DB, ignore=400)
        
    def create_index(self, index):
        self.es.indices.create(index=index, ignore=400)

    def saveDoc(self, type, id, doc):
        self.es.index(index=self.TYRE_DB, doc_type=type, id=id, body=doc)

    def getDoc(self, type, id):
        return self.es.get(index=self.TYRE_DB, doc_type=type, id=id)["_source"]
    
    def saveTyreByID(self, tyre, id):
        self.saveDoc("tyre", id, tyre)
        
    def getTyreByID(self, id):
        return self.getDoc("tyre", id)
    
