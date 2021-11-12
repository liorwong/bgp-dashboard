FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y bgpdump
RUN apt-get install -y python3.7
RUN apt-get install -y python3-pip
RUN apt-get install -y wget
COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

RUN wget https://bgp.cgtf.net/ribs/rib.latest.bz2
RUN mkdir /root/bgpdump
RUN mv rib.latest.bz2 /root/bgpdump/rib.latest.bz2
COPY ./entrypoint.sh /root/bgpdump/entrypoint.sh
COPY ./startup.sh /root/bgpdump/startup.sh
RUN chmod +x /root/bgpdump/entrypoint.sh
RUN chmod +x /root/bgpdump/startup.sh
ENTRYPOINT /root/bgpdump/entrypoint.sh