FROM ubuntu:18.04
MAINTAINER payton@cooomma.info

RUN apt-get update -y  && apt-get install -y libssl-dev libmysqlclient-dev python3-dev 
RUN apt-get install -y python3-pip && pip3 install --upgrade pip
COPY . /app
RUN pip install -r /app/requirements.txt
WORKDIR /app
ENTRYPOINT python3 /app/app.py
