#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

pylint \
  --disable=F0401 \
  --indent-string='  ' \
  'src'
