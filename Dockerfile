FROM python:3.12-slim

RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    procps \
    libxrender1 \
    libxext6 \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    rdkit \
    pandas \
    requests \
    odfpy \
    umap-learn \
    tomli-w

# Pre-warm numba's JIT cache while the image layer is still writable.
# Without this, numba tries to write the cache at runtime into the
# read-only image layer and crashes.
RUN python -c "import umap"

COPY bin/ /usr/local/bin/
RUN chmod a+rx /usr/local/bin/*.py

WORKDIR /app
CMD ["reference.py", "--help"]