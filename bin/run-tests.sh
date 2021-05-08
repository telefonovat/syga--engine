#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

for example in $( find ./examples -name '*.py' ) ; do
  example=${example#.\/examples\/}
  example=${example%\.py}

  ./bin/run-example.sh "$example"
  out="$( cat "./out/$example.json" )"

  res="$( echo "$out" | jq -r .res )"
  err="$( echo "$out" | jq -r .err )"
  elapsed="$( echo "$out" | jq -r .elapsed | grep -Po '\d+\.\d{0,3}' | sed 's/\.//' | grep -Po '[1-9]\d*$' )ms"

  if [ "$res" = 'success' ] ; then
    printf " \033[1;32m✔\033[0m $example \033[0;90m$elapsed\033[0m\n"
  else
    printf " \033[1;31m$res\033[0m $example \n"
    echo ""
    echo "$err"

    exit 1
  fi

  if [ "$?" != '0' ] ; then
    printf "\033[1;31mResponse code: $?\033[0m\n"

    exit "$?"
  fi
done

exit 0
