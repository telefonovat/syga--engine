#!/bin/bash

# This is just a temporary way to run the REST API

cd "$( dirname "$( realpath "$0" )" )/.."

# MFF VPS
ssh syga "\
  cd /srv/syga-engine && \
  git pull origin master && \
  ./bin/pre-start.sh && \
  ./bin/docker/kill.sh && \
  ./bin/docker/build.sh && \
  ./bin/docker/run.sh | timeout 5s xargs docker logs -f "
