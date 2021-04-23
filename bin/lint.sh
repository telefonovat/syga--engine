#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

pylint \
  --disable=C0303,F0401 \
  --indent-string='  ' \
  'src'
