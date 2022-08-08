#!/bin/bash

# python venv
pydir="/p3/"
if [ ! -d "$pydir" ]; then
  echo "Installing p3 venv"
  virtualenv -p python3 p3
fi
. p3/bin/activate && pip install -r requirements.txt

. p3/bin/activate && python schemas.py


# docker
#dv=$(docker --version)
#if grep -q "Docker version" <<< "$dv"; then
#  echo "$dv" allready installed
#else
#  echo "Installing docker now..."
#  curl -fsSL https://get.docker.com -o get-docker.sh
#  ./get-docker.sh
#   apt install docker-compose
#fi

# dockerized mysql
# docker exec -it adia_mysql mysql -p --password=9999
#dps=$(docker ps)
#if grep -q "prueba_adia_mysql" <<< "$dps"; then
#  echo "$dps"
#  echo "dockerized mysql is installed yet"
#else
#  echo "Installing mysql now..."
#  mkdir -p data/db
#  docker-compose up -d
#  #docker run -d -p 3306:3306 --name adia_mysql -e MYSQL_ROOT_PASSWORD=9999 mysql
#fi
#loguear y crear db
#docker exec -it adia_mysql mysql -p --password=9999
# esto te toca hacerlo a mano o python:
# CREATE DATABASE prueba_adia_db;

## dockerized mongo
#mkdir -p "db/mongo_files"
#dps=$(docker ps)
#if grep -q "db_mongo" <<< "$dps"; then
#  echo "$dps"
#else
#  echo "Installing mongo now..."
#  docker pull mongo
#  docker run -it -v db/mongo_files/data/db --name db_mongo -d mongo
#fi
