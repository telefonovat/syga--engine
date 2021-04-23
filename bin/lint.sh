#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

pylint \
  --indent-string='  ' \
  'src'
