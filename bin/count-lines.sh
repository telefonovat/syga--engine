#!/bin/bash

root="$( realpath "$(dirname "$0")" )/../src"

total=0

for lang in 'py' # specify the language suffixes
do
  count=$( find "$root" -name "*.$lang" | xargs wc -l | tail -n 1 | grep -Po '\d+' )
  printf "$lang\t$count lines\n"
  total=$((total+count))
done

printf "\n"
printf "total\t$total lines\n"
