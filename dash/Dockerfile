FROM ubuntu:latest
USER root
WORKDIR ./usr/src
RUN apt update & apt upgrade
RUN apt install npm build-essential libzmq3-dev nano wget
RUN cd ~  \
    & wget https://github.com/dashpay/dash/releases/download/v18.1.0/dashcore-18.1.0-x86_64-linux-gnu.tar.gz \
    & tar -xvzf dashcore-18.1.0-x86_64-linux-gnu.tar.gz  \
    & rm dashcore-18.1.0-x86_64-linux-gnu.tar.gz
RUN git clone https://github.com/dashevo/dashcore-node
RUN cd dashcore-node & npm install & ./bin/dashcore-node create mynode
RUN cd mynode & ../bin/dashcore-node install @dashevo/insight-api & ../bin/dashcore-node install @dashevo/insight-ui




