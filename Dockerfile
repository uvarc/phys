FROM python:3.7.8-slim-buster
LABEL maintainer="UVA Research Computing <uvarc@virginia.edu>"

RUN apt-get update && apt-get install -y --no-install-recommends \
        nginx && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uwsgi

ARG APP=femtographer
WORKDIR /$APP
COPY . /$APP
COPY nginx.conf /etc/nginx/sites-enabled/default

RUN pip install --no-cache-dir -r requirements.txt

CMD service nginx start && uwsgi -s /tmp/uwsgi.sock --chmod-socket=666 --manage-script-name --mount /=$APP:$APP
