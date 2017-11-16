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

def extractIndexes(string):
    result = {}
    m = re.findall("(\d+)([RSTUVZ])", s)
    if len(m) > 0:
        result['load index']  = m[0][0]
        result['speed index'] = m[0][1]
    }
    return(result)

def extractSize(string):
    ## TODO: gestire 107/110
    ## re.findall("(\d+)/?(\d+)([RSTUVZ])", s)
    result = {}
    if string is not None:
        match = re.match(".* (\d+)[ /](\d+) Z?R?(\d+).+", string)
        if match.lastindex == 3:
            result["width"]    = match.group(1)
            result["series"]   = match.group(2)
            result["diameter"] = match.group(3)
        else:
            result["error"] = "Cannot find a size from '%s'" % string
    return result

def extractSeasonality(s):
    if bool(len(re.findall("WINTER|INVERNAL|M\+S|SNOW", s))):
        return "WINTER"
    if bool(len(re.findall("SUMMER|ESTIV", s))):
        return "SUMMER"
    if bool(len(re.findall("SEASON|STAGIONI", s))):
        return "ALL_SEASON"
    return "UNKNOWN"
    
    
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

def extractDataFromFile(infile, outfile, fields):
    df = pd.read_json(infile, lines=True)

    df[fields].apply(lambda x: x.astype(str).str.upper()).drop_duplicates().sort_values(fields).to_csv(outfile, index=False,mode="a", header=False)

