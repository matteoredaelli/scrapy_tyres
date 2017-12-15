from datetime import datetime
import logging
import tyre_utils

# by default we connect to localhost:9200


class Store(object):

    def getItemID(self, item):
        if item["ean"]:
            id = item["ean"]
        else:
            id = None
            
        return id
    
    def saveTyre(self, item):
        id = self.getItemID(item)
        if id:
            self.saveTyreByID(id, item)
        else:
            logging.warning('Cannot save tyre: missing brand or ean or manufacturer_number')
            
    def saveTyreByID(self, id, item):
        logging.warning("to be implemented")
    
    def getTyre(self, item):
        id = self.getItemID(item)
        item = None
        if id:
            try:
                item = self.getTyreByID(id=id)
            except:
                logging.debug('item does not exist in database')
        else:
            logging.warning('Cannot get tyre: missing brand or ean or manufacturer_number')
        return item
          
    def getTyreByID(self, id):
        logging.warning("to be implemented")
        return None
    
    def updateTyre(self, item):
        item1 = self.getTyre(item)
        if item1:
            item = tyre_utils.mergeItems(item, item1)
        else:
            logging.debug('adding new tyre: %s' % str(item))
            
        return self.saveTyre(item)
