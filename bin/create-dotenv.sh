#!/bin/bash

cd "$( dirname "$( realpath "$0" )" )/../src"

echo '
SECRET_PASSWORD="super-secret-password"
' > .env
