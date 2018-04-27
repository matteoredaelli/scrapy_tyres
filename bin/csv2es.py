import sys, csv
import os, datetime


from elasticsearch import Elasticsearch
import logging, json


hostname = sys.argv[1]
index = sys.argv[2]
doc_type = "tyre"
es = Elasticsearch([hostname])

es.indices.create(index=index, ignore=400)

filename = 'export.csv'

with open(filename, newline='') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=';')
    for row in spamreader:
        row = dict(row)
        ean = row["ean"]
        #row["_id"] = row["ean"]
        print(ean)
        es.index(index=index, doc_type=doc_type, id=ean, body=row)
