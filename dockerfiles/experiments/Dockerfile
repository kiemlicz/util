FROM python:3-slim-buster

ENV TCP_PORT="8080"

RUN pip3 install flask==2.1.1 flask-api==3.0.post1 kubernetes==23.3.0

COPY web.py /opt/
WORKDIR /opt

ENTRYPOINT [ "python3" ]
CMD [ "/opt/web.py" ]
