FROM debian:stretch-slim

RUN apt-get update && apt-get install -y python3-pip && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT [ "/bin/bash" ]
