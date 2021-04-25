#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/../src"

pylint \
  --output-format=text \
  $(find -not -path "./tests/*" -not -path "./__algs/*" -type f -name "*.py" ! -path "**/.venv/**")
