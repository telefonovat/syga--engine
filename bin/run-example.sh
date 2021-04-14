#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

echo "$1" | grep '/' -q && {
  echo "Invalid symbols in example name"
  exit 1
}

target="./examples/$1.py"

if [ ! -f "$target" ] ; then
  echo "Example '$1' does not exist"
  exit 1
fi

code="$( cat "$target" )"

input_json=$( jq -n --arg code "$code" '{code: $code}' | jq -c . )

echo "$input_json" | python3 ./src/main.py
