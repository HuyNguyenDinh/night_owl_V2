source ../venv/bin/activate
daphne -b 0.0.0.0 -p 8000 night_owl_market.asgi:application
