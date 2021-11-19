#!/bin/bash

# Root directory
cd "$( dirname "$( realpath "$0" )" )/.." || exit 1

# Script settings
shopt -s nullglob

# Main
py3clean .

for file in ./logs/*.log ./src/__algs/*.py ./out/*.json ; do
  rm "$file"
done

exit 0
