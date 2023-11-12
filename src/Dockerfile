FROM ubuntu:latest

RUN apt-get update
RUN apt-get install python3 python3-pip libpq-dev -y

RUN useradd -ms /bin/bash admin
USER admin

RUN pip3 install flask==3.0.0 psycopg2==2.9.9
RUN export PATH="/home/admin/.local/bin:$PATH"
COPY . /app

#RUN /home/admin/.local/bin/pdoc --output-dir=/var/log/ /app/routes.py
CMD /home/admin/.local/bin/pdoc --output-dir=/var/log/ /app/routes.py && python3 /app/main.py > /var/log/urlshortener.log 2>&1
