#!/bin/sh

export DB_HOST=
export DB_NAME=
export DB_USER=
export DB_PASS=
export WEB_PORT=8080
export WEB_HOST=0.0.0.0

gunicorn -b ${WEB_HOST}:${WEB_PORT} -w 2 -k gevent -n www-dump-api
