FROM debian:testing
RUN apt update && apt install -y git bpfcc-tools bpfcc-tools python3-bpfcc arping bison clang-format cmake dh-python \
    dpkg-dev pkg-kde-tools ethtool flex inetutils-ping iperf libbpf-dev libclang-dev libclang-cpp-dev libedit-dev libelf-dev \
    libfl-dev libzip-dev linux-libc-dev llvm-dev libluajit-5.1-dev luajit python3-netaddr python3-pyroute2 python3-distutils python3 &&\
    ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /opt

RUN git clone https://github.com/iovisor/bcc.git &&\
    mkdir bcc/build; cd bcc/build && cmake .. && make && make install
