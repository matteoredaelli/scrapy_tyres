import sys, csv,re
import pandas as pd
import numpy as np


#re.match(r"^(.+) (P|LT|T)?(\d+(\.\d+)?)/(\d+(\.\d+)?) (Z?R)?(\d+) (\d+(/\d+)?)(\w) ?(\w*)", s).groups()

#^(.+) (P|LT|T)?(\d+(\.\d+)?)\/(\d+(\.\d+)?) (Z?R|-)?(\d+)(C?) (\d+(\/\d+)?)(\w) (.*)


filename = sys.argv[1]
print(filename)
df = pd.read_csv(filename, sep=";")

def csv2ml(row):
        description = row["description"].split(",")[0]
        desc = description.replace(")", "").replace("(", "").replace("+", "\+").replace("*", "\+")
        print("from: " + desc)
        speed_index = row["speed_index"]
        if speed_index is None or speed_index == "":
                speed_index = "\w"
                
        reg = r"^(%s) (%s) (P|LT)?(%s)/(%s) (Z?R)?(%s) (%s)(%s)" % (row["brand"], row["product"], row["width"], row["series"], row["rim"], row["load_index"], speed_index)
        index = row["load_index"] + row["speed_index"].replace("(", "").replace(")","")
        if index == "" or index is None:
                return
        
        r = r"^(.+ %s)" % index
        desc = re.sub(r, "\\1", desc)

        match = re.match(reg, desc)
        if match:
                m = match.groups()
                print("[%s](brand) [%s](product) [%s](type) [%s](width) (%s) (%s)?(%s) (%s)(%s)" % m)

        print(desc + "\n")

with open(filename, newline='') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=';')
    for row in spamreader:
        csv2ml(row)
