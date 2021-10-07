#!/bin/bash

# Root directory
cd "$( dirname "$( realpath "$0" )" )/.." || exit 1

# Main
find ./src -not -path "./src/__algs/*" -type f -name "*.py" ! -path "**/.venv/**" -exec python3 -m pylint --output-format=text {} + || exit "$?"

find ./bin/ -name '*.sh' -exec shellcheck {} + || exit "$?"

exit 0
