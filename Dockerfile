FROM ubuntu:16.04

 # system-related commands
RUN apt-get update && apt-get -y install build-essential curl python3 python3-pip libffi-dev

# install project dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# copy application-related source files
COPY src /tmp/src
COPY test /tmp/test
COPY master volume /tmp/