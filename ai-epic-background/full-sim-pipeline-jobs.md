# Job Creator

`simulation_pipeline/job_creator.py` defines the `JobCreator` class used by
every stage script. It owns the boilerplate — directories, SLURM scripts, log
locations, submit scripts — so a stage script only supplies the input files,
the output naming and the command that runs inside the container.

## What it generates

For one dataset (one card, usually one beam energy) `JobCreator.run()` writes
into `<output_dir>/jobs/`:

| File | Purpose |
| --- | --- |
| `<basename>.container.sh` | One per input file — what runs inside the Singularity / Apptainer image |
| `<basename>.slurm.sh` | One per input file — a single-job `sbatch` script, for rerunning one file |
| `container_scripts.list` | All container scripts of the dataset, one per line |
| `array.slurm.sh` | SLURM job-array script; each array task runs `slurm_files_per_job` lines of the list in sequence |
| `submit_jobs.sh` | Submits this dataset only: `sbatch --array=0-N[%throttle]` calls in chunks of `slurm_array_chunk` tasks |
| `run_local.sh` | Runs this dataset's container scripts locally, in sequence |

After all cards, `write_top_master_scripts` adds two scripts in the common
parent of the dataset output directories:

- `submit_all_slurm_jobs.sh` — calls every dataset's `submit_jobs.sh`;
- `run_all_local.sh` — runs every container script locally.

The per-dataset and all-dataset scripts have different names on purpose:
running "submit all" from inside one dataset's `jobs/` directory used to submit
a single energy.

Inside an array task a failing file only logs a warning; the rest of the chunk
continues, and the task exits non-zero at the end so `sacct` shows it as
failed.

## Logs

SLURM stdout/stderr never go to `/work`. Logs are written under `farm_out_dir`
(default `/farm_out/$USER`), mirroring the output path, e.g.
`/farm_out/romanov/work/eic3/.../csv-reco/9x130/`. Because `/farm_out` is
purged after a few days, every job gzip-copies its own log and err file to
`<output_dir>/logs/` on exit, including on walltime or `scancel` (`TERM`).

## Minimal usage

```python
from simulation_pipeline.job_creator import JobCreator, exension_replacer

runner = JobCreator(
    input_files=["file1.in", "file2.in"],
    output_file_name_func=exension_replacer(".in", ".out"),
    output_dir="/path/to/output",
    bind_dirs=["/data"],
)

runner.container_script_template = """#!/bin/bash
echo "Processing {input_file}"
my_program --input {input_file} --output {output_file} --events {events}
"""

runner.run()
```

`container_script_template` is formatted with `input_file`, `output_file`,
`output_dir`, `basename`, `events` and every constructor setting. Literal
braces in the template must be doubled (`${{VAR}}`). `exension_replacer`
(spelled this way in the code) maps an input name to an output path by swapping
the suffix and raises on inputs with a different suffix.

## Customizing the container script

Two hooks, both used by the stage scripts:

- `container_script_params_updater` — a function that receives the parameter
  dict for one input and returns it with extra keys. Stage 10 adds the
  afterburner preset, stage 11 the cocktail arguments and RNG seed, stage 40
  the per-role output paths.
- `container_script_generate_func` — replaces the whole generator. It receives
  the input file and returns `{"basename": ..., "content": ...}`.

```python
def custom_generate(input_file):
    basename = os.path.splitext(os.path.basename(input_file))[0]
    content = f"""#!/bin/bash
set -e
my_special_program --input {input_file}
"""
    return {"basename": basename, "content": content}

runner.container_script_generate_func = custom_generate
```

## Constructor arguments

| Argument | Default | Meaning |
| --- | --- | --- |
| `input_files` | — | Input paths; `root://` URLs are kept verbatim |
| `output_file_name_func` | — | `(input_file, output_dir) → output path` |
| `output_dir` | — | Output directory; `jobs/` and `logs/` go inside it |
| `bind_dirs` | — | Directories bound into the container (`-B d:d`) |
| `events` | `5000` | Events per job, available to the template |
| `beam_config` | `""` | Dataset label: the array job name, and the `epic_craterlake_<beam_config>.xml` suffix in the `npsim` / `eicrecon` templates |
| `container` | `eicweb/eic_xl:nightly` on `/cvmfs` | Image path |
| `slurm_time` | `24:00:00` | `--time` |
| `slurm_cpus_per_task` | `1` | `--cpus-per-task` |
| `slurm_mem_per_cpu` | `2G` | `--mem-per-cpu`; the farm is provisioned for 2 GB per CPU and bills extra CPUs above that |
| `slurm_account` | `eic` | `--account` |
| `slurm_partition` | `production` | `--partition` |
| `slurm_array_chunk` | `10000` | Max tasks per `sbatch --array` call (farm `MaxArraySize` is 10001) |
| `slurm_files_per_job` | `1` | Input files per array task |
| `slurm_array_throttle` | `0` | Max simultaneous array tasks (`%N`); 0 = no limit |
| `slurm_tmp_disk` | `""` | Node-local disk request, written as `--gres=disk:<value>` |
| `farm_out_dir` | `/farm_out/$USER` | Base directory for SLURM logs |

## What comes from the campaign config

Stages 10–30 pass `container`, `bind_dirs`, `event_count`,
`slurm_mem_per_cpu` and `farm_out_dir` from the config. Stage 40 also passes
`slurm_files_per_job` (default 20 in that script), `slurm_array_throttle` and
`slurm_tmp_disk`. Stage 90 takes `slurm_time` from the config, as one string
or a per-energy map. All other SLURM settings — `slurm_time` for stages 10–40,
`slurm_cpus_per_task`, `slurm_account`, `slurm_partition` — use the defaults
above.

## Why this design

The pipeline runs on the JLab farm, which uses **SLURM + Singularity**. Each
stage is generated and submitted separately because:

- one bad input must not fail the whole stage;
- stages have different resource profiles (afterburner is fast, `npsim` is
  long, CSV conversion can need several GB);
- a failed file can be rerun alone with `sbatch jobs/<basename>.slurm.sh`;
- short jobs are batched (`slurm_files_per_job`) because the farm penalizes
  floods of jobs shorter than two minutes.
