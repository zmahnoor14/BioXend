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

An example template is at `exampledata/template_filled.ods`.

---

### Run with Docker (local / laptop)

Docker Desktop must be running. Build the image once:

```bash
docker build -t zmahnoor/bioxend:latest .
```

Then run the pipeline — Docker is enabled by default, no profile flag needed:

```bash
nextflow run main.nf \
  --input  path/to/template_filled.ods \
  --prefix HMDM \
  --xenobiotic_class drug
```

Or run directly from GitHub (uses the `devel` branch):

```bash
nextflow run zmahnoor14/BioXend -r devel \
  --input  path/to/template_filled.ods \
  --prefix HMDM \
  --xenobiotic_class drug
```

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

### Run with Apptainer (HPC)

Apptainer is a drop-in replacement for Singularity on newer HPC systems. Use the same `singularity` profile — Nextflow handles Apptainer transparently:

```bash
nextflow run main.nf -profile singularity \
  --input  path/to/template_filled.ods \
  --prefix HMDM \
  --xenobiotic_class drug
```

If your HPC requires pulling the image manually first:

```bash
apptainer pull bioxend.sif docker://zmahnoor/bioxend:latest

nextflow run main.nf -profile singularity \
  -with-singularity bioxend.sif \
  --input  path/to/template_filled.ods \
  --prefix HMDM \
  --xenobiotic_class drug
```

---

### Outputs

See [output.md](output.md) for a description of all generated files.
