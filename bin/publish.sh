#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

# This is just a temporary way to run the REST API
ssh syga "\
  cd /srv/syga-engine && \
  git pull origin master && \
  ./bin/docker/kill.sh && \
  ./bin/docker/build.sh && \
  ./bin/docker/run.sh | timeout 5s xargs docker logs -f "
