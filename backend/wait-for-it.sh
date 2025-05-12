#!/usr/bin/env bash

# Fonte original: https://github.com/vishnubob/wait-for-it

HOST="$1"
PORT="$2"
shift 2

echo "🕐 Esperando ${HOST}:${PORT} estar disponível..."

while ! nc -z "$HOST" "$PORT"; do
  sleep 1
done

echo "✅ ${HOST}:${PORT} está disponível. Iniciando aplicação..."
exec "$@"
