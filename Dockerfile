FROM python:3.7.3-slim

RUN mkdir -p /app
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./src /app
RUN mkdir -p /tmp/output
