#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

ssh phillip "\
  cd /srv/nprg045-engine && \
  git pull origin master && \
  ./bin/docker/kill.sh && \
  ./bin/docker/build.sh && \
  ./bin/docker/run.sh | timeout 5s xargs docker logs -f "
