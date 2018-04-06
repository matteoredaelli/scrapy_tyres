import sys, csv
import pandas as pd
import numpy as np

filename = 'export.csv'
df = pd.read_csv(filename, sep=";")

brands_list = df.brand.drop_duplicates().tolist()
brands_list.sort()

brands = {}

def csv2html(row, f):
    f.write("\n<h2>ean %s</h2>\n<ul>" % (row["ean"]))
    
    for k in ["description", "manufacturer_number", "product"]:
        s = "<li>%s: %s</li>\n" % (k, row[k])

        f.write(s)
    f.write("</ul>\n")
    

for brand in brands_list:
    brands[brand] = {}
    file = "static/" + brand.replace(" ", "-").lower() + ".html"
    brands[brand]["filename"]  = file
    brands[brand]["f"] = open(file, "w")
    brands[brand]["f"].write("<h1>%s</h1>\n" % brand)


with open(filename, newline='') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=';')
    for row in spamreader:
        brand = row["brand"]
        csv2html(row, brands[brand]["f"])

for brand in brands_list:
    brands[brand]["f"].close()
