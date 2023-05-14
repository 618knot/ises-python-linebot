FROM python:3.9
USER root
WORKDIR /app
COPY requirements.txt /app/
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app/ /app

RUN pip install --no-cache-dir uvicorn