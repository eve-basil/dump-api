basil-dump-api
==============

Hi, I serve some common use cases for consuming the Eve Dump as a RESTful API!


Dependencies
------------
I expect you to have a database dump in a MySQL compatible format, already 
loaded. Keeping it up to date is your problem. Just point me at it. The 
other dependencies for this project are detailed in the following usage 
options.


Usage
-----
 - There is a `Vagrantfile` in `ext/` you can copy to the repo root and 
 customize. From there ensure you fill in the ENV vars needed to run 
 `start.sh` to start the server.
 - There is a `bootstrap.sh` file in `ext` you can use on any Ubuntu 14.04 or
 similar environment to set up the prerequisites. From there ensure you fill
 in the ENV vars needed to run `start.sh` to start the server.
 - There are three `Dockerfile`s in `ext/docker` you can use to push the bit
 into a working environment. Details can be found below.
 
 
Doing it with Docker
--------------------
Be sure to fill in the ENV variables for step 7. 
 
1. docker build -t dump-api-base -f ext/docker/base.docker .
2. docker build -t dump-api-build -f ext/docker/build.docker  .
3. docker run -it --name builder dump-api-build 
4. docker cp builder:/wheelhouse .
5. docker rm builder
6. docker build -t dump-api-run -f ext/docker/run.docker .
7. docker run-d -p 8081:8081 -e DB_HOST=${DB_HOST} -e DB_NAME=${DB_NAME} \
    -e DB_USER=${DB_USER} -e DB_PASS=${DB_PASS} --name dumpapi  dump-api-run
    