FROM python:3.12-slim

RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    procps \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    rdkit \
    pandas \
    requests \
    odfpy \
    tomli-w

COPY bin/ /usr/local/bin/
RUN chmod a+rx /usr/local/bin/*.py

WORKDIR /app
CMD ["reference.py", "--help"]