FROM ubuntu:latest

RUN apt-get update
RUN apt-get install python3 python3-pip libpq-dev -y

RUN useradd -ms /bin/bash admin
USER admin

RUN pip3 install flask psycopg2
COPY . /app

CMD python3 /app/main.py > /var/log/urlshortener.log 2>&1
