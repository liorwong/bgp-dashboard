FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y bgpdump
RUN apt-get install -y wget
# COPY ./requirements.txt /tmp/requirements.txt

RUN wget https://bgp.cgtf.net/ribs/rib.latest.bz2
RUN bgpdump -m rib.latest.bz2 | /var/tmp/bgpdump_to_mongo.py