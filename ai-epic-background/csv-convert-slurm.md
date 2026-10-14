# Batch on SLURM

CSV conversion on the farm is driven by `simulation_pipeline/40_csv_convert.py`, which emits
SLURM **job arrays** through the shared [`JobCreator`](/ai-epic-background/full-sim-pipeline-jobs).
The older Snakemake workflow is retired. This page covers how the jobs are laid out, submitted
and tuned.

## Generating the jobs

See [Running the Converter](/ai-epic-background/csv-convert-running) for the config keys. In short:

```bash
cd simulation-pipeline
generate_datasets csv_phase10 -c configs/config-phase10-cal-18x275.yaml
python simulation_pipeline/40_csv_convert.py csv_phase10 -c configs/config-phase10-cal-18x275.yaml
```

## What gets written

For each energy the generator writes into the stage's `output` directory, e.g.
`…/csv-2026-09-bkg-phase10/18x275`:

```
…/csv-2026-09-bkg-phase10/18x275/
├── jobs/
│   ├── <stem>.container.sh          # per file: the conversion, run inside the container
│   ├── <stem>.slurm.sh              # per file: SLURM wrapper (for rerunning one file)
│   ├── container_scripts.list       # the list the array tasks index into
│   ├── array.slurm.sh               # the SLURM job-array script
│   ├── submit_jobs.sh               # submits this energy's arrays
│   └── run_local.sh                 # runs this energy's files locally, in sequence
├── logs/                            # gzip copies of the SLURM logs, written at job exit
└── <stem>.<role>.csv.zip            # the CSV outputs
```

Two aggregate scripts go to the common parent of all energies' output directories (the output
directory itself when the config has one energy):

- `submit_all_slurm_jobs.sh` — runs every energy's submit script;
- `run_all_local.sh` — runs every container script locally, in sequence.

## Submitting

```bash
…/csv-2026-09-bkg-phase10/submit_all_slurm_jobs.sh      # every energy
…/csv-2026-09-bkg-phase10/18x275/jobs/submit_jobs.sh     # one energy
```

Each array task processes `slurm_files_per_job` lines of `container_scripts.list` in sequence;
one failing file does not stop the rest of the chunk, and the task exits non-zero after all
files were attempted if any failed. Submission is split into `sbatch --array` calls that stay
under the cluster's `MaxArraySize`.

To rerun one input, submit its wrapper, or run its container script inside the container:

```bash
sbatch …/18x275/jobs/<stem>.slurm.sh
bash …/18x275/jobs/<stem>.container.sh     # inside the container environment
```

Rerunning is safe: a job regenerates only the roles whose zip is missing or empty.

## Node-local staging

Each job copies its input file (and paired file) to the compute node's local disk, converts
the local copies and moves the outputs to the stage's `output` directory at the end. The
staging directory is created under the first writable of `$TMPDIR`,
`/scratch/slurm/$SLURM_JOB_ID`, `/scratch` and `/tmp`, and removed at exit. Before copying,
the job checks the free space against the input size plus `staging_headroom_gb` (default 25)
and exits with code 3 when it does not fit. Staging is skipped when every output already
exists.

## Farm settings

The generator applies the JLab farm rules; these config fields tune them:

| Key | Default | Effect |
| --- | --- | --- |
| `farm_out_dir` | `/farm_out/$USER` | SLURM stdout/stderr go here, mirroring the output path; job scripts and outputs stay in the output directory. `/farm_out` is purged after a few days, so each job gzip-copies its logs to `<output>/logs/` at exit. |
| `slurm_mem_per_cpu` | `2G` | memory per CPU; the farm is provisioned for 2 GB per CPU |
| `slurm_files_per_job` | `20` | input files per array task, so tasks run for minutes |
| `slurm_array_throttle` | `0` (no limit) | maximum array tasks running at once (`%N`) |
| `slurm_tmp_disk` | none | node-local disk request, e.g. `"100G"` → `--gres=disk:100G`, so tasks land on nodes with room to stage |
| `staging_headroom_gb` | `25` | staging space required on top of each input's size |

These are config fields; see the [Full-Sim Pipeline](/ai-epic-background/full-sim-pipeline).

## Prerequisites

- `singularity` on the compute nodes (the job scripts call `singularity exec`); the container
  image is set per campaign by `container` in the config.
- With `converter: eic2ai`, an eic2ai binary on a file system the compute nodes see, set as
  `eic2ai_bin`. The existing configs use a binary built in the same container release as
  `container` (see [Building eic2ai](/ai-epic-background/csv-convert-running#building-eic2ai)).
- Access to `/cvmfs` and `/work` (JLab farm).
