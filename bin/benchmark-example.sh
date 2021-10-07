#!/bin/bash

# Root directory
cd "$( dirname "$( realpath "$0" )" )/.." || exit 1

# Constants
RUNS='20'

# Parameters
alg="$1"

echo "$alg" | grep '/' -q && {
  echo "Invalid symbols in example name"
  exit 1
}

# Variables
target="./examples/$alg.py"

# Main
if [ ! -f "$target" ] ; then
  echo "Example '$alg' does not exist"
  exit 1
fi

total='0'
for _ in $( seq 1 $RUNS ) ; do
  ./bin/run-example.sh "$alg"

  out="$( cat "./out/$alg.json" )"

  res="$( echo "$out" | jq -r .res )"
  err="$( echo "$out" | jq -r .err )"
  elapsed="$( echo "$out" | jq -r .elapsed | grep -Po '\d+\.\d{0,3}' | sed 's/\.//' | grep -Po '[1-9]\d*$' )"

  if [ "$res" = 'success' ] ; then
    printf " \033[1;32m✔\033[0m %s \033[0;90m%sms\033[0m\n" "$alg" "$elapsed"
  else
    printf " \033[1;31m%s\033[0m %s \n" "$res" "$alg"
    echo ""
    echo "$err"

    exit 1
  fi

  total=$((total + elapsed))
done

printf "\nAverage \033[0;90m%sms\033[0m\n" "$((total / RUNS))"
