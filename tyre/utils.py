import re
import pandas as pd
import logging
##
## isXXX
##
##  input: string
##  outout Bool

def isMFS(s):
    return bool(len(re.findall(" (MFS|FSL|PROTEZIONE) ?", s)))

def isExtraLoad(s):
    return bool(len(re.findall(" XL ?", s)))

def isNCS(s):
    return bool(len(re.findall(" SIL|ACO|ACOUSTIC|NST|SOUND|SILENT", s)))

def isReinforced(s):
    return bool(len(re.findall(" RF ?", s)))

def isRunflat(s):
    return bool(len(re.findall(" DSST|EMT|HRFS|MOExtended|PAX|RUNFLAT|R-F|RFT|ROF|SSR|(RUN FLAT)|TRF|ZRP|ZP|ZPS", s)))

def isSelfSeal(s):
    return bool(len(re.findall(" SEAL|CS", s)))

def isStuddable(s):
    return bool(len(re.findall(" STUDDABLE|CHIODABILE", s)))

def isStudded(s):
    return bool(len(re.findall(" STUDDED|CHIODATO|NASTARENGAS|SPIKE", s)))


def normalizeCommonValues(s):
    if s is None:
        return s
    sup = s.upper()
    if sup == "Sì" or \
            sup == "SI" or \
            sup == "YES":
        return True
    if sup == "NO":
        return False

    return s


def updateMLTrainFile(item, filename="data/ml_product.train"):
    if "ean" in item and "brand" in item and "description" in item:
        s = "__label__%s_%s %s %s" % (item["brand"].replace(" ",""), item["ean"], item["ean"], item["description"])
        if "manufacturer_number" in item:
            s = "%s %s" % (s, item["manufacturer_number"])
        with open(filename, "a+") as f:
            f.write(s + "\n")
        f.closed



def load_brands(filename="data/brands.csv"):
   return utils.load_csv_to_set(filename)

def load_sizes(filename="data/sizes.csv"):
   return utils.load_csv_to_set(filename)

def load_products(filename="data/products.csv"):
   return utils.load_csv_to_set(filename)

def build_root(item):
    root = None
    if "width" in item and "series" in item and "diameter" in item and "radial" in item:
        root = "%s/%s %s%s" % (item["width"], item["series"], item["radial"], item["diameter"])
    return root
