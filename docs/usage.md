## Usage

### Prerequisites

- [Nextflow](https://www.nextflow.io/) >= 22.10.0
- [Docker](https://www.docker.com/) 

---

### Quickstart

```bash
nextflow run main.nf -profile docker \
  --input  path/to/Template_open.ods \
  --outdir results/
```

---

### Input

The pipeline takes a single input: a filled-out `Template_open.ods` MIX-MB submission template.

```
--input  path/to/Template_open.ods
```

The template has five sheets that the pipeline reads:

| Sheet | Used by |
|-------|---------|
| Reference | GENERATE_REFERENCE |
| Chemicals | GENERATE_CHEMICALS |
| Microbes | GENERATE_ASSAY |
| Experiment | GENERATE_ASSAY_PARAM, GENERATE_ACTIVITY |
| Biotransformation | GENERATE_ACTIVITY |

An example template is provided at `Standards/Templates/Template_open.ods`.

---

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--input` | required | Path to filled `Template_open.ods` |
| `--outdir` | `./results` | Directory where output files are written |
| `--prefix` | `HMDM` | Prefix for auto-generated compound IDs (e.g. `HMDM0001`, where HMDM is based on the user RIDX `HumanMicrobiomeDrugMetabolism`) |
| `--xenobiotic_class` | `xenobiotic compound` | Class name (singular form) used in assay descriptions (e.g. `drug`, `pesticide`) |
| `--strict` | `false` | Exit with error on any validation warning |

---

### Profiles

Run with `-profile <name>` to select the execution environment:

| Profile | Description |
|---------|-------------|
| `docker` | Run processes inside the `bioxend:0.1.0` Docker container (recommended) |
| `singularity` | Use Singularity instead of Docker (for HPC environments) |
| `slurm` | Submit jobs to a SLURM cluster |

**Build the Docker image before first use:**

```bash
docker build -t bioxend:0.1.0 .
```

---

### Examples

**Minimal run:**
```bash
nextflow run main.nf -profile docker \
  --input Standards/Templates/Template_open.ods
```

**Custom output directory and compound prefix:**
```bash
nextflow run main.nf -profile docker \
  --input Standards/Templates/Template_open.ods \
  --outdir my_results/ \
  --prefix COMPOUND
```

**Strict validation mode:**
```bash
nextflow run main.nf -profile docker \
  --input Standards/Templates/Template_open.ods \
  --strict
```

**On a SLURM cluster:**
```bash
nextflow run main.nf -profile slurm \
  --input Standards/Templates/Template_open.ods \
  --outdir results/
```

---

### Outputs

See [output.md](output.md) for a description of all generated files.
