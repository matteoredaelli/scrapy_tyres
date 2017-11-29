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

import tyre_utils

import json, os, re, sys

if len(sys.argv) != 2:
    print('Usage: ' + sys.argv[0] + ' <sourcefile.json>')
    sys.exit(1)

# Grab the input and output
source = sys.argv[1]

out_prefix="data/tyres"

with open(source, 'r') as f:
    for line in f:
        line = line.strip()
        item = json.loads(line)
        item_new = tyre_utils.extractAll(item["description"])
        item = tyre_utils.mergeItems(item, item_new)
        if "ean" in item:
            outpath = "%s/%s/%s" % (out_prefix, item["brand"], item["ean"])
            filename = "%s/%s.json" % (outpath, item["source"])
            tyre_utils.updateMLTrainFile(item)
        else:
            outpath = "%s/%s" % (out_prefix, item["brand"])
            outpath = outpath.replace(" ","-")
            filename = "%s/%s.json" % (outpath, item["id"])
        outpath = outpath.replace(" ","-")
        filename = filename.replace(" ","-")       
        os.makedirs(outpath, exist_ok=True)
        with open(filename, 'w') as txtfile:
            json.dump(item, txtfile)