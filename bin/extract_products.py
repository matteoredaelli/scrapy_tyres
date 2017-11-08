# -*- coding: utf-8 -*-

#    Copyright (C) 2016-2017 Matteo.Redaelli@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pandas as pd

import re, sys

if len(sys.argv) != 2:
    print('Usage: ' + sys.argv[0] + ' <sourcefile.json>')
    sys.exit(1)

# Grab the input and output
source = sys.argv[1]

def remove_extra_text(text):
    import re
    text = text \
            .replace("PNEUMATICO", "") \
            .replace("CHIODABILE", "") \
            .replace("CHIODATO", "") \
            .replace("RINNOVATI", "") \
            .replace("(", "") \
            .replace(")", "") \
            .replace("MFS", "") \
            .replace("FSL", "") \
            .replace("NORDIC", "") \
            .replace("STREET CAR", "") \
            .replace("COMPOUND", "")
    text = re.sub(' CON .+$)', '', text)
    text = re.sub(' DOPPIA INDENTIFICAZIONE ', ' ', text)
    text = re.sub(' DOPPIE INDICAZIONI ', ' ', text)
    text = re.sub(' \*.+$', ' ', text)
    text = re.sub(' SCT+$', ' ', text)
    return re.sub(' +', ' ', text).strip()


def normalize_common_pre(df):
    return df\
      .filter(df.id.isNotNull()) \
      .filter(df.id != '') \
      .filter(df.brand.isNotNull()) \
      .filter(df.brand != '') \
      .filter(df.size.isNotNull()) \
      .filter(df.size != '') \
      .select(*(upper(col(c)).alias(c) for c in df.columns)) \
      .withColumn("brand",       regexp_replace("brand", "[-_]", " ")) \
      .withColumn("price",       regexp_replace("price", " €",   "")) \
      .withColumn("price",       regexp_replace("price", ",",    ".")) 

def normalize_common_post(df):
    return df

def normalize_autodocit(df):
    return df\
      .filter(regexp_extract('description', '(rinnovati)', 1) == '') \
      .withColumn("id",          trim(regexp_replace("id",       "MPN: ",""))) \
      .withColumn("ean",         trim(regexp_replace("ean",      "EAN: ",""))) \
      .withColumn("country",     lit("IT")) \
      .withColumn("currency",    lit("EUR")) \
      .withColumnRenamed("season", col("stagione")) \
      .withColumnRenamed("Pneumatici Runflat:",  "runflat") \
      .withColumnRenamed("Pneumatici chiodati:", "chiodabile")

def normalize_gommadrettoit(df):
    return df\
      .filter(regexp_extract('size', '(rinnovati)', 1) == '') \
      .withColumn("id",          trim(regexp_replace("id",       "MPN: ",""))) \
      .withColumn("ean",         trim(regexp_replace("ean",      "EAN: ",""))) \
      .withColumn("mfs",         regexp_extract("size",   "(MFS|FSL|bordo di protezione|bordino di protezione)", 1)) \
      .withColumn("xl",          regexp_extract("size",   " (XL|RF)\s*", 1)) \
      .withColumn("studded",     regexp_extract("size",   " (chiodato)\s*", 1)) \
      .withColumn("studdable",   regexp_extract("size",   " (chiodabile)\s*", 1)) \
      .withColumn("country",     lit("IT")) \
      .withColumn("currency",    lit("EUR")) \


df = pd.read_json(source, lines=True)


## extract brands

for field in ["brand", "product", "description"]:
    filename="data/%s" % field
    df[[field]].drop_duplicates().apply(lambda x: x.astype(str).str.upper()).sort_values(field).to_csv(filename, index=False,mode="a", header=False)
