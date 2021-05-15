#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

RUNS='20'

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

total='0'
for i in $( seq 1 $RUNS ) ; do
  ./bin/run-example.sh "$alg"

  out="$( cat "./out/$alg.json" )"

  res="$( echo "$out" | jq -r .res )"
  err="$( echo "$out" | jq -r .err )"
  elapsed="$( echo "$out" | jq -r .elapsed | grep -Po '\d+\.\d{0,3}' | sed 's/\.//' | grep -Po '[1-9]\d*$' )"

  if [ "$res" = 'success' ] ; then
    printf " \033[1;32m✔\033[0m $alg \033[0;90m${elapsed}ms\033[0m\n"
  else
    printf " \033[1;31m$res\033[0m $alg \n"
    echo ""
    echo "$err"

    exit 1
  fi

  total=$((total + elapsed))
done

printf "\nAverage \033[0;90m$((total / RUNS))ms\033[0m\n"
