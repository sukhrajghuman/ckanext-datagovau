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

        print "using ZIP file " + zip_resource['url'].replace('https', 'http')
        (filepath, headers) = urllib.urlretrieve(zip_resource['url'].replace('https', 'http'), "input.zip")
        print "zip downloaded"
        # use unzip program rather than python's zipfile library for maximum compatibility
        rv = subprocess.call(['unzip', filepath])
        # with ZipFile(filepath, 'r') as myzip:
        #	myzip.extractall()
        print "zip unzipped"


        interesting_extensions = ["csv", "xls", "xlsx", "json", "geojson", "shp", "kml"]
        # Multiple files transform to multiple file resources
        resource_files = []
        # Multiple folders transform to multiple zip file resources
        resource_dirs = []
        for f in os.listdir(tempdir):
            if os.path.isfile(os.path.join(tempdir, f)):
                if f.split('.').pop().lower() in interesting_extensions:
                    resource_files.append(f)
            if os.path.isdir(os.path.join(tempdir, f)):
                # only zip up folders if they contain at least one interesting file
                interesting_dir_files = []
                for g in os.listdir(os.path.join(tempdir, f)):
                    if g.split('.').pop().lower() in interesting_extensions:
                        interesting_dir_files.append(os.path.join(f, g))
                        break
                if len(interesting_dir_files) > 0:
                    resource_dirs.append(f)


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

        print resource_files
        # Check for single csv/xls/shp/kml files - no action required
        if len(resource_files) > 1:
            for file in resource_files:
                path = os.path.join(tempdir, file)
                update_resource(file, path)

        print resource_dirs
        for dir in resource_dirs:
            zipf = zipfile.ZipFile(dir + '.zip', 'w', zipfile.ZIP_DEFLATED)
            zipdir(dir, zipf)
            zipf.close()
            update_resource(dir, dir + '.zip')
