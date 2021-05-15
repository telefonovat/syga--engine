#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

if [ ! -f '.env' ] ; then
  echo "Missing .env"
  exit 1
fi

if [ ! -f '.envkeys' ] ; then
  echo "Missing .envkeys"
  exit 1
fi

for key in $( cat .envkeys | grep -Po '^.+?=$' ) ; do
  cat .env | grep -q "^$key" || {
    echo "Missing key $key"
    exit 1
  }
done

exit 0
