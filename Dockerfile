# -----------------------------------------------------------------------
# BioXend — Docker image
# Base: python:3.10-slim + pip
#
# Build (use version from versions/workflow.txt):
#   docker build -t bioxend:$(cat versions/workflow.txt) .
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