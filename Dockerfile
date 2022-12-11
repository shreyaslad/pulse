FROM ubuntu:latest

RUN apt update && apt upgrade -y

# Install Java 17 in the container
RUN apt install -y \
    software-properties-common \
    ca-certificates \
    apt-transport-https \
    curl
RUN curl https://apt.corretto.aws/corretto.key | apt-key add -
RUN add-apt-repository 'deb https://apt.corretto.aws stable main'
RUN apt update \
    && apt install -y java-17-amazon-corretto-jdk

# This Dockerfile is meant to already exist with your server files
ADD . /server
WORKDIR /server

# NOTE: Specifically runs a 1.19.2 PaperMC Minecraft
# Server. Change as needed
CMD java -Xmx5G -Xms5G -jar paper-1.19.2-307.jar