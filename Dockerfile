FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN \
  apt-get -y update && \
  mkdir /srv/app

ADD . /srv/app

WORKDIR /srv/app

RUN \
  pip install --upgrade pip && \
  pip install -r requirements.txt
