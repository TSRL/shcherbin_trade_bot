FROM python:3.9.6-slim

RUN mkdir /app
WORKDIR /app

COPY ./trade_bot /app

RUN apt-get update
RUN ACCEPT_EULA=y apt-get install -y gcc libpq-dev libssl-dev g++
RUN pip install psycopg2
RUN pip install flake8

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN useradd django

USER django

EXPOSE 8989