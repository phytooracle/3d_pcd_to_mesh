
FROM ubuntu:18.04

WORKDIR /opt
COPY . /opt

USER root

RUN apt-get update
RUN apt-get install -y wget \
                       build-essential \
                       software-properties-common \
                       apt-utils \
                       libgl1-mesa-glx

RUN wget https://www.python.org/ftp/python/3.8.5/Python-3.8.5.tgz
RUN tar -xzf Python-3.8.5.tgz
RUN cd Python-3.8.5/ && ./configure && make && make install
RUN apt-get install -y python3-pip
RUN apt-get update
RUN pip3 install -r requirements.txt
RUN apt-get install -y locales && locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'

ENTRYPOINT [ "python3", "/opt/3d_pcd_to_mesh.py" ]
