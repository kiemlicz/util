FROM debian:bookworm-slim

RUN apt-get update &&  \
    apt-get install -y iproute2 dnsutils netcat-openbsd iputils-ping iperf3 curl traceroute iptables tcpdump stress-ng sysstat vim gnupg2 apt-transport-https ca-certificates

RUN curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg &&\
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | tee /usr/share/keyrings/cloud.google.asc &&\
    echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /' | tee /etc/apt/sources.list.d/kubernetes.list &&\
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.asc] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list &&\
    apt-get update && apt-get install -y kubectl google-cloud-cli google-cloud-sdk-gke-gcloud-auth-plugin

RUN rm -rf /var/lib/apt/lists/*

ENTRYPOINT [ "/bin/bash" ]
