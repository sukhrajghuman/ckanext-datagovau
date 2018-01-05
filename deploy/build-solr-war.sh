#!/bin/sh
wget -c https://archive.apache.org/dist/lucene/solr/4.3.1/solr-4.3.1.tgz
tar zxvf solr-4.3.1.tgz
cp solr-4.3.1/dist/solr-4.3.1.war ./solr.war
mkdir -p WEB-INF/lib
mkdir -p WEB-INF/resources
cp solr-4.3.1/example/resources/log4j.properties WEB-INF/resources
cp solr-4.3.1/example/lib/ext/* WEB-INF/lib
cp -r solr-4.3.1/example/solr solr
cp schema.xml solr/collection1/conf
zip -r solr.war WEB-INF solr
rm -rfv solr solr-4.3.1 WEB-INF