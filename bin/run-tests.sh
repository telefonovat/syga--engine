#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

python3 src/test.py || exit 1

echo ''
echo 'Running examples...'
echo ''

for example in $( find ./examples -name '*.py' ) ; do
  example=${example#.\/examples\/}
  example=${example%\.py}

  printf "$example -> "

  res="$( ./bin/run-example.sh "$example" | jq .res )"

  echo "$res"

  if [ "$?" != '0' ] ; then
    echo "Response code: $?. Aborting..."
    exit "$?"
  fi
done
