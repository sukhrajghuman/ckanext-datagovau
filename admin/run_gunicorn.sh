#!/bin/bash
cd /var/lib/ckan/dga/pyenv/src/ckan/
source /var/lib/ckan/dga/pyenv/bin/activate
export NEW_RELIC_CONFIG_FILE="/var/lib/ckan/dga/pyenv/src/ckan/newrelic.ini"
newrelic-admin run-program /var/lib/ckan/dga/pyenv/bin/gunicorn \
my_ckan:application \
-b :8080 \
-n 2 \
-k gevent \
--max-requests 1000 \
--log-level warning
#--paste /var/lib/ckan/dga/pyenv/src/ckan/development.ini
#--debug --log-level debug \
