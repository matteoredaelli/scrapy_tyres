## -*- coding: utf-8 -*-

import sys
import csv
import numpy as np
import os, datetime
import datetime

import logging, json


filein = sys.argv[1]
fileout = sys.argv[2]
source = sys.argv[3]
today = datetime.datetime.strptime(sys.argv[4], "%Y-%m-%d")

sep = sys.argv[5] if len(sys.argv) == 6 else "\n"

if sep == "\\t":
    sep = "\t"

with open(filein, newline='', encoding='utf-8') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=sep)
    with open(fileout, 'w') as f:
        for row in spamreader:
            row = dict(row)
            row["source"] = source
            row["crawled"] = today

            json.dump(row, f, ensure_ascii=False)
            f.write("\n")
