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

from tyre import item as tyre_item

import store_fs, store_es

import json, os, re, sys

import logging
import scrapy_tyres.pipelines
import init

PIPELINES = ['scrapy_tyres.pipelines.MappingFieldsPipeline', 'scrapy_tyres.pipelines.CleanValuesPipeline', 'scrapy_tyres.pipelines.NormalizeCommonValuesPipeline', 'scrapy_tyres.pipelines.UppercasePipeline', 'scrapy_tyres.pipelines.NormalizeFieldsPipeline']

pipelines = {}
for p in PIPELINES:
    newclass = "%s()" % p
    pipelines[p] = eval(newclass)

if len(sys.argv) < 2:
    print('Usage: ' + sys.argv[0] + ' <sourcefile.json>')
    sys.exit(1)

# Grab the input and output
source = sys.argv[1]

out_prefix="data/tyres"


# when using from command line --log=DEBUG
# getattr(logging, loglevel.upper())


with open(source, 'r') as f:
    for line in f:
        line = line.strip()
        item = json.loads(line)

        for p in pipelines:
            function = "pipelines[\"%s\"].process_item(item, 0)" % p
            item = eval(function)
        item_new = tyre_item.extractAll(item)
        item = tyre_item.mergeItems(item, item_new)

        ##if "ean" in item:
        ##  tyre.utils.updateMLTrainFile(item)
            
        if "ean" in item:
            logging.warning("Parsing %s" % item["ean"])
            init.es.saveItem(item)
            if "brand" in item:
                init.es.saveBrandIfNew(item["brand"])
            #init.store_fs.saveItem(item)
        else:
            outpath = "%s/parked/%s" % (out_prefix, item["brand"])
            filename = "%s/%s.json" % (outpath, item["description"].replace("/","-"))
            outpath = outpath.replace(" ","-")
            filename = filename.replace(" ","-").replace("'","")
            os.makedirs(outpath, exist_ok=True)
            with open(filename, 'w+') as f:
                json.dump(item, f)
            f.closed
