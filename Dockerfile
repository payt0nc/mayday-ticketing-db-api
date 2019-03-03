FROM ubuntu:18.04
MAINTAINER payton@cooomma.info

RUN apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa

RUN apt-get install -y --no-install-recommends libssl-dev libmysqlclient-dev python3.7 \
    && apt-get install -y python3-pip \
    && pip3 install --upgrade pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY . /app
RUN pip install --no-cache-dir -r /app/requirements.txt
WORKDIR /app
ENTRYPOINT python3 /app/app.py
