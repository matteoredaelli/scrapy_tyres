export es=http://localhost:9200/tyredb

curl -XDELETE $es
curl -XPUT $es
