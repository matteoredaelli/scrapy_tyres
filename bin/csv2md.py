import sys, csv
import pandas as pd
import numpy as np
import os, datetime

header = """---
date: "2000-01-01"
title: "__BRAND__"
menu: "main"
draft: false
---

""" # % datetime.datetime.today().strftime("%Y-%m-%d")

header_ean = """---
date: "__DAY__"
title: "__BRAND__ - __EAN__"
draft: false
---

"""

filename = 'export.csv'
df = pd.read_csv(filename, sep=";")

brands_list = df.brand.drop_duplicates().tolist()
brands_list.sort()

brands = {}

for brand in brands_list:
    brands[brand] = {}
    dir = "website/content/tyres/" + brand.replace(" ", "-").lower()
    file = dir + "/_index.md"
    os.makedirs(dir, exist_ok=True)
    brands[brand]["dir"]  = dir
    brands[brand]["f"] = open(file, "w")
    brands[brand]["f"].write(header.replace("__BRAND__", brand))

with open(filename, newline='') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=';')
    for row in spamreader:
        brand = row["brand"]
        ean = row["ean"]
        day = max(row["crawled"].split(","))
        s = "- [%s](%s.html)\n" % (ean, ean)
        #brands[brand]["f"].write(s)
        file = brands[brand]["dir"] + "/" + ean + ".md"
        f = open(file, "w")
        f.write(header_ean.replace("__BRAND__", brand).replace("__EAN__", ean).replace("__DAY__", day))
        for k in row:
            s = "- %s: %s\n" % (k, row[k])
            f.write(s)
        f.close


for brand in brands_list:
    brands[brand]["f"].close()
