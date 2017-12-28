import json
import logging
import store
import os


class FS(store.Store):
    def __init__(self):
        import os
        os.makedirs(self.TYRE_DB, exist_ok=True)

    def getFilenameFromID(self, id):
        filename = "data/" + self.TYRE_DB + "/" + id
        return filename
    
    def saveTyreByID(self, id, item):
        filename = self.getFilenameFromID(id)
        with open(filename, 'w') as f:
            json.dump(item, f, ensure_ascii=False)           
        
    def getTyreByID(self, id):
        filename = self.getFilenameFromID(id)
        item = json.load(filename)
        return item
