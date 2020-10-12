FROM debian:buster-slim

ENV UDP_PORT="9999"

RUN apt-get update && apt-get install -y python3-minimal

COPY server.py /opt/

ENTRYPOINT [ "python3" ]
CMD [ "/opt/server.py" ]
