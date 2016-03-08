#!/bin/bash
set -ev
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

mkdir ${DIR}/../data

pushd ${DIR}/../data
  wget https://www.fuzzysteve.co.uk/dump/latest/eve.db.bz2 --no-check-certificate -q
  bunzip2 eve.db.bz2

  wget https://www.fuzzysteve.co.uk/dump/latest/blueprints.yaml.bz2 --no-check-certificate -q
  bunzip2 blueprints.yaml.bz2
popd
