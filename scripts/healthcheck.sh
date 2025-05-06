#!/bin/sh
# Healthcheck script for SQLoslav

set -e

HOST=${HOST:-"localhost"}
PORT=${PORT:-"5000"}
TIMEOUT=${TIMEOUT:-"5"}

echo "Checking SQLoslav health at http://$HOST:$PORT..."

if command -v curl > /dev/null 2>&1; then
  response=$(curl -s -o /dev/null -w "%{http_code}" --max-time $TIMEOUT http://$HOST:$PORT/)
elif command -v wget > /dev/null 2>&1; then
  response=$(wget -q -O /dev/null --timeout=$TIMEOUT --server-response http://$HOST:$PORT/ 2>&1 | awk '/^  HTTP/{print $2}' | tail -n 1)
else
  echo "Neither curl nor wget found. Cannot perform health check."
  exit 1
fi

if [ "$response" = "200" ]; then
  echo "SQLoslav is healthy (HTTP 200 OK)"
  exit 0
else
  echo "SQLoslav is not healthy (HTTP $response)"
  exit 1
fi 