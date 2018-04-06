import sys, csv
import pandas as pd
import numpy as np


header = """---
path: "/tireX/__BRAND__"
date: "2018-03-30"
title: "Tyre brand __BRAND__"
---

"""

filename = 'export.csv'
df = pd.read_csv(filename, sep=";")

brands_list = df.brand.drop_duplicates().tolist()
brands_list.sort()

brands = {}

for brand in brands_list:
    brands[brand] = {}
    file = "gatsby-site/src/pages/" + brand.replace(" ", "-").lower() + ".md"
    brands[brand]["filename"]  = file
    brands[brand]["f"] = open(file, "w")
    brands[brand]["f"].write(header.replace("__BRAND__", brand))

with open(filename, newline='') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=';')
    for row in spamreader:
        brand = row["brand"]
        s = "\n## %s\n" % (row["ean"])
        brands[brand]["f"].write(s)
        for k in row:
            s = "- %s: %s\n" % (k, row[k])
            brands[brand]["f"].write(s)


for brand in brands_list:
    brands[brand]["f"].close()
