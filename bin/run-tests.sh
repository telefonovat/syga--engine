#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

python3 src/test.py || exit 1

echo ''
echo 'Examples'
echo ''

for example in $( find ./examples -name '*.py' ) ; do
  example=${example#.\/examples\/}
  example=${example%\.py}

  printf " - $example\t"

  res="$( ./bin/run-example.sh "$example" | jq -r .res )"

  if [ "$res" = 'success' ] ; then
    printf "\033[1;32mOK\033[0m\n"
  else
    printf "\033[1;31m$res\033[0m\n"
    exit 1
  fi

  if [ "$?" != '0' ] ; then
    printf "\033[1;31mResponse code: $?\033[0m\n"
    exit "$?"
  fi
done

echo ''
printf "\033[1;32mALL TESTS PASSED\033[0m\n"
