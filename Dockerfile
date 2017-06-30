FROM phusion/baseimage

MAINTAINER Dimi Balaouras <dimi@stek.io>

# Update packages
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install --upgrade pip

# Create install directories
RUN mkdir -p /opt/azure-storage-backup
WORKDIR /opt/azure-storage-backup

# Pepare Logging directory
RUN mkdir -p /var/log/azure-storage-backup

# Add src
ADD app app
ADD config config
ADD requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
ENV PYTHONPATH "$PYTHONPATH:/opt/azure-storage-backup/app"
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8