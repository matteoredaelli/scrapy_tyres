
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
    
    def saveTyreByID(self, id, tyre):
        self.es.index(index=self.TYRE_DB, doc_type="tyre", id=id, body=tyre)
        
    def getTyreByID(self, id):
        tyre = self.es.get(index=self.TYRE_DB, doc_type="tyre", id=id)["_source"]
        return tyre
