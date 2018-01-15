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

## field
    def saveField(self, field, id, record = None):
        if record is None:
            record = {"name": id}
        self.saveDoc("!" + field, id, record)

    def getField(self, field, id):
        return self.getDoc("!" + field, id)

    def saveFieldIfNew(self, field, id, record = None):
        b = self.getField(field, id)
        if b is None or b.keys() == []:
            self.saveField(field, id, record)
