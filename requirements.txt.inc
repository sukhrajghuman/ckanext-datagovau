# to rebuild 
# > cat requirements.txt.inc ../ckan/requirements.txt > requirements.txt
feedparser

#cloud foundry  
#ckan
# to follow master
-e git+https://github.com/ckan/ckan#egg=ckan==alwaysinstallanewversionplz
-e git+https://github.com/maxious/ckanext-s3multipart#egg=ckanext-s3multipart==alwaysinstallanewversionplz
boto
gunicorn
cfenv
