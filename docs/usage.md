## Usage

### Installation

You need two tools installed: **Nextflow** and **Docker**. Follow the steps for your operating system below.

#### 1. Install Java (required by Nextflow)

Nextflow runs on Java. Check if you already have it:

```bash
java -version
```

If not installed, use [SDKMAN](https://sdkman.io/):

```bash
curl -s https://get.sdkman.io | bash
```

On new terminal: 

```bash
sdk install java 17.0.10-tem
java -version
```

#### 2. Install Nextflow

```bash
curl -s https://get.nextflow.io | bash
```

This downloads a `nextflow` file to your current directory. Move it somewhere on your PATH so you can use it from anywhere. <BR>
Make nextflow executable and move it to executable path: 

```bash
chmod +x nextflow
mkdir -p $HOME/.local/bin/
mv nextflow $HOME/.local/bin/
```

Verify the installation:

```bash
nextflow -version
```

#### 3. Install Docker

Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/) for your operating system (macOS or Windows). On Linux, follow the [Docker Engine install guide](https://docs.docker.com/engine/install/).

After installation, start Docker Desktop and verify it is running:

```bash
docker --version
```

#### 4. Get BioXend

Clone the repository:

```bash
git clone https://github.com/zmahnoor14/BioXend.git
cd BioXend
```

That's it — no conda environments or manual dependency installs are needed. All software runs inside Docker.

---

### Quickstart

The Docker image is hosted on [Docker Hub](https://hub.docker.com/r/zmahnoor/bioxend) and pulled automatically.

```bash
nextflow run main.nf -profile docker \
  --input  path/to/Template_open.ods \
  --outdir results/ \
  --prefix HMDM \
  --xenobiotic_class drug
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

### Docker (recommended)

The image `zmahnoor/bioxend:latest` is hosted on [Docker Hub](https://hub.docker.com/r/zmahnoor/bioxend) and pulled automatically by Nextflow when you use `-profile docker`. No manual build step is required.

**Run the container interactively (optional):**
```bash
docker run -it zmahnoor/bioxend:latest bash
```

---

### Singularity (HPC environments)

Singularity is not a built-in profile. Pull the image directly from Docker Hub and run with `-with-singularity`:

```bash
singularity pull bioxend.sif docker://zmahnoor/bioxend:latest

nextflow run main.nf \
  -with-singularity bioxend.sif \
  --input  path/to/Template_open.ods \
  --outdir results/ \
  --prefix HMDM \
  --xenobiotic_class drug
```

---

### Outputs

See [output.md](output.md) for a description of all generated files.
