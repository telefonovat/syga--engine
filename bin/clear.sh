#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

py3clean .

rm logs/algs/*.log || echo "Logs already clear"
rm src/__algs/*.py || echo "Algs already clear"

printf '' > logs/debug.log
