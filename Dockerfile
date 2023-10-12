# syntax=docker/dockerfile:1

FROM ubuntu:16.04
FROM python:3.11.1

WORKDIR /service
COPY . ./
EXPOSE 8080
ENTRYPOINT ["python3", "main.py"]