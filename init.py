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

import tyre.item
import utils

import store_fs, store_es
import json, os, re, sys
import logging

es = store_es.ES()
#store_fs = store_fs.FS()

#logging.basicConfig(filename='extract_products.log',level=logging.WARNING)
logging.basicConfig(level=logging.WARNING)

# when using from command line --log=DEBUG
# getattr(logging, loglevel.upper())

source_fields_mapping = utils.load_csv_to_dict("data/source-fields-mapping.csv")
source_fields_mapping = utils.load_csv_to_dict("data/source-fields-mapping.csv")
