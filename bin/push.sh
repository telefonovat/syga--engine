#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

if [ "$1" = '' ] ; then
  echo "Missing commit message. Aborting..."
  exit 1
fi

git add .
git commit -m "$1"
git push origin master

exit 0
