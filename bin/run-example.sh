#!/bin/bash

# Root directory
cd "$( dirname "$( realpath "$0" )" )/.." || exit 1

# Parameters
alg="$1"

echo "$alg" | grep '/' -q && {
  echo "Invalid symbols in example name"
  exit 1
}

# Main
target="./examples/$alg.py"

if [ ! -f "$target" ] ; then
  echo "Example '$alg' does not exist"
  exit 1
fi

jq -n --arg code "$( cat "$target" )" '{code: $code}' \
  | python3 src/main.py \
  > "./out/$alg.json" \
  2> "./logs/$alg.log"

exit "$?"
