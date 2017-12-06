import re

##
## isXXX
##
##  input: string
##  outout Bool

def isMFS(s):
    return bool(len(re.findall(" (MFS|FSL|PROTEZIONE) ?", s)))

def isExtraLoad(s):
    return bool(len(re.findall(" XL ?", s)))

def isReinforced(s):
    return bool(len(re.findall(" RF ?", s)))

def isRunflat(s):
    return bool(len(re.findall("RUNFLAT|R-F|SSR", s)))

def isStuddable(s):
    return bool(len(re.findall("STUDDABLE|CHIODABILE", s)))

def isStudded(s):
    return bool(len(re.findall("STUDDED|CHIODATO", s)))


def normalizeCommonValues(s):
    if s is None:
        return s
    sup = s.upper()
    if sup == "Sì" or \
            sup == "SI" or \
            sup == "YES" or \
            sup == u"S\\u00ec":
        return True
    if sup == "NO":
        return False

    return s

##
## normalizeXXX
##
##  input: item
##  outout item

def normalize_brand(item):
    if "brand" in item:
        s=item["brand"]
        s.replace("-", " ")
        item["brand"] = s
    return item

def normalize_load_index(item):
    item["load_index"] = re.sub("\(.*\)","",item["load_index"]).strip()

    return item
def normalize_price(item):
    s=item["price"]
    if bool(len(re.findall("€", s))):
        item["currency"] = "EUR"
    elif bool(len(re.findall("$", s))):
        item["currency"] = "USD"
    
    s = s.replace("$", "").replace("€", "").replace(",", ".").strip()
    item["price"] = s
    return item

def normalize_product(item):
    if "brand" in item:
        item["product"] = item["product"].replace(item["brand"],"").strip()
    return item

def normalize_size(item):
    s = item["size"]
    s = s.replace("rinnovati", "").replace(",", "").strip()
    item["size"] = s
    return item

def normalize_seasonality(item):
    s = item["seasonality"]
    if bool(len(re.findall("WINTER|INVERNAL|M\+S|SNOW", s))):
        season = "WINTER"
    elif bool(len(re.findall("SUMMER|ESTIV", s))):
        season = "SUMMER"
    elif bool(len(re.findall("SEASON|STAGIONI", s))):
        season = "ALL_SEASONS"
    else: 
        season = s
    item["seasonality"] = season
    return item

def normalize_vehicle(s):
    s = item["vehicle"]
    if bool(len(re.findall("AUTO|PKW", s))):
        result = "CAR"
    else:
        result = s
    item["vehicle"] = result
    return item


##
## extractXXX
##
##  input: string
##  output: dict, to be merged with item

def extractBrand(s):
    result = {}   
    list = s.split(" ")
    if len(list) < 3:
        result["error"] = "String too short, cannot extract a brand from description '%s'" % s
    else:
        brand = list[0]
        if len(brand) < 3:
            brand = "%s %s" % (brand, list[1])
        result['brand'] = brand
        result = normalize_brand(result)
    return(result)

def extractOEMark(s):
    result = {}
    l = re.findall(" ?(MOE|N0|N1|MO|AO|RO1|NH|MCLAREN|LRO|\*)", s, flags=re.IGNORECASE)
    if len(l) > 0:
        result["oe_mark"] = l[0]
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
            result["error"] = "cannot extract product from description '%s'" % s
    return result

def extractEan(s):
    result = {}
    l = re.findall(" ?(\d{13})", s)
    if len(l) > 0:
        result["ean"] = l[0]
    return(result)

def extractIndexes(s):
    ## TODO: gestire 107/110
    ## re.findall("(\d+)/?(\d+)([RSTUVZ])", s)
    result = {}
    m = re.findall("(\d+)([RSTUVWZ])", s)
    l = len(m)
    if l > 0:
        result['load_index']  = m[l-1][0]
        result['speed_index'] = m[l-1][1]
    return(result)

def extractSize(s):
    ## TODO: fails with
    ##   Hankook RW06 175 R14C 99Q
    result = {}
    if s is not None:
        match = re.findall("(\d+)/(\d*) ?Z?R?(\d+)", s)
        if len(match) > 0:
            result["width"]    = match[0][0]
            result["series"]   = match[0][1]
            result["diameter"] = match[0][2]
        else:
            result["error"] = "Cannot extract a size from '%s'" % s
    return result

def extractSeasonality(s):
    result = {}
    season = normalizeSeasonality(s)
    if s != season:
        result["seasonality"] = season
    return result


def extractExtraInfos(s):
    extra = {}
    if isExtraLoad(s):
        extra["xl"] = True
    if isMFS(s):
        extra["mfs"] = True
    if isReinforced(s):
        extra["reinforced"] = True
    if isRunflat(s):
        extra["runflat"] = True   
    if isStuddable(s):
        extra["studdable"] = True
    if isStudded(s):
        extra["studded"] = True    
    return extra

def extractAll(item):
    s = item["description"]
    result = extractProduct(s)
    result.update(extractSize(s))
    result.update(extractIndexes(s))
    result.update(extractExtraInfos(s))
    result.update(extractEan(s))
    result.update(extractOEMark(s))
    return(result)

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

def updateMLTrainFile(item, filename="data/ml_product.train"):
    if "ean" in item and "brand" in item and "description" in item:
        s = "__label__%s_%s %s %s" % (item["brand"].replace(" ",""), item["ean"], item["ean"], item["description"])
        if "manufacturer_number" in item:
            s = "%s %s" % (s, item["manufacturer_number"])
        with open(filename, "a+") as f:
            f.write(s + "\n")
        f.closed
