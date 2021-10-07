#!/bin/bash

# Root directory
cd "$( dirname "$( realpath "$0" )" )/.." || exit 1

# Parameters
if [ "$1" = '' ] ; then
  echo "Missing commit message. Aborting..."
  exit 1
fi

# Main
git add . || exit "$?"
git commit -m "$1" || exit "$?"
git push origin master || exit "$?"

exit 0
