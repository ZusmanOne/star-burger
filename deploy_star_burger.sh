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
curl -H "X-Rollbar-Access-Token: 818f735ce59e48a1bfa752dfbcc23378"
-H "Content-Type: application/json" -X POST 'https://api.rollbar.com/api/1/deploy'
-d '{"environment": "venvburger", "revision": "53570a46342e23d224532672ef4824c69438baae",
 "rollbar_name": "login_name", "local_username": "zusmanone", "comment": "success deploy", "status": "succeeded"}'
echo СКРИПТ УСПЕШНО ВЫПОЛНЕН!



