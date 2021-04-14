#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

py3clean .

ls logs/algs/ | grep -Po '\.log$' && rm logs/algs/*.log || echo "Logs already clear"
ls src/__algs/ | grep -Po '\.py$' && rm src/__algs/*.py || echo "Algs already clear"

printf '' > logs/debug.log
