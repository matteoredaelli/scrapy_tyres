import csv
import re
import pandas as pd

def clean_text(text):
    if text is None or text=="":
        return text
    #t = re.sub("[\t\n\r\"']", " ", text)

    t = re.sub('[\t\n\r"]', " ", str(text)).replace(u'\xa0', u' ')
    return re.sub(" +", u" ", t).strip()

def clean_dict(d):
    for i in list(d.keys()):
        d[i] = clean_text(d[i])
        if d[i] is None or d[i] == "" or d[i] == "missing":
            del d[i]
    return d

def json2df(infile):
    df = pd.read_json(infile, lines=True)
    return df

def extractDataFromFile(infile, outfile, fields):
    df = json2df(infile)
    df[fields].apply(lambda x: x.astype(str).str.upper()).drop_duplicates().sort_values(fields).to_csv(outfile, index=False,mode="a", header=False)

def list2dict(list, sep=":"):
    result = {}
    for e in list:
        m = e.split(sep)
        if len(m) == 2:
            result[m[0].strip()] = m[1].strip()
    return result
    
    
def load_csv_to_dict(filename):
    with open(filename) as f:
        return dict(filter(None, csv.reader(f)))
