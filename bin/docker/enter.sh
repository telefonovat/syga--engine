#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/../.."

container="$( docker ps --filter "ancestor=wiki/nprg045-engine" -q )"

if [ "$container" = '' ] ; then
  exit 1
fi

sudo docker exec -it "$container" /bin/bash
