from datetime import datetime
import logging
import tyre.item

import config

# by default we connect to localhost:9200


class Store(object):
    TYRE_DB = config.STORE_TYREDB
    
    def getTyre(self, t):
        return self.getTyreByID(t["ean"])
        
    def saveTyre(self, t):
        return self.saveTyreByID(t, t["ean"])
        
    def saveItem(self, item):
        t = self.getTyre(item)
        print(t)
        if t and len(t.keys()) == 0:
            logging.warning('Adding new item')
        t = tyre.item.mergeItemIntoTyre(item, t)
        return self.saveTyre(t)

    def saveTyreIByD(self, tyre, id):
        logging.error("saveTyreID to be implemented")
        
    def getTyreByID(self, id):
        logging.error("getTyreID to be implemented")


