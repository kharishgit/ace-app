FROM ubuntu
#FROM python:3.8-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Install dependencies required for psycopg2 python package
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc \
    python3-pip python3-psycopg2 curl nano nginx supervisor
RUN pip3 install --upgrade pip
RUN python3 -m pip install --upgrade setuptools
RUN mkdir -p /ace
WORKDIR /ace
COPY ./aceappsite.conf /etc/nginx/sites-enabled/default
COPY ./ /ace/
COPY .env /ace/.env
RUN mkdir -p logs
RUN pip3 install -r requirements.txt
