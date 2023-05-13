#!/bin/bash


echo СКРИПТ ЗАПУЩЕН
git pull origin master
docker-compose -f docker-compose.prod.yml up
echo "Контейнеры запущены"


