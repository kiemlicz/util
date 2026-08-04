FROM debian:trixie

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl git jq bc bison flex libssl-dev make libc6-dev libncurses5-dev crossbuild-essential-arm64 dwarves debhelper rsync \
    fakeroot libelf-dev xz-utils ca-certificates &&\
    rm -rf /var/lib/apt/lists/*
