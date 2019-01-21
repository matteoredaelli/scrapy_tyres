# -*- coding: utf-8 -*-

#   scrapy_web
#    Copyright (C) 2016-2019 Matteo.Redaelli@gmail.com>
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

import csv
import fire
import json
import logging
import os
import sys

class ConvertText(object):
    """Convert text files"""

    def csv2json(self, filein, fileout="stdout", sep=",", encoding="utf-8"):
        if sep == "\\t":
            sep = "\t"

        if not os.path.exists(filein):
            logging.error("Input file '%s' is missing, bye!")
            sys.exit(1)

        with open(filein, newline='', encoding=encoding) as csvfile:
            #with open(filein, newline='', encoding='latin-1') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=sep)
            f = sys.stdout if  (fileout == "stdout") else open(fileout, 'w')
            for row in spamreader:
                row = dict(row)
                json.dump(row, f, ensure_ascii=False)
                f.write("\n")
            f.close

if __name__ == '__main__':
    logging.basicConfig(format='%(message)s')
    fire.Fire(ConvertText)
    sys.exit(0)
