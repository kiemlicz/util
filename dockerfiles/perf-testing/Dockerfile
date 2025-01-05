FROM python:3.12-bookworm

RUN apt-get update && apt-get install -y iproute2
RUN pip3 install prometheus-client~=0.21.1 uvloop~=0.21.0 asyncudp~=0.11.0

COPY *.py /opt/
WORKDIR /opt

ENTRYPOINT [ "python3" ]
CMD [ "/opt/server.py" ]
