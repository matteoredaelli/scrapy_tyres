import tyre.utils
import re
import pandas as pd

##
## normalizeXXX
##
##  input: item
##  outout item

def normalize_brand(item):
    if "brand" in item:
        s=item["brand"]
        s.replace("-", " ").replace("_", " ")
        item["brand"] = s
    return item

def normalize_load_index(item):
    if "load_index" in item:
        item["load_index"] = re.sub("\(.*\)","",item["load_index"]).strip()
    return item

def normalize_label_fuel(item):
    if "label_fuel" in item:
        item["label_fuel"].upper()
    return item

def normalize_label_noise(item):
    if "label_noise" in item:
        item["label_noise"].upper().replace("DB","").strip()
    return item

def normalize_label_wet(item):
    if "label_wet" in item:
        item["label_wet"].upper()
    return item

def normalize_price(item):
    if "price" in item:
        s=item["price"]
        if bool(len(re.findall("€", s))):
            item["currency"] = "EUR"
        elif bool(len(re.findall("\$", s))):
            item["currency"] = "USD"
    
        s = s.replace("$", "").replace("€", "").replace(",", ".").strip()
        item["price"] = s
    return item

def normalize_product(item):
    if "brand" not in item:
        return item
    item = normalize_brand(item)
    
    if "product" in item:
        item["product"] = item["product"].replace(item["brand"], "").strip()
    return item

def normalize_size(item):
    if "size" in item:
        s = item["size"]
        s = s.replace("rinnovati", " ").replace(",", " ").strip()
        item["size"] = s
    return item

def normalize_seasonality(item):
    if "seasonality" in item:
        s = item["seasonality"]
        s.replace("(EURO)","").strip()
        if bool(len(re.findall("WINTER|INVERNAL|M\+S|SNOW|KITKARENGAS|NASTARENGAS", s))):
            season = "WINTER"
        elif bool(len(re.findall("SUMMER|ESTIV|KESÄRENGAS", s))):
            season = "SUMMER"
        elif bool(len(re.findall("SEASON|STAGIONI|4MEVSIM|JOKASÄÄNRENGAS", s))):
            season = "ALL_SEASONS"
        else: 
            season = s
        item["seasonality"] = season
    return item

def normalize_vehicle(item):
    if "vehicle" in item:
        s = item["vehicle"].upper()
        if bool(len(re.findall("AUTO|PKW", s))):
            result = "CAR"
        elif s == "HA":
            result = "CAR"
        elif s == "PA":
            result = "VAN"
        elif s == "4x4":
            result = "SUV"
        else:
            result = s
        item["vehicle"] = result
    return item


def mergeItems(item1, item2, append=False):
    ## TODO: append=True dow not work
    for f in item2:
        if not f in item1:
            item1[f] = item2[f]
        elif append and f not in [ "brand", "ean", "manufacturer_number", "product"]:
            ## multivalues are allowed
            v1 = item1[f]
            if not isinstance(v1, list):
                v1 = [v1]
            v2 = item2[f]
            if not isinstance(v2, list):
                v2 = [v2]
            ## only unique values
            v = list(set(v1 + v2))
            ## value will be a string if there is only 1 element in the lust
            if len(v) == 1:
                v = v[0]
            item1[f] = v
    return item1

def mergeItemIntoTyre(item, tyre={} ):
    if tyre is None:
        tyre = {}
    if item is None:
        return tyre
    if "source" in item and item["source"]:
        source = item["source"]
    else:
        source = "Unknow"
    for f in item:
        if item[f] is not None and not f.startswith("_"):
            if f not in tyre:
                tyre[f] = {}
            if f == "ean":
                tyre[f] = item[f]
            else:
                tyre[f][source] = item[f]
    return tyre

##
## extractXXX
##
##  input: string
##  output: dict, to be merged with item

def extractBrand(s):
    result = {}   
    list = s.split(" ")
    if len(list) < 3:
        if not "logging" in result:
            result["logging"] = []
        result["logging"].append("cannot extract brand from description '%s'" % s)
    else:
        brand = list[0]
        if len(brand) < 3:
            brand = "%s %s" % (brand, list[1])
        result['brand'] = brand
        result = normalize_brand(result)
    return(result)

def extractOEMark(s):
    result = {}
    l = re.findall(" ?(MOE|N0|N1|MO|AO|RO\d|NH|MCLAREN|LRO|F0\d|\*)", s, flags=re.IGNORECASE)
    if len(l) > 0:
        result["oe_mark"] = l[0]
    return result

def extractOEModels(s, filename="data/oe_manufacturers.csv"):
    oe = pd.read_csv(filename)
    result = {"oe_models": []}
    for manu in list(oe.MANUFACTURER):
        regexp = r"(%s ?.*$)" % manu
        l = re.findall(regexp, s)
        if len(s) > 0:
            result["oe_models"] = result["oe_models"] + l
    return result

def extractProduct(s):
    result = extractBrand(s)
    if "brand" in result:
        brand = result['brand']
        s = s.replace(brand,"").strip()
        regexp_product = "(.+) \d+[/ ]\d* ?Z?R\d+"
        m = re.findall(regexp_product, s)
        if len(m) > 0:
            result["product"] = m[0]
        else:
            if not "logging" in result:
                result["logging"] = []
            result["logging"].append("cannot extract product from description '%s'" % s)
    return result

def extractEan(s):
    result = {}
    l = re.findall(" ?(\d{13})", s)
    if len(l) > 0:
        result["ean"] = l[0]
    return result

def extractIndexes(s):
    ## TODO: gestire 107/110
    ## re.findall("(\d+)/?(\d+)([RSTUVZ])", s)
    result = {}
    m = re.search("\(?(\d+/?\d+)\)?([I-Z])", s)
    if m and m.groups and len(m.groups()) > 0:
        result['speed_index'] = m.groups('')[1]
        load_index  = m.groups('')[0]
        load_index_list =  load_index.split("/")
        result['load_index'] = load_index_list[0]
        if len(load_index_list) == 2:
            result['load_index2'] = load_index_list[1]
        result["index"] = m.group()
    return result

def extractSize(s):
    ## TODO: manginc C
    ##   Hankook RW06 175 R14C 99Q
    result = {}
    if s is not None:
        match = re.search("(\d+\.?\d*)/?(\d+\.?\d*)? ?(ZR|R|-)(\d+)(C)?", s)
        if match and len(match.groups()) >= 4:
            ## size
            result["width"]    = match.groups('')[0]
            result["series"]   = match.groups('')[1]
            result["radial"]   = match.groups('')[2]
            result["diameter"] = match.groups('')[3]
            if match[0] and len(match[0]) >= 5 and match[0][4].upper() == "C":
                result["vehicle"] = "LT"
            result["size"] = match.group()
        else:
            if not "logging" in result:
                result["logging"] = []
            result["logging"].append("Cannot extract the 'size' from '%s'" % s)
    return result

def extractSeasonality(s):
    result = {}
    season = normalizeSeasonality(s)
    if s != season:
        result["seasonality"] = season
    return result


def extractExtraInfos(s):
    extra = {}
    if tyre.utils.isExtraLoad(s):
        extra["xl"] = True
    if tyre.utils.isMFS(s):
        extra["mfs"] = True
    if tyre.utils.isNCS(s):
        extra["ncs"] = True
    if tyre.utils.isReinforced(s):
        extra["reinforced"] = True
    if tyre.utils.isRunflat(s):
        extra["runflat"] = True
    if tyre.utils.isSelfSeal(s):
        extra["self_seal"] = True  
    if tyre.utils.isStuddable(s):
        extra["studdable"] = True
    if tyre.utils.isStudded(s):
        extra["studded"] = True    
    return extra

def extractAll(item):
    result = {}
    
    if "description" not in item:
        return result
    
    s = item["description"]
    
    result = extractProduct(s)
    if "brand" in result:
        s = s.replace(result["brand"],"")
    if "product" in result:
        s = s.replace(result["product"],"")
    s = s.strip()
    
    result.update(extractSize(s))
    if "size" in result:
        s = s.replace(result["size"],"").strip()
    result.update(extractIndexes(s))
    if "index" in result:
        s = s.replace(result["index"],"").strip()

    result.update(extractExtraInfos(s))
    result.update(extractEan(s))
    result.update(extractOEMark(s))
    result.update(extractOEModels(s))
    return(result)


            
