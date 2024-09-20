FROM ubuntu:22.04

RUN rm -f /etc/apt/sources.list.d/arrow.list

RUN apt-get update && \
    apt-get install -y \
    curl \
    awscli \
    gdal-bin \
    postgresql-client && \
    apt-get clean

WORKDIR /pg_scripts

COPY ./postgres /pg_scripts

RUN chmod +x /pg_scripts/*.sh

ENTRYPOINT ["/bin/bash"]