import sys, csv
import pandas as pd
import numpy as np

filename = sys.argv[1]
df = pd.read_csv(filename, sep=";")[["ean", "manufacturer_number", "description"]]


with open(filename, newline='') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=';')
    for row in spamreader:
        row = {k:v for k, v in row.items() if k in ("ean", "manufacturer_number", "description")}
        if row["ean"] and row["ean"] != "":
            s = "__LABEL__%s %s" % (row["ean"], " ".join(row.values()))
            print(s)
