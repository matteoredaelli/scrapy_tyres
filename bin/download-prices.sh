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
done

for r in $(cat data/sizes.csv) ; do
  w=$(echo $r |cut -f1 -d',')
  s=$(echo $r |cut -f2 -d',')
  d=$(echo $r |cut -f3 -d',')
  filename=$outdir/$prefix-autopink-shop.it.json
  echo scrapy crawl autopink-shop.it -t jsonlines -o $filename -a width=$w -a series=$s -a diameter=$d -a details=1
  filename=$outdir/$prefix-gommadiretto.it.json
  echo scrapy crawl gommadiretto.it -t jsonlines -o $filename -a width=$w -a series=$s -a diameter=$d -a details=1
done
