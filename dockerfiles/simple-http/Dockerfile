FROM python:3-slim-buster

ENV TCP_PORT="8080"

RUN pip3 install flask==1.1.2 flask-api==2.0

COPY web.py /opt/
WORKDIR /opt

ENTRYPOINT [ "python3" ]
CMD [ "/opt/web.py" ]
