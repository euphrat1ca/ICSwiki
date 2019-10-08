FROM python:3.7.4-alpine3.10
LABEL maintainer="Fabian Affolter <fabian@affolter-engineering.ch>"
LABEL version="0.6.0"
LABEL description="Expliot - Internet Of Things Security Testing and \
Exploitation Framework"

ENV LANG C.UTF-8

RUN apk add --no-cache \
        make \
        python3 \
        git \
        glib-dev \
        gcc \
        libstdc++ \
        g++ \
        python3-dev

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

ADD . /usr/src/app

RUN python3 setup.py install

ENTRYPOINT expliot
