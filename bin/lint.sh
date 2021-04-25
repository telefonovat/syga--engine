#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

pylint \
  --output-format=text \
  $(find -not -path "./src/tests/*" -not -path "./.history/*" -type f -name "*.py" ! -path "**/.venv/**")
