#!/bin/bash

# Root directory
cd "$( dirname "$( realpath "$0" )" )/.." || exit 1

# Main
python3 -m pylint \
  --output-format=text \
  $(find ./src -not -path "./src/__algs/*" -type f -name "*.py" ! -path "**/.venv/**") || exit "$?"

# find ./bin/ -name '*.sh' | xargs shellcheck || exit "$?"

exit 0
