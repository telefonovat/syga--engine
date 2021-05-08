#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/../.."

docker build -t wiki/nprg045-engine . "$@"
