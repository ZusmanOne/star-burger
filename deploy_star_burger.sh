#!/bin/bash

set -e
echo СКРИПТ ЗАПУЩЕН
git pull origin master
source venvburger/bin/activate
pip install -r requirements.txt
npm install
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
python manage.py collectstatic --noinput
python manage.py migrate --noinput
sudo systemctl daemon-reload
sudo systemctl reload nginx
echo СКРИПТ УСПЕШНО ВЫПОЛНЕН!



