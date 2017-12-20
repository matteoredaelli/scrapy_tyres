# -*- coding: utf-8 -*-

#   scrapy_tyres
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
#
elasticserver=$1
YEAR=$(date +%Y)
MONTH=$(date +%m)
DAY=$(date +%d)
outdir="data/sources"
prefix=$YEAR-$MONTH-$DAY
mkdir -p $outdir

scrapy list > data/sources.csv

for spider in $(scrapy list) ; do
    filename=$outdir/$prefix-$spider.json
    echo scrapy crawl "${spider}" -t jsonlines -o $filename
    echo python3 bin/extract_products.py $filename.json $elasticserver
done
