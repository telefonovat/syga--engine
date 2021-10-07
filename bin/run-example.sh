#!/bin/bash

# Root directory
cd "$( dirname "$( realpath "$0" )" )/.." || exit 1

# Constants
MAX_ATTEMPTS='60'
PORT='3103'

# Parameters
alg="$1"

echo "$alg" | grep '/' -q && {
  echo "Invalid symbols in example name"
  exit 1
}

# Variables
target="./examples/$alg.py"

# Main
if [ ! -f "$target" ] ; then
  echo "Example '$alg' does not exist"
  exit 1
fi

python3 src/main.py --port "$PORT" --debug > ./logs/flask.log 2>&1 &
flask_pid="$!"

for _ in $( seq 1 "$MAX_ATTEMPTS" ) ; do
  if [ "$( curl --silent -o /dev/null -w "%{http_code}" "http://localhost:$PORT/api/ping" )" == '200' ] ; then
    break
  else
    sleep 0.05
  fi
done

code="$( cat "$target" )"
input_json=$( jq -n --arg code "$code" --arg alg "$alg" '{code: $code, secret: "super-secret-password", uid: $alg}' | jq -c . )

curl --silent \
  --header "Content-Type: application/json" \
  --request 'POST' \
  --data "$input_json" \
  "http://localhost:$PORT/api/alg" > "./out/$alg.json"

exit_code="$?"

kill "$flask_pid"

exit "$exit_code"
