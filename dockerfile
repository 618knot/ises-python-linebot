FROM python:3.9-slim-buster
USER root
WORKDIR /app
COPY ./ .
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir uvicorn