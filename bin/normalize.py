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

from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import *
from pyspark.sql.types import *
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import re, sys, csv

RECORDS_TO_SHOW=30

if len(sys.argv) != 2:
    print('Usage: ' + sys.argv[0] + ' <source>')
    sys.exit(1)

# Grab the input and output
source = sys.argv[1]

# warehouse_location points to the default location for managed databases and tables
warehouse_location = 'spark-warehouse'

spark = SparkSession \
    .builder \
    .appName(sys.argv[0]) \
    .config("spark.sql.warehouse.dir", warehouse_location) \
    .enableHiveSupport() \
    .getOrCreate()
spark.sparkContext.setLogLevel('WARN')

def write_values(values, outpath, mode="overwrite"):
    of = open(outpath, 'w')
    for l in values:
        of.write(str(l))
        of.write("\n")
    of.close()
    ## df = spark.createDataFrame(zip(iter(values)), ["value"])
    ## df.write.csv(outpath, mode="overwrite")

def stats(df):
    print("Total records=%d" % df.count())
    print(df.columns)
    write_values(df.columns, "data/db/columns")
    for f in df.columns:
        print("Column %s" % f)
        values = df.select(f).distinct().rdd.map(lambda row : row[0]).collect()

        print(" distinct values: %d" % len(values))
        outpath="data/db/" + f
        write_values(values, outpath)
        df.groupBy(f).count().orderBy('count', ascending=False).show(RECORDS_TO_SHOW, False)

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

remove_extra_text_udf = udf(remove_extra_text, StringType())

def normalize_common_pre(df):
    df1 = df.dropDuplicates() \
             .filter(df.id.isNotNull()) \
             .filter(df.id != '') \
             .toDF(*[c.lower().strip().replace(" ", "") for c in df.columns])
    return df1.select(*(upper(col(c)).alias(c) for c in df1.columns))

def normalize_common_ot(df): df \
    .withColumn("crawled", crawled[0:10]) \
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

def normalize_gommadirettoit(df):
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


def main():
    df = spark.read.json(source)
    stats(normalize_common_pre(df))

if __name__== "__main__":
  main()
