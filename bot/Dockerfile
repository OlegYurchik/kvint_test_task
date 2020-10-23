FROM python:slim-stretch

WORKDIR /home/bot

COPY . /home/bot

RUN apt update -y
RUN apt install -y git
RUN pip3 install -r requirements.txt
