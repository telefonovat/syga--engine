#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

pylint \
  --disable=F0401,E0001 \
  --indent-string='  ' \
  'src'
