import ckanapi # download from https://github.com/ckan/ckanapi and include in your scraper repo

destination = ckanapi.RemoteCKAN('http://data.gov.au','')
results = destination.action.package_search(rows=1000,fq="-harvest_portal:* and harvest_source_title:data.sa")
print results['count']

for result in results['results']:
    print "delete from harvest_object_error where harvest_object_id in (select id from harvest_object where package_id ='"+ result['id']+"');"
    print "delete from harvest_object_extra where harvest_object_id in (select id from harvest_object where package_id ='"+ result['id']+"');"
    print "delete from harvest_object where package_id = '"+ result['id']+"';"
