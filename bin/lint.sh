#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/../src"

python3 -m pylint \
  --output-format=text \
  $(find -not -path "./__algs/*" -type f -name "*.py" ! -path "**/.venv/**")
