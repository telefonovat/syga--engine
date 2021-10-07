#!/bin/bash

# Root directory
cd "$( dirname "$( realpath "$0" )" )/.." || exit 1

# Script settings
shopt -s nullglob

# Main
for example in ./examples/*.py ; do
  example=${example#.\/examples\/}
  example=${example%\.py}

  ./bin/run-example.sh "$example" || exit "$?"
  out="$( cat "./out/$example.json" || exit "$?" )"

  res="$( echo "$out" | jq -r .res || exit "$?" )"
  err="$( echo "$out" | jq -r .err || exit "$?" )"
  elapsed="$( echo "$out" | jq -r .elapsed | grep -Po '\d+\.\d{0,3}' | sed 's/\.//' | grep -Po '[1-9]\d*$' || exit "$?" )ms"

  if [ "$res" = 'success' ] ; then
    printf " \033[1;32m✔\033[0m %s \033[0;90m%s\033[0m\n" "$example" "$elapsed"
  else
    printf " \033[1;31m%s\033[0m %s \n" "$res" "$example"
    echo ""
    echo "$err"

    exit 1
  fi
done

exit 0
