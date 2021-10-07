#!/bin/bash

# Root directory
cd "$( dirname "$( realpath "$0" )" )/.." || exit 1

# Main
echo '
SECRET_PASSWORD="super-secret-password"
API_BASE="/api"
DEBUG_MODE="yes"
' > ./src/.env

exit 0
