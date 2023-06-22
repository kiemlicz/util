FROM debian:bookworm-slim

RUN apt-get update &&  \
    apt-get install -y iproute2 dnsutils netcat-openbsd iputils-ping iperf3 curl traceroute iptables tcpdump && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT [ "/bin/bash" ]
