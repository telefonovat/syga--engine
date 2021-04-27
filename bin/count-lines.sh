#!/bin/bash

cd "$( realpath "$(dirname "$0")" )/../"

total=0

for lang in 'py' 'sh' # specify the language suffixes
do
  count=$( find ./src ./examples ./bin -name "*.$lang" | xargs wc -l | tail -n 1 | grep -Po '\d+' )
  printf "$lang\t$count lines\n"
  total=$((total+count))
done

printf "\n"
printf "total\t$total lines\n"

exit 0
