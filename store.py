from datetime import datetime
import logging
from tyre import item as tyre_item

import config


class Store(object):
    TYRE_DB = config.STORE_TYREDB

    def getTyre(self, t):
        return self.getTyreByID(t["ean"])

    def saveTyre(self, t):
        return self.saveTyreByID(t["ean"], t)

    def saveItem(self, item):
        t = self.getTyre(item)
        print(t)
        print(item)
        if t is None or len(t.keys()) == 0:
            logging.warning('Adding new item')

        t = tyre_item.mergeItemIntoTyre(item, t)
        print(t)
        return self.saveTyre(t)

    def saveTyreByID(self, id, tyre):
        self.saveDoc("tyre", id, tyre)

    def getTyreByID(self, id):
        return self.getDoc("tyre", id)

## brands
    def saveBrand(self, id, brand = None):
        if brand is None:
            brand = {"id": id, "name": id}
        self.saveDoc("brand", id, brand)

    def getBrand(self, id):
        return self.getDoc("brand", id)

    def saveBrandIfNew(self, id, brand = None):
        b = self.getBrand(id)
        if b is None or b.keys() == []:
            self.saveBrand(id, brand)
