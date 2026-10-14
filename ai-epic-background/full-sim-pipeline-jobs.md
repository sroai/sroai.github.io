# Job Creator

`job_creator.py` defines the `JobCreator` class shared by every
`NN_create_*_jobs.py` script. It owns the boilerplate so each stage script can
focus on stage-specific input / output naming and the inner command.

## What it generates

For each input file it produces:

1. A **container script** — what runs *inside* the Singularity / Apptainer image.
2. A **SLURM submitter** — one batch script that wraps the whole campaign and
   queues every container script as an `sbatch` array job.

This gives you a flat directory of self-contained scripts that you can re-run
individually if a single job fails, plus a single submitter to launch the lot.

## Minimal usage

```python
from job_creator import JobCreator

def output_name(input_file, output_dir):
    return os.path.join(output_dir, os.path.basename(input_file).replace(".in", ".out"))

runner = JobCreator(
    input_files=["file1.in", "file2.in"],
    output_file_name_func=output_name,
    output_dir="/path/to/output",
    bind_dirs=["/data", "/home"],
)

runner.container_job_template = """#!/bin/bash
echo "Processing {input_file}"
my_program --input {input_file} --output {output_file} --events {events}
echo "Done!"
"""

runner.run()
```

## Advanced usage

For stages where the command depends on the input file, override
`generate_container_script`:

```python
def custom_generate(input_file):
    basename = os.path.splitext(os.path.basename(input_file))[0]
    special_params = calculate_params(input_file)
    content = f"""#!/bin/bash
set -e
my_special_program --params {special_params} --input {input_file}
"""
    return {"basename": basename, "content": content}

runner.generate_container_script = custom_generate
```

## Configuration knobs

The constructor accepts:

- `input_files` — list of inputs (typically a `glob.glob`).
- `output_file_name_func` — callable that maps input → output path.
- `output_dir` — where outputs land.
- `bind_dirs` — directories to bind into the container (`/cvmfs`, `/volatile`, …).
- `events` — events per job (forwarded into the template).
- `container` — Singularity image path.
- `slurm_time`, `slurm_cpus_per_task`, `slurm_mem_per_cpu`, `slurm_account`,
  `slurm_partition` — SLURM resource requests.

In production these come from the YAML campaign config rather than being
hard-coded in each `NN_create_*_jobs.py` script.

## Why this design?

The pipeline runs on the JLab farm, which uses **SLURM + Singularity**. Each
stage is independently rerunnable, which matters because:

- A single bad input shouldn't fail the whole stage.
- Stages have very different resource profiles (afterburner is fast, `npsim` is
  long, `EICrecon` is memory-heavy).
- Rerunning a single failed file by re-submitting its one `*.container.sh`
  script is much cheaper than re-launching a whole stage.
