FROM debian:trixie

ENV DEBIAN_FRONTEND=noninteractive

RUN dpkg --add-architecture arm64 && \
    apt-get update && apt-get install -y \
    curl git jq bc bison flex libssl-dev make libc6-dev libncurses5-dev crossbuild-essential-arm64 dwarves debhelper rsync \
    fakeroot libelf-dev xz-utils ca-certificates lsb-release kmod python3 libdw-dev libssl-dev:arm64 libelf-dev:arm64 &&\
    rm -rf /var/lib/apt/lists/*
