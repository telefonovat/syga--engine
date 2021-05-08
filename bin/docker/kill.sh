#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/../.."

containers="$( docker ps --filter "ancestor=wiki/nprg045-engine" -q )"

if [ "$containers" != '' ] ; then
  echo "$containers" | xargs docker kill
fi
