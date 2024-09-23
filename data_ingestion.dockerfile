FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    bash \
    curl \
    awscli \
    gdal-bin \
    postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /pg_scripts

COPY ./postgres /pg_scripts

RUN chmod +x /pg_scripts/*.sh

ENTRYPOINT ["/bin/bash"]