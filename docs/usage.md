## Usage

### Requirements

- [Java](https://sdkman.io/) >= 17
- [Nextflow](https://www.nextflow.io/) >= 22.10.0
- [Docker](https://www.docker.com/products/docker-desktop/)

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

### Run

```bash
nextflow run zmahnoor14/BioXend -latest -profile docker \
  --input  path/to/Template_open.ods \
  --prefix HMDM \
  --xenobiotic_class drug
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--input` | yes | Path to your filled `Template_open.ods` |
| `--prefix` | yes | Short prefix for compound IDs (e.g. `HMDM`) |
| `--xenobiotic_class` | yes | Class of compound (e.g. `drug`, `pesticide`) |
| `--outdir` | no | Output directory (default: `./results`) |
| `--strict` | no | Exit on validation warnings (default: `false`) |

An example template is at `Standards/Templates/Template_open.ods`.

---

### HPC (Singularity)

```bash
singularity pull bioxend.sif docker://zmahnoor/bioxend:latest

nextflow run zmahnoor14/BioXend \
  -with-singularity bioxend.sif \
  --input  path/to/Template_open.ods \
  --prefix HMDM \
  --xenobiotic_class drug
```

---

### Outputs

See [output.md](output.md) for a description of all generated files.
