#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/../.."

containers="$( docker ps --filter "ancestor=wiki/syga" -q )"

if [ "$containers" != '' ] ; then
  echo "$containers" | xargs docker kill
fi
