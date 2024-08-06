#!/bin/sh

gunicorn --worker-class uvicorn.workers.UvicornWorker \
  --workers 2 \
  --bind 0.0.0.0:$ED_SERVER_PORT \
  english_daily.main:create_app

# Run the main container process
exec "$@"
