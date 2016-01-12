#!/usr/bin/python
# coding=utf-8
'''
energyrating.gov.au scraper for data.gov.au
<alex.sadleir@linkdigital.com.au>
1.0  10/9/2013  initial implementation
1.01 12/11/2013 made resource categories case insensitive and updated entries
1.02 02/04/2014 added computer monitors category
1.03 07/04/2014 error handling around file store URL
1.04 30/04/2014 change both api links to https and increase file store wait time
2.0  21/10/2014 Use new file upload API
'''

import ckanapi # get from https://github.com/open-data/ckanapi

import os
import urllib2
import time
from os.path import basename

import sys
from urlparse import urlsplit
import tempfile


class LoaderError(Exception):
    pass

#http://diveintopython.org/http_web_services/etags.html
class NotModifiedHandler(urllib2.BaseHandler):
    def http_error_304(self, req, fp, code, message, headers):
        addinfourl = urllib2.addinfourl(fp, headers, req.get_full_url())
        addinfourl.code = code
        return addinfourl

def fetchURL(url):
    #url = canonurl(url)
    req = urllib2.Request(url)
    print "Fetching %s" % (url)
    if url.startswith("mailto") or url.startswith("javascript") or url.startswith("#") or url == None or url == "":
        print >> sys.stderr, "Not a valid HTTP url"
        return (None, None, None)
    req.add_header("User-Agent", "Mozilla/4.0 (compatible; data.gov.au webspider)")
    opener = urllib2.build_opener(NotModifiedHandler())
    try:
        url_handle = opener.open(req, None, 20)
        print "Fetch completed"
        content = url_handle.read()
        localName = basename(urlsplit(url)[2])
        if url_handle.info().has_key('Content-Disposition'):
            # If the response has Content-Disposition, we take file name from it
            localName = url_handle.info()['Content-Disposition'].split('filename=')[1]
            if localName[0] == '"' or localName[0] == "'":
                localName = localName[1:-1]
        return (localName, None, content)
        #store as attachment epoch-filename
    except (urllib2.URLError) as e:

        error = ""
        if hasattr(e, 'reason'):
            error = "error %s in downloading %s" % (str(e.reason), url)
        elif hasattr(e, 'code'):
            error = "error %s in downloading %s" % (e.code, url)
        print error
        return (None, None, None)

# Instantiate the CKAN client.
api_key = 'c3557c21-bfda-44e7-a5c3-c97de603d56b'
server = 'data.gov.au'


ckandirect = ckanapi.RemoteCKAN('http://' + server, apikey=api_key)

household_category_urls = {
    "air conditioners": "http://reg.energyrating.gov.au/comparator/product_types/64/search/?&export_format=csv",
    "clothes dryers": "http://reg.energyrating.gov.au/comparator/product_types/35/search/?&export_format=csv",
    "clothes washers": "http://reg.energyrating.gov.au/comparator/product_types/49/search/?&export_format=csv",
    "computer monitors": "http://reg.energyrating.gov.au/comparator/product_types/74/search/?&export_format=csv",
    "dishwashers": "http://reg.energyrating.gov.au/comparator/product_types/41/search/?&export_format=csv",
    "fridges and freezers": "http://reg.energyrating.gov.au/comparator/product_types/28/search/?&export_format=csv",
    "televisions": "http://reg.energyrating.gov.au/comparator/product_types/32/search/?&export_format=csv"
}

unlabeled_category_urls = {
    "air conditioners": "http://reg.energyrating.gov.au/comparator/product_types/64/search/?&export_format=csv",
    "ballasts": "http://reg.energyrating.gov.au/comparator/product_types/51/search/?&export_format=csv",
    "chillers": "http://reg.energyrating.gov.au/comparator/product_types/59/search/?&export_format=csv",
    "close control air conditioners": "http://reg.energyrating.gov.au/comparator/product_types/60/search/?&export_format=csv",
    "commercial refrigerators": "http://reg.energyrating.gov.au/comparator/product_types/37/search/?&export_format=csv",
    "compact fluorescent lamps": "http://reg.energyrating.gov.au/comparator/product_types/61/search/?&export_format=csv",
    "computers": "http://reg.energyrating.gov.au/comparator/product_types/73/search/?&export_format=csv",
    "distribution transformers": "http://reg.energyrating.gov.au/comparator/product_types/38/search/?&export_format=csv",
    "electric motors": "http://reg.energyrating.gov.au/comparator/product_types/54/search/?&export_format=csv",
    "elv lighting converter/transformer": "http://reg.energyrating.gov.au/comparator/product_types/39/search/?&export_format=csv",
    "external power supply": "http://reg.energyrating.gov.au/comparator/product_types/55/search/?&export_format=csv",
    "hot water heaters (electric)": "http://reg.energyrating.gov.au/comparator/product_types/58/search/?&export_format=csv",
    "hot water heaters (gas)": "http://reg.energyrating.gov.au/comparator/product_types/62/search/?&export_format=csv",
    "incandescent lamps": "http://reg.energyrating.gov.au/comparator/product_types/40/search/?&export_format=csv",
    "linear fluorescent lamps": "http://reg.energyrating.gov.au/comparator/product_types/34/search/?&export_format=csv",
    "set top boxes": "http://reg.energyrating.gov.au/comparator/product_types/33/search/?&export_format=csv"
}

energy_pkgs = {
    "energy-rating-for-household-appliances": household_category_urls,
    "energy-rating-data-for-household-appliances-non-labelled-products": unlabeled_category_urls
}

if __name__ == "__main__":
        #print pkg
        for pkg_name, category_urls in energy_pkgs.iteritems():
            pkg = ckandirect.action.package_show(id=pkg_name)
            for resource in pkg['resources']:
                print "Updating resource: " + resource['name']
                resource_category = resource['name'].split('-')[0].strip()
                if resource_category.lower() not in category_urls:
                    print ("Appliance category not found: " + resource_category)
                else:
                    (returned_filename, mime_type, content) = fetchURL(category_urls[resource_category.lower()])
                    #print content
                    suffix = "_"+returned_filename.encode("ascii", "ignore").replace("/", "")
                    #add file extension if missing
                    if len(suffix) < 5 or (suffix[-4] != "." and suffix[-5] != "."):
                        suffix = suffix + "." + "csv"
                    if content != None :
                        tf = tempfile.NamedTemporaryFile(suffix=suffix)
                        tfName = os.path.abspath(tf.name)
                        print "CSV temporarily downloaded to " +tfName
                        tf.seek(0)
                        tf.write(content)
                        tf.flush()
                        resource['name'] = resource_category + " - " + returned_filename
                        time1 = time.time()
                        ckandirect.action.resource_update(id =resource['id'], name=resource['name'], data_dict=resource, upload=open(tfName))
                        time2 = time.time()
                        print "Resource successfully updated with new data URL in %0.3f ms" % ((time2-time1)*1000.0)
                    else:
                        print "Error uploading file: " + returned_filename
