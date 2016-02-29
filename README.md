basil.refapi
==============

Hi, I serve some common use cases for consuming the Eve SDK Static Reference 
data as a RESTful API!


Dependencies
------------
I expect you to have a database dump in a MySQL compatible format, already 
loaded. Keeping it up to date is your problem. Just point me at it. The 
other dependencies for this project are detailed in the following usage 
options.

The `requirements/txt` and `production-requirements.txt` files list the 
python packages required to run this web service. Use the first to run
in dev mode, and use both to produce wheels which should be used to run
in production when you are satisfied with your testing.


Usage
-----
 - There is a `Vagrantfile` in `ext/` you can copy to the repo root and 
 customize. From there ensure you fill in the ENV vars needed to run 
 `start.sh` to start the server.
 - There is a `bootstrap.sh` file in `ext` you can use on any Ubuntu 14.04 or
 similar environment to set up the prerequisites to test drive this. From 
 there ensure you fill in the ENV vars needed to run `start.sh` to start the 
 server. Manually `pip install -r production-requirements.txt` to bake
 yourself a production-like deploy.
 - There are four Dockerfiles in `ext/docker` you can use to push the bits
 into a working environment (dev/production). Details can be found below.
 
 
Doing it with Docker
--------------------
This outlines the process to run this in production. Be sure to fill in the 
ENV variables for step 7. If you want to use a dev mode version you would use
a much simpler variant of this process (simply build base and dev, then run 
the dev image).
 
 1. `docker build -t apibase -f ext/docker/base .`
 2. `docker build -t make-dumpapi -f ext/docker/build  .`
 3. `docker run -it --name builder make-dumpapi `
 4. `docker cp builder:/wheelhouse .`
 5. `docker rm builder`
 6. `docker build -t prod-dumpapi -f ext/docker/run .`
 7. `docker run -d -p 8081:8081 --name dumpapi -e DB_HOST=${DB_HOST} 
    -e DB_NAME=${DB_NAME} -e DB_USER=${DB_USER} -e DB_PASS=${DB_PASS} 
    dump-api-run`
    