import re
import pandas as pd

def clean_text(text):
    if text is None or text=="":
        return text
    #t = re.sub("[\t\n\r\"']", " ", text)
    t = re.sub('[\t\n\r"]', " ", str(text))
    return re.sub(" +", " ", t).strip()

def clean_dict(d):
    for i in d:
        d[i] = clean_text(d[i])
    return d

def extractBrand(s):
    result = {}   
    list = s.split(" ")
    if len(list) < 3:
        result["error"] = "String too short, cannot extract a brand from description '%s'" % s
    else:
        brand =list[0]
        if len(brand) < 3:
            brand = "%s %s" % (brand, list[1])
        result['brand'] = brand
    return(result)

def extractProduct(s):
    result = extractBrand(s)
    if "brand" in result:
        brand = result['brand']
        regexp_product = "%s (.+) \d+[/ ]\d* ?Z?R\d+" % brand
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
        match = re.findall("(\d+)[ /](\d*) ?Z?R?(\d+)", s)
        if len(match) > 0:
            result["width"]    = match[0][0]
            result["series"]   = match[0][1]
            result["diameter"] = match[0][2]
        else:
            result["error"] = "Cannot extract a size from '%s'" % s
    return result

def extractSeasonality(s):
    result = {}
    if bool(len(re.findall("WINTER|INVERNAL|M\+S|SNOW", s))):
        season = "WINTER"
    elif bool(len(re.findall("SUMMER|ESTIV", s))):
        season = "SUMMER"
    elif bool(len(re.findall("SEASON|STAGIONI", s))):
        season = "ALL_SEASONS"
    else: 
        season = ""
        result["error"] = "Cannot find a size from '%s'" % s
    result["seasonality"] = season
    return(result)
    
    
def isMFS(s):
    return bool(len(re.findall(" (MFS|FSL|PROTEZIONE) ?", s)))

def isExtraLoad(s):
    return bool(len(re.findall(" (XL|RF) ?", s)))

def isRunflat(s):
    return bool(len(re.findall("RUNFLAT", s)))

def isStuddable(s):
    return bool(len(re.findall("STUDDABLE|CHIODABILE", s)))

def isStudded(s):
    return bool(len(re.findall("STUDDED|CHIODATO", s)))

def extractExtraInfos(s):
    extra = {}
    if isExtraLoad(s):
        extra["xl"] = True
    if isMFS(s):
        extra["mfs"] = True
    if isRunflat(s):
        extra["runflat"] = True
    if isStuddable(s):
        extra["studdable"] = True
    if isStudded(s):
        extra["studded"] = True    
    return extra

def extractAll(s):
    result = extractProduct(s)
    result.update(extractSize(s))
    result.update(extractIndexes(s))
    result.update(extractExtraInfos(s))
    result.update(extractEan(s))
    return(result)

def json2df(infile):
    df = pd.read_json(infile, lines=True)
    return df

def extractDataFromFile(infile, outfile, fields):
    df = json2df(infile)
    df[fields].apply(lambda x: x.astype(str).str.upper()).drop_duplicates().sort_values(fields).to_csv(outfile, index=False,mode="a", header=False)


def jsonFieldsMapping(infile="db/json-fields-mapping.csv"):
    df = pd.read_csv(infile)
    fields = dict(df.values)
    return fields

def jsonRenameFields(record, fields=None):
    if not fields:
        fields = jsonFieldsMapping()
    for f in record:
        if f in fields:
            record[fields[f]] = record[f]
            del record[f]
    return(record)
    
def jsonNormalizeValues(record):
    ## uppercase
    for f in ["brand", "model", "description"]:
        if f in record:
            record[f] = record[f].upper()
    return(record)
    
