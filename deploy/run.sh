#!/bin/bash -x
set -x
python setup.py develop
# change to directory of script
cd $(dirname "$0")

python update_config.py
tail -n10 development.ini
paster --plugin=ckan db init -c development.ini
paster --plugin=ckan user add admin email=admin@admin password=abcdef123

#gunicorn ckan --workers=2 --paste development.ini -b 0.0.0.0:$PORT

paster --plugin=ckan serve development.ini
