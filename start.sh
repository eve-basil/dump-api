#!/bin/sh

##
# Ensure these are all set in the environment
#
# export DB_HOST=
# export DB_NAME=
# export DB_USER=
# export DB_PASS=
# export WEB_WORKERS=2
# export WEB_PORT=8080
# export WEB_HOST=0.0.0.0

gunicorn -b ${WEB_HOST}:${WEB_PORT} -w ${WEB_WORKERS} -k gevent \
    basil-dump-api.server:application
