## Usage

### Requirements

- [Java](https://sdkman.io/) >= 17
- [Nextflow](https://www.nextflow.io/) >= 22.10.0
- One of: [Docker](https://www.docker.com/products/docker-desktop/), [Singularity](https://docs.sylabs.io/guides/latest/user-guide/), or [Apptainer](https://apptainer.org/)

---

### Installation

```bash
# Java (if not already installed)
curl -s "https://get.sdkman.io" | bash
sdk install java

# Nextflow
curl -s https://get.nextflow.io | bash
chmod +x nextflow && mv nextflow $HOME/.local/bin/
```

---

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--input` | yes | Path to your filled `Template_open.ods` |
| `--prefix` | yes | Short prefix for compound IDs (e.g. `HMDM`) |
| `--xenobiotic_class` | yes | Class of compound (e.g. `drug`, `pesticide`) |
| `--outdir` | no | Output directory (default: `./results`) |
| `--strict` | no | Exit on validation warnings (default: `false`) |

An example template is at `exampledata/Template_filled.ods`.

---

### Run with Docker (local / laptop)

Docker Desktop must be running. Build the image once:

```bash
docker build -t zmahnoor/bioxend:latest .
```

Then run the pipeline:

```bash
nextflow run main.nf -profile docker \
  --input  exampledata/Template_filled.ods \
  --prefix HMDM \
  --xenobiotic_class drug
```

Or run directly from GitHub (uses the `main` branch):

```bash
nextflow run zmahnoor14/BioXend -r main \
  --input  path/to/template_filled.ods \
  --prefix HMDM \
  --xenobiotic_class drug
```

---

### Running from a network-mounted volume (NFS / SMB)

Nextflow's cache database requires file-locking support. Network mounts (e.g. `/Volumes/...` on macOS) do not support this. If your project lives on a network volume, redirect both the cache and work directories to a local path:

```bash
NXF_CACHE_DIR=/tmp/nextflow_cache \
nextflow run /full/path/to/main.nf \
  -profile docker \
  -w /tmp/nextflow_work \
  --input  /full/path/to/exampledata/Template_filled.ods \
  --prefix HMDM \
  --xenobiotic_class drug \
  --outdir /full/path/to/results
```

`--outdir` can still point back to the network volume — only the cache and intermediate work files need to be local.

---

### Run with Singularity (HPC)

Singularity pulls the Docker image from Docker Hub automatically. No manual image build needed.

```bash
nextflow run main.nf -profile singularity \
  --input  path/to/template_filled.ods \
  --prefix HMDM \
  --xenobiotic_class drug
```

To run on a SLURM cluster, combine profiles:

```bash
nextflow run main.nf -profile singularity,slurm \
  --input  path/to/template_filled.ods \
  --prefix HMDM \
  --xenobiotic_class drug
```
---