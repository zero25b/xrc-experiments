# Following https://docs.dash.org/en/stable/docs/user/developers/insight.html
FROM ubuntu:latest
USER root
RUN apt update
RUN apt upgrade
RUN apt install -y npm build-essential libzmq3-dev wget
RUN cd ~ 
RUN wget https://github.com/dashpay/dash/releases/download/v18.1.0/dashcore-18.1.0-x86_64-linux-gnu.tar.gz
RUN tar -xvzf dashcore-18.1.0-x86_64-linux-gnu.tar.gz
RUN rm dashcore-18.1.0-x86_64-linux-gnu.tar.gz
RUN git clone https://github.com/dashevo/dashcore-node
RUN cd dashcore-node 
RUN npm install 
RUN ./bin/dashcore-node create mynode
RUN cd mynode
RUN ../bin/dashcore-node install @dashevo/insight-api
RUN ../bin/dashcore-node install @dashevo/insight-ui




