FROM debian:stretch-slim

RUN apt-get update && apt-get install -y netcat-openbsd

ENTRYPOINT [ "nc" ]
