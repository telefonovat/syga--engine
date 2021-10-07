#!/bin/bash

# Root directory
cd "$( dirname "$( realpath "$0" )" )/.." || exit 1

# Main
./bin/dotenv-check-keys.sh || exit "$?"

exit 0
