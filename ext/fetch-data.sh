#!/bin/bash
set -ev
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ ! -d "${DIR}/../data" ];then
    mkdir ${DIR}/../data
fi

pushd ${DIR}/../data
  if [ ! -f "eve.db" ]; then
    wget https://www.fuzzysteve.co.uk/dump/latest/eve.db.bz2 --no-check-certificate -q
    bunzip2 eve.db.bz2
  fi
  if [ ! -f "blueprints.yaml" ]; then
    wget https://www.fuzzysteve.co.uk/dump/latest/blueprints.yaml.bz2 --no-check-certificate -q
    bunzip2 blueprints.yaml.bz2
  fi
popd
