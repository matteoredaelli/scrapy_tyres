from datetime import datetime
import logging
import tyre.utils

# by default we connect to localhost:9200


class Store(object):

    def getTyreID(self, item):
        if item and isinstance(item, dict) and "ean" in item and item["ean"]:
            id = item["ean"]
            if not isinstance(id, dict):
                ## if it is an item, we have directly the value
                return id
            ## otherwise we get the first value
            id = list(id.values())
            if len(id) > 0:
                return id[0]
        return None
    
    def saveItem(self, item):
        tyre = self.getTyre(item)
        if tyre and len(tyre.keys()) == 0:
            logging.warning('Adding new item')
        tyre = tyre.utils.mergeItemIntoTyre(item, tyre)
        return self.saveTyre(tyre)
            
    def saveTyre(self, tyre):
        id = self.getTyreID(tyre)
        if id:
            self.saveTyreByID(id, tyre)
        else:
            logging.warning('Cannot save tyre: missing ean?')
            
    def saveTyreByID(self, id, tyre):
        logging.warning("to be implemented")
    
    def getTyre(self, item):
        tyre = {}
        id = self.getTyreID(item)
        if id:
            try:
                tyre = self.getTyreByID(id=id)
            except:
                logging.debug('tyre does not exist in database')
        else:
            logging.warning('Cannot get tyre: missing brand or ean or manufacturer_number')
        return tyre
          
    def getTyreByID(self, id):
        logging.warning("to be implemented")
        return None
