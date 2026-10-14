# Batch on SLURM

> The old Snakemake workflow (`Snakefile`, `run_jlab_slurm.sh`, `uv`-managed
> deps) is **retired**. CSV conversion is now driven by
> `40_csv_convert.py`, which emits SLURM **job arrays** through the shared
> [`JobCreator`](/ai-epic-background/full-sim-pipeline-jobs). This page covers how those jobs are
> laid out and submitted.

## Generating the jobs

See [Running the Converter](/ai-epic-background/csv-convert-running) — in short:

```bash
cd simulation-pipeline
generate_datasets csv_eicrecon -c configs/config-off-26-06.yaml
python simulation_pipeline/40_csv_convert.py csv_eicrecon -c configs/config-off-26-06.yaml
```

This writes a flat `jobs/` directory under the stage's output path.

## What gets written

For output dir `…/csv-reco/9x130`, the generator produces:

```
…/csv-reco/9x130/
├── jobs/
│   ├── <stem>.container.sh          # per-file: runs the config's macros
│   ├── <stem>.slurm.sh              # per-file wrapper (for reruns of one file)
│   ├── container_scripts.list       # the list the array indexes into
│   ├── array.slurm.sh               # the SLURM job-array wrapper
│   ├── submit_all_slurm_jobs.sh     # master submitter (one or few sbatch calls)
│   └── run_all_local.sh             # run everything locally, in sequence
└── <stem>.<role>.csv[.zip]          # the CSV outputs land here
```

## Submitting

```bash
cd …/csv-reco/9x130/jobs
./submit_all_slurm_jobs.sh          # queues everything as SLURM array(s)
```

To debug a single input, run its per-file script directly:

```bash
bash …/csv-reco/9x130/jobs/<stem>.container.sh   # inside the container env
```

Or run the whole set locally, in sequence, with timing:

```bash
./run_all_local.sh
```

## Farm etiquette (baked in)

The generator applies the JLab farm rules automatically — you don't set these by
hand:

- **SLURM stdout/stderr never goes to `/work`** (it overloads the work file
  server). Logs go under `farm_out_dir` (default `/farm_out/$USER`), mirroring the
  output path, e.g. `/farm_out/romanov/work/eic3/.../csv-reco/9x130/`. Job scripts
  and CSV outputs still live on `/work`.
- **Memory defaults to 2G/CPU** — the farm is provisioned for 2GB per CPU;
  requesting more makes SLURM bill extra CPUs. Override per campaign with
  `slurm_mem_per_cpu` only if a stage truly needs it.
- **Files are batched per job** (`slurm_files_per_job`, default 20) and array
  calls are chunked under the cluster's `MaxArraySize`, so jobs run for minutes
  rather than seconds (admins flag sub-2-minute jobs).

These knobs are config fields (`farm_out_dir`, `slurm_mem_per_cpu`,
`slurm_files_per_job`) — see the [Full-Sim Pipeline](/ai-epic-background/full-sim-pipeline).

## Prerequisites

- `apptainer` / `singularity` on compute nodes (the container image is set per
  campaign in the config).
- Access to `/cvmfs` and `/work` (JLab farm).
- SLURM for batch mode.
