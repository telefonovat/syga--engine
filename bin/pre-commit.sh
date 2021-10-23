#!/bin/bash

# Root directory
cd "$( dirname "$( realpath "$0" )" )/.." || exit 1

# Main
echo " > ./bin/lint.sh"
./bin/lint.sh || exit "$?"

echo " > python3 src/test.py"
python3 src/test.py || exit "$?"

echo " > ./bin/run-tests.sh"
./bin/run-tests.sh || exit "$?"

exit 0
