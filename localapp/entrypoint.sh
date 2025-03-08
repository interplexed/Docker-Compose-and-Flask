#!/bin/bash
set -e

echo "HOST: $DATABASE_HOST, USER: $DATABASE_USER, PASSWORD: $DATABASE_PW, DATABASE: $DATABASE_DB"
echo "URL: $DATABASE_URL"

# python /localapp/init_db.py

exec gunicorn --reload -b 0.0.0.0:5000  --pythonpath "/" "localapp.wsgi:app"
