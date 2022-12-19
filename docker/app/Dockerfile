FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Create a user to avoid running containers as root in production
RUN addgroup --system web \
    && adduser --system --ingroup web web
# Install os-level dependencies (as root)
RUN apt-get update && apt-get install -y -q --no-install-recommends \
  # dependencies for building Python packages
  build-essential \
  # postgress client (psycopg2) dependencies
  libpq-dev \
  # cleaning up unused files to reduce the image size
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*
# Switch to the non-root user
USER web
# Create a directory for the source code and use it as base path
WORKDIR /home/web/code/
# Copy the python depencencies list for pip
COPY --chown=web:web ./requirements.txt requirements.txt
# Switch to the root user temporary, to grant execution permissions.
USER root
# Install python packages at system level
RUN python -m pip install --no-cache-dir -r requirements.txt
# Copy entrypoint script which waits for the db to be ready
COPY --chown=web:web ./docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
COPY --chown=web:web ./docker/start-celery-worker.sh /usr/local/bin/start-celery-worker.sh
USER web
# This script will run before every command executed in the container
ENTRYPOINT ["entrypoint.sh"]
