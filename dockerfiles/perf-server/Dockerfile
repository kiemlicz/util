FROM python:3.12-bookworm

RUN pip3 install prometheus-client~=0.21.1

COPY *.py /opt/
WORKDIR /opt

ENTRYPOINT [ "python3" ]
CMD [ "/opt/server.py" ]
