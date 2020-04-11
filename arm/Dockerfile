#!/bin/bash

# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:3.7-buster

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# install dependencies
# RUN apt-get --yes update
# RUN apt-get --yes install python-pip
RUN apt-get -y update
RUN apt-get -y upgrade
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# tell the port number the container should expose
EXPOSE 5000

# run the command
CMD ["python", "./app.py"]