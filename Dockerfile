FROM python:3.7.9-alpine3.12

COPY . /app/

WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt
#RUN cp config/config.py.example config/config.py
