#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/../.."

if [ "$1" = '' ] ; then
  port="5000"
else
  port="$1"
fi

docker run -p "$port:5000" -d wiki/aruna-engine
