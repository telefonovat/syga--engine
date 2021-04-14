#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

py3clean .

ls logs/algs/ | grep -qPo '\.log$' && rm logs/algs/*.log
ls src/__algs/ | grep -qPo '\.py$' && rm src/__algs/*.py

printf '' > logs/debug.log
