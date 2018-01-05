import os
from cfenv import AppEnv

env = AppEnv()

with open(os.path.dirname(os.path.realpath(__file__)) + "/development.ini", "a") as config:
    print env.uris
    config.write('\n')
    config.write('ckan.site_url = https://' + env.uris[0] + '\n')
    postgres = env.get_service(label='postgres')
    config.write("sqlalchemy.url = " + postgres.credentials['uri'] + '\n')
    # config.write( "ckan.datastore.write_url = "+postgres.credentials['uri'])
    # echo 'ckan.datastore.write_url = $DATABASE_URL' > development.ini
    # ckan.datastore.read_url

    redis = env.get_service(label='redis32').credentials
    redis_url = "redis://:{}@{}:{}/0".format(redis['password'], redis['host'], redis['port'])
    config.write('ckan.redis.url = ' + redis_url + '\n')
    config.write('\n')