import ckanapi # download from https://github.com/ckan/ckanapi and include in your scraper repo

destination = ckanapi.RemoteCKAN('http://data.gov.au')
results = destination.action.package_search(rows=1000,fq="owner_org:cd2fe71e-4353-41a3-9201-05602b04110d and -harvest_source_id:*")
print results['count']

for result in results['results']:

    print ""
    print "loading",result['name']
    if 'aims-data-catalogue' != result['name']:
        dataset = destination.action.package_show(id=result['name'])

        try:
            result = destination.call_action('package_delete', dataset)
            print "dataset deleted"
        except Exception,e:
            print ""
            print "dataset " + result['name'] + ' failed'
            print str(e)
            print ""
