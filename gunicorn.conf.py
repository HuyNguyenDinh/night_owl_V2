import multiprocessing

command = "/home/dinhhuy2005/Source/Python/venv/bin/gunicorn"
pythonpath = "/home/dinhhuy2005/Source/Python/night_owl_V2"
bind = "127.0.0.1:8001"
workers = multiprocessing.cpu_count() * 2 + 1
log_file = "/tmp/gunicorn.log"
raw_env = ["DB_HOST=127.0.0.1", "DB_PORT=5432", "DB_NAME=night_owl", "DB_USER=postgres", "DB_PASSWORD=postgres"]
daemon = True
pidfile = '/tmp/night_owl_gunicorn_pid.pid'
