
FROM ubuntu:18.04

WORKDIR /opt
COPY . /opt

USER root

RUN apt-get update
RUN apt-get install -y python3.6-dev \
                       python3-pip \
                       wget \
                       gdal-bin \
                       libgdal-dev \
                       libspatialindex-dev \
                       build-essential \
                       software-properties-common \
                       apt-utils \
                       libgl1-mesa-glx

RUN apt-get update
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3", "/opt/3d_pcd_to_mesh.py" ]
