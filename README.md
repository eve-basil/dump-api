basil.refapi
==============

[![Build Status](https://travis-ci.org/eve-basil/refapi.svg?branch=master)](https://travis-ci.org/eve-basil/refapi)

Hi, I serve some common use cases for consuming the Eve SDK Static Reference 
data as a RESTful API!


Dependencies
------------
I expect you to have a database dump in a MySQL compatible format, already 
loaded. Keeping it up to date is your problem. Just point me at it.

I expect you to have a Redis service available. Maintaining it is also your
problem. See the notes below for *Loading Redis* under the *Usage* heading for
instructions on how to load the expected data into Redis.

The `requirements.txt` and `production-requirements.txt` files list the 
python packages required to run this web service. Use the first to run
in dev mode, and use both to produce wheels which should be used to run
in production when you are satisfied with your testing.

Usage
-----

### Loading Redis
- ensure you have the `blueprints.yaml` file available locally, see also 
  `ext/fetch-data.sh` for how and where to get it.
- define each of the following env vars:
    - `REDIS_HOST` (e.g. `=localhost`)
    - `REDIS_PASSWORD` (e.g. `=""`)
    - `BLUEPRINTS_FILE` (e.g. `data/blueprints.yaml`)
- run `python basil_refapi/migrate.py` 

### Vagrant
- There is a `Vagrantfile` in `ext/` you can copy to the repo root and 
  customize. From there ensure you fill in the ENV vars needed to run 
 `start.sh` to start the server.
- There is a `bootstrap.sh` file in `ext` you can use on any Ubuntu 14.04 or
  similar environment to set up the prerequisites to test drive this. From 
  there ensure you fill in the ENV vars needed to run `start.sh` to start the 
  server. Manually `pip install -r production-requirements.txt` to bake
  yourself a production-like deploy. 

### Docker
There are four Dockerfiles in `ext/docker` you can use to push the bits into a
working environment (dev/production). 

Be sure to fill in the ENV variables for step 7. If you want to use a dev mode
version you would use a much simpler variant of this process (simply build
base and dev, then run the dev image).
 
 1. `docker build -t apibase -f ext/docker/base .`
 2. `docker build -t make-refapi -f ext/docker/build  .`
 3. `docker run -it --name builder make-dumpapi `
 4. `docker cp builder:/wheelhouse .`
 5. `docker rm builder`
 6. `docker build -t prod-refapi -f ext/docker/run .`
 7. `docker run -d -p 8081:8081 --name refapi -e DB_HOST=${DB_HOST} 
    -e DB_NAME=${DB_NAME} -e DB_USER=${DB_USER} -e DB_PASS=${DB_PASS} 
    dump-api-run`

### Ansible
see also https://github.com/eve-basil/deploy
 
Testing
-------
To run the tests, you will want to follow the guidance above under the
sections above to generate an environment with the `requirements.txt` contents
installed.

Additionally, the `test-requirements.txt` file lists the python packages
required to run the automated tests for this project. You should provide a
`eve.db` file in a subdirectory called `data` off the root of this repository
in order to make the tests pass. See also `ext/fetch-data.sh` for how and
where to get this file.

At this point you can run the tests with `py.test`
