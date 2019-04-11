FROM debian:stretch-slim

RUN apt-get update && apt-get install -y iproute2 dnsutils netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT [ "/bin/bash" ]
