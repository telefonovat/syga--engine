#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/.."

./bin/dotenv-check-keys.sh || exit "$?"
