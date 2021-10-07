#!/bin/bash

# Root directory
cd "$( dirname "$( realpath "$0" )" )/.." || exit 1

# Main
if [ ! -f '.env' ] ; then
  echo "Missing .env"
  exit 1
fi

if [ ! -f '.envkeys' ] ; then
  echo "Missing .envkeys"
  exit 1
fi

while read -r key ; do
  if ! echo "$key" | grep -qPo '^#' ; then
    grep -q "^$key" < .env || {
      echo "Missing key $key"
      exit 1
    }
  fi
done < .envkeys

exit 0
