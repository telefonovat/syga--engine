#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

for example in $( find ./examples -name '*.py' ) ; do
  example=${example#.\/examples\/}
  example=${example%\.py}

  printf " - $example "

  out="$( ./bin/run-example.sh "$example" )"
  res="$( echo "$out" | jq -r .res )"
  err="$( echo "$out" | jq -r .err )"

  if [ "$res" = 'success' ] ; then
    printf "\033[1;32mOK\033[0m\n"
  else
    printf "\033[1;31m$res\033[0m\n"
    echo ""
    echo "$err"

    exit 1
  fi

  if [ "$?" != '0' ] ; then
    printf "\033[1;31mResponse code: $?\033[0m\n"

    exit "$?"
  fi
done

echo ''
printf "\033[1;32mALL TESTS PASSED\033[0m\n"

exit 0
