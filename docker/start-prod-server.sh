#!/bin/sh
echo "Running migrations.."
python manage.py migrate
echo "Starting server.."
daphne -b 0.0.0.0 -p 8000 night_owl_market.asgi:application