#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

if [ "$1" = '' ] ; then
  echo "Missing commit message. Aborting..."
  exit 1
fi

git add . || exit "$?"
git commit -m "$1" || exit "$?"
git push origin master || exit "$?"

exit 0
