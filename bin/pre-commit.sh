#!/bin/bash

# Root directory
cd "$( dirname "$( realpath "$0" )" )/.." || exit 1

# Main
echo " > ./bin/clear.sh"
./bin/clear.sh || exit "$?"

echo " > ./bin/lint.sh"
./bin/lint.sh || exit "$?"

echo " > ./bin/clear.sh && python3 src/test.py 2> ./logs/test.log"
./bin/clear.sh && python3 src/test.py 2> ./logs/test.log || exit "$?"

echo " > ./bin/clear.sh && ./bin/run-tests.sh"
./bin/clear.sh && ./bin/run-tests.sh || exit "$?"

echo " > ./bin/clear.sh"
./bin/clear.sh || exit "$?"

exit 0
