#!/usr/bin/python
# coding=utf-8
'''
zip extractor for data.gov.au
<alex.sadleir@linkdigital.com.au>
1.0  06/11/2015  initial implementation
'''
import ckanapi  # https://github.com/open-data/ckanapi
import sys, errno, tempfile, os, urllib, subprocess
from dateutil import parser
from datetime import datetime
from datetime import datetime
import zipfile
import zlib

# https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

if len(sys.argv) != 4:
    print "zip extractor. command line: api_url api_key dataset_id"
    sys.exit(errno.EACCES)
else:
    (path, api_url, api_key, dataset_id) = sys.argv

ckan = ckanapi.RemoteCKAN(address=api_url, apikey=api_key)
print dataset_id
dataset = ckan.action.package_show(id=dataset_id)
print "loaded dataset" + dataset['name']
# pprint(dataset)
data_modified_date = dataset['metadata_modified']
activity_list = ckan.action.package_activity_list(id=dataset['id'])
# checking that bot was not last editor ensures no infinite loop
# todo scan for last date of non-bot edit
# Or last modified date could be compared with zip_extracted resources scan dates set.
if len(activity_list) > 0 and activity_list[0]['user_id'] == "68b91a41-7b08-47f1-8434-780eb9f4332d" \
    and activity_list[0]['timestamp'].split("T")[0] != datetime.now().isoformat().split("T")[0]:
    print 'last editor was bot'
    sys.exit(0)
print "Data modified: " + str(parser.parse(data_modified_date))

for resource in dataset['resources']:
    if "zip" in resource['format'].lower():
        zip_resource = resource
        if 'zip_extract' not in zip_resource or zip_resource.get('zip_extract', '') != 'True':
            print 'zip resource ' + resource['name'] + ' ('+resource['id']+ ') not opted in for extraction: ' + zip_resource.get('zip_extract', '')
            continue

        # download resource to tmpfile
        tempdir = tempfile.mkdtemp(dataset['id'])
        os.chdir(tempdir)
        print tempdir + " created"

        # urlretrieve does not work with https. We can't really get files through an https connection without
        # going through a proxy
        print "using ZIP file " + zip_resource['url'].replace('https', 'http')
        (filepath, headers) = urllib.urlretrieve(zip_resource['url'].replace('https', 'http'), "input.zip")
        print "zip downloaded"
        # use unzip program rather than python's zipfile library for maximum compatibility
        rv = subprocess.call(['unzip', filepath])
        #with ZipFile(filepath, 'r') as myzip:
        #    myzip.extractall()
        #zipfile.ZipFile(filepath, 'r').extractall()
        print "zip unzipped"

        interesting_extensions = ["csv", "xls", "xlsx", "json", "geojson", "shp", "kml"]
        # Multiple files transform to multiple file resources
        resource_files = []

        def update_resource(file, path):
            print "updating/creating "+file
            existing = False
            for resource in dataset['resources']:
                if resource['name'] == file:
                    existing = True
                    resource['last_modified'] = datetime.now().isoformat()
                    print ckan.call_action('resource_update', resource, files={'upload': open(path)})
            if not existing:
                print ckan.call_action('resource_create', {"package_id": dataset['id'], "name": file, "url": file,
                                                           "parent_res": zip_resource['id'],
                                                           "zip_extracted": "True", "last_modified": datetime.now().isoformat()},
                                                            files={'upload': open(path)})

        def count_interesting(path):
            for g in os.listdir(path):
                if g.split('.').pop().lower() in interesting_extensions:
                    return 1
            return 0

        def recurse_directory(path):
            if (len([fn for fn in os.listdir(path)]) < 3 and len([ndir for ndir in os.listdir(path) if os.path.isdir(ndir)]) == 1):
                for f in os.listdir(path):
                    if os.path.isdir(os.path.join(path,f)):
                        return recurse_directory(os.path.join(path,f))

            os.chdir(path)
            numInteresting = len([f for f in os.listdir(path) if (os.path.isfile(os.path.join(path, f)) and (f.split('.').pop().lower() in interesting_extensions))])
            for f in os.listdir(path):
                if os.path.isfile(os.path.join(path, f)) and numInteresting > 1:
                    if f.split('.').pop().lower() in interesting_extensions:
                        update_resource(f, os.path.join(path, f))
                if os.path.isdir(os.path.join(path, f)):
                    # only zip up folders if they contain at least one interesting file
                    if count_interesting(os.path.join(path, f)) > 0:
                        zipf = zipfile.ZipFile(f + '.zip', 'w', zipfile.ZIP_DEFLATED)
                        zipdir(f, zipf)
                        zipf.close()
                        update_resource(f, f+'.zip')

        recurse_directory(tempdir)