#!/bin/bash

# Root directory
cd "$( dirname "$( realpath "$0" )" )/.." || exit 1

# Variables
total=0

# Main
for lang in 'py' 'sh' # specify the language suffixes
do
  lines="$( find ./src ./examples ./bin -name "*.$lang" -exec wc -l {} + )"
  count="$( echo "$lines" | tail -n 1 | grep -Po '\d+' )"

  printf "%s\t%d lines\n" "$lang" "$count"

  total=$((total+count))
done

printf "\n"
printf "total\t%d lines\n" "$total"

exit 0
