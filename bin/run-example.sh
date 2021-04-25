#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

alg="$1"

echo "$alg" | grep '/' -q && {
  echo "Invalid symbols in example name"
  exit 1
}

target="./examples/$alg.py"

if [ ! -f "$target" ] ; then
  echo "Example '$alg' does not exist"
  exit 1
fi

code="$( cat "$target" )"
input_json=$( jq -n --arg code "$code" --arg alg "$alg" '{code: $code, secret: "super-secret-password", uid: $alg}' | jq -c . )

echo "$input_json" | python3 ./src/main.py > "./out/$alg.json"

exit_code="$?"

cat "./out/$alg.json"

exit "$exit_code"
