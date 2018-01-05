#!/bin/sh
wget -c http://sourceforge.net/projects/geoserver/files/GeoServer/2.12.1/geoserver-2.12.1-war.zip
wget -c http://sourceforge.net/projects/geoserver/files/GeoServer/2.12.1/extensions/geoserver-2.12.1-pyramid-plugin.zip
wget -c http://sourceforge.net/projects/geoserver/files/GeoServer/2.12.1/extensions/geoserver-2.12.1-vectortiles-plugin.zip
mkdir geoserver
cd geoserver
unzip ../geoserver-2.12.1-war.zip
unzip -o ../geoserver-2.12.1-pyramid-plugin.zip
unzip -o ../geoserver-2.12.1-vectortiles-plugin.zip
mkdir -p WEB-INF/lib
mv *.jar WEB-INF/lib
mkdir data
cp -rfv ../geodata/* data/
zip -r geoserver.war WEB-INF data