#!/bin/bash

# Root directory
cd "$( dirname "$( realpath "$0" )" )/.." || exit 1

# Main
if [ ! -f '.envkeys' ] ; then
  touch .envkeys
fi

cp .envkeys temp/.envkeys.copy

printf '# This file contains keys which MUST be present in .env\n' > .envkeys
printf '# This file auto generated in bin/dotenv-copy-keys.sh\n\n' >> .envkeys

grep -Po '^.+?=' < .env >> .envkeys

diff .envkeys temp/.envkeys.copy > /dev/null 2>&1

diff_exit_code="$?"

rm temp/.envkeys.copy

exit "$diff_exit_code"
