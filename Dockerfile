# -----------------------------------------------------------------------
# BioXend — Docker image
# Base: python:3.10-slim + pip
#
# Build:
#   docker build -t bioxend:0.1.0 .
#
# Use with Nextflow:
#   nextflow run main.nf -profile docker --input ...
# -----------------------------------------------------------------------
FROM python:3.10-slim

RUN pip install --no-cache-dir \
    rdkit \
    pandas \
    requests \
    odfpy \
    tomli-w

COPY bin/ /usr/local/bin/
RUN chmod +x /usr/local/bin/*.py

WORKDIR /data
CMD ["reference.py", "--help"]