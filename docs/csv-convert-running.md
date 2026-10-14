# Running the Converter

There are two ways to run a conversion: invoke a single macro by hand with
`root` (quick, one file, one role), or generate a whole campaign's worth of jobs
with `40_csv_convert.py` (batch, many files, many roles).

## Option 1 — one macro by hand (ROOT)

Every converter is a ROOT macro whose entry function has the same name as the
file. Run it inside an environment that has ROOT + podio + EDM4EIC/EDM4HEP
available (e.g. inside the `eic_xl` container), from the `csv_convert/` directory:

```bash
cd simulation-pipeline/csv_convert

# edm4eic (reco level):
root -x -l -b -q 'edm4eic_reco_particles.cxx("input.edm4eic.root","input.reco_particles.csv")'
root -x -l -b -q 'edm4eic_trk_hits.cxx("input.edm4eic.root","input.trk_hits.csv")'

# edm4hep (sim level):
root -x -l -b -q 'edm4hep_acceptance_ppim.cxx("input.edm4hep.root","input.acceptance_ppim.csv")'
```

Each macro takes `(input_root, output_csv)`. The output-CSV name is up to you when
you call it directly; the batch driver below names it `<input-stem>.<role>.csv`
by convention.

## Option 2 — generate jobs for a campaign

For anything beyond a spot check, let the pipeline generate jobs. This is the
same path used in production and it applies the farm etiquette (SLURM arrays,
logs off `/work`, 2G/CPU) automatically.

First mint dataset cards for the stage, then generate the jobs:

```bash
cd simulation-pipeline

# 1. Discover inputs into cards (local glob, --rucio, or explicit --files):
generate_datasets csv_eicrecon -c configs/config-off-26-06.yaml

# 2. Emit one job per input ROOT file, running the config's macros:
python simulation_pipeline/40_csv_convert.py csv_eicrecon -c configs/config-off-26-06.yaml
```

`40_csv_convert.py <stage>` reads the stage block from the config — its `macros:`
list decides which converters run, and its `output:` decides where the CSVs land.
Use `csv_dd4hep` for the `edm4hep_*` macros and `csv_eicrecon` for the
`edm4eic_*` ones; the script itself is identical for both.

### Inspect emitted jobs without a farm

A stage renders job scripts from a card's `files:` list — it never stats the
inputs — so you can dry-render against a synthetic card:

```bash
generate_datasets csv_eicrecon -c cfg.yaml --energy 9x130 \
    --files /any/path/msf_9x130_0001.edm4eic.root /any/path/msf_9x130_0002.edm4eic.root
python simulation_pipeline/40_csv_convert.py csv_eicrecon -c cfg.yaml

cat <output>/csv-reco/9x130/jobs/*.container.sh   # per-file container script
cat <output>/csv-reco/9x130/jobs/array.slurm.sh   # SLURM job-array wrapper
bash -n <output>/csv-reco/9x130/jobs/*.sh         # syntax-check without running
```

The generated container script runs one `convert <role> <macro>.cxx <out.csv>`
line per configured macro. It uses `set -uo pipefail` (but **not** `-e`) so the
converters are independent: one crashing does not abort the others, and a macro
that leaves a 0-byte CSV has it deleted so the next run retries it instead of
skipping an "already exists" file. Non-empty outputs are zipped to `<out>.csv.zip`.

## Quick visualisation

Once a `trk_hits` CSV is produced, you can inspect a single event with the
plotting script in
[`analyses/time-vs-z-plots/`](https://github.com/eic/ai-epic-background/tree/main/analyses/time-vs-z-plots):

```bash
uv run python analyses/time-vs-z-plots/background_analysis.py input.trk_hits.csv 0 -o event_0_hits.png
```

This writes two figures: a `time vs z` scatter plot for the requested event, and a
companion plot covering the full time range. Hits are colored by `prt_gen_status`
(red for `prt_gen_status == 1`, primary particles).
