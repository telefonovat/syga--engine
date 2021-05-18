#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

py3clean .

ls ./logs/algs/ | grep -qPo '\.log$' && rm ./logs/algs/*.log
ls ./src/__algs/ | grep -qPo '\.py$' && rm ./src/__algs/*.py
ls ./out/ | grep -qPo '\.json$' && rm ./out/*.json

printf '' > logs/debug.log

exit 0
