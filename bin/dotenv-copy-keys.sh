#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

if [ ! -f '.envkeys' ] ; then
  touch .envkeys
fi

cp .envkeys temp/.envkeys.copy

echo '# This file contains keys which MUST be present in .env' > .envkeys
echo '# This file auto generated in bin/dotenv-copy-keys.sh' >> .envkeys
echo '' >> .envkeys

cat .env | grep -Po '^.+?=' >> .envkeys

diff .envkeys temp/.envkeys.copy > /dev/null 2>&1

diff_exit_code="$?"

rm temp/.envkeys.copy

exit "$diff_exit_code"
