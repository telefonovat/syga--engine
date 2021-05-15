#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/../.."

container="$( docker ps --filter "ancestor=wiki/syga" -q )"

if [ "$container" = '' ] ; then
  exit 1
fi

sudo docker exec -it "$container" /bin/bash
