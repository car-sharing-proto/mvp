# syntax=docker/dockerfile:1
FROM postgres:latest

COPY ./db/init.sql /docker-entrypoint-initdb.d/init.sql

FROM python:latest
WORKDIR /service
COPY . ./
RUN python3 -m venv venv
RUN . venv/bin/activate
RUN pip3 install -r requirements.txt
EXPOSE 4000
CMD ["python3", "main.py"]