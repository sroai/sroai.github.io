# Running the Converter

Run eic2ai by hand on one file for a spot check, or generate a campaign's worth of jobs with
`40_csv_convert.py`. Both need a built eic2ai binary.

## Building eic2ai

eic2ai needs podio, EDM4HEP, EDM4EIC, zlib and fmt — build it inside an EIC container that
ships them (eic_xl, eic-full, eic-claude). From the `eic2ai/` directory of the pipeline
repository:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
./build/eic2ai --list-writers
```

The configure step downloads minizip-ng 4.2.2. Offline, pass
`-DFETCHCONTENT_SOURCE_DIR_MINIZIP=<unpacked source tree>`, or `-DEIC2AI_FETCH_MINIZIP=OFF` to
use a system minizip-ng.

On a machine with a local docker image, `tests/build_in_image.sh <image> <build-dir> [jobs]`
runs the same two cmake steps inside that image, e.g.
`tests/build_in_image.sh eicweb/eic_xl:nightly build-eic_xl-nightly 6`. It assumes the
parent-repository layout (`submodules/simulation-pipeline/eic2ai`) and mounts `/data`.

The existing campaign configs keep one build directory per container release and run each
binary in the release it was built in (`build-eic_xl-26.06` with `eic_xl:26.06.0-stable`,
`build-eic_xl-26.07` with `eic_xl:26.07.0-stable`).

## Option 1 — one file by hand

```bash
# Every role a reco + sim pair supports:
eic2ai --reco msf_9x130_0001.edm4eic.root --sim msf_9x130_0001.edm4hep.root \
       --out-dir out --writers auto

# Selected roles; positional files are sorted into reco/sim by their suffix:
eic2ai msf_9x130_0001.edm4eic.root msf_9x130_0001.edm4hep.root \
       --out-dir out --writers trk_hits,cal_hits,event_index

# Quick look at the first 100 events, plain CSV:
eic2ai --reco msf_9x130_0001.edm4eic.root --out-dir out --writers trk_hits -n 100 --compress none
```

Options (from `eic2ai --help`):

| Option | Meaning |
| --- | --- |
| `--reco FILE` | eicrecon output (`.edm4eic.root`); `<stem>` is taken from this file |
| `--sim FILE` | npsim output (`.edm4hep.root`) holding the same events as the reco file |
| `FILE...` | positional inputs, assigned by suffix (`.edm4eic.root` reco, `.edm4hep.root` sim) |
| `--out-dir DIR` | output directory, created when missing (required) |
| `--writers LIST` | comma-separated roles (required, or `auto`) |
| `--writers auto` | every writer whose inputs are given; skipped writers are listed |
| `--compress MODE` | `zip` (default), `none` (plain CSV) or `gz` |
| `--zip-level N` | deflate level for zip and gz, 1–9, default 3 |
| `-n N` | process the first N entries only |
| `--progress N` | progress line every N events (default 100; 0 = off) |
| `--selective` | read only the collections the enabled writers list (off by default; faster reads) |
| `--list-writers` | print each role, its needs and collections, then exit |
| `--list-columns` | print the header of every output, then exit |

Exit codes: `0` every writer succeeded; `1` at least one writer failed (its output is
discarded, the others are complete); `2` the run did not start or stopped (bad options,
unreadable input, pairing guard).

## Option 2 — generate jobs for a campaign

The batch driver is `simulation_pipeline/40_csv_convert.py`. It applies the farm settings
(SLURM arrays, logs under `/farm_out`, memory per CPU, node-local staging) described on
[Batch on SLURM](/ai-epic-background/csv-convert-slurm).

First write the dataset cards for the stage, then generate the jobs:

```bash
cd simulation-pipeline

# 1. Discover inputs into cards (local glob, --rucio, or explicit --files):
generate_datasets csv_phase10 -c configs/config-phase10-cal-18x275.yaml

# 2. Emit one job per input ROOT file:
python simulation_pipeline/40_csv_convert.py csv_phase10 -c configs/config-phase10-cal-18x275.yaml
```

The stage argument is the name of a stage block in the config (`csv_phase10`,
`csv_phase12`, `csv_eicrecon`, …); the script is the same for every stage.

### Config keys

| Key | Where | Meaning |
| --- | --- | --- |
| `converter` | stage or top level | `macros` (default) or `eic2ai` |
| `eic2ai_bin` | stage or top level | path of the eic2ai binary as seen inside the container; required for `eic2ai`; its directory is bound into the container |
| `eic2ai_args` | stage or top level | extra options appended to the eic2ai call, e.g. `--selective` |
| `roles` | stage | roles to produce (eic2ai only); covers roles without a macro, such as `event_index` |
| `macros` / `sim_macros` / `paired_macros` | stage | macro lists; with `eic2ai` they name roles too (`edm4eic_trk_hits` → `trk_hits`) when `roles` is absent |
| `input`, `pattern` | stage | where `generate_datasets` globs the inputs |
| `paired: {dir, suffix}` | stage | each input gets a same-stem companion file, e.g. the `.edm4hep.root` for `cal_hits`; inputs without one are skipped with a warning at job-build time |
| `output` | stage | directory for the CSV zips and `jobs/` |
| `staging_headroom_gb` | stage or top level | staging space required on top of each input's size (default 25) |

An eic2ai stage from `configs/config-phase10-cal-18x275.yaml`:

```yaml
converter: "eic2ai"
eic2ai_bin: "/work/eic3/users/romanov/optim/submodules/simulation-pipeline/eic2ai/build-eic_xl-26.06/eic2ai"
eic2ai_args: ""

csv_phase10:
  input:   "${eicrecon.output}"
  pattern: "*.edm4eic.root"
  paired:
    dir:    "${npsim_background.output}"
    suffix: ".edm4hep.root"
  output:  "${base_dir}/csv-2026-09-bkg-phase10/${energy}"
  roles:
    - trk_hits
    - cal_hits
    - reco_dis
    - event_index
```

### What one job does

With `converter: eic2ai`, the container script for one input file:

1. skips every role whose `<stem>.<role>.csv.zip` already exists and is non-empty, and exits
   when none is missing;
2. copies the input (and its paired file) to node-local disk;
3. runs one `eic2ai <inputs> --out-dir <staging> --writers <missing roles> --compress zip <eic2ai_args>`;
4. moves the finished zips to the stage's `output` directory.

A writer that fails leaves no file and the job exits non-zero, so the next run regenerates
that role alone.

### Inspect emitted jobs without a farm

A stage renders job scripts from a card's `files:` list without opening the inputs, so you can
dry-render against a synthetic card:

```bash
generate_datasets csv_eicrecon -c cfg.yaml --energy 9x130 \
    --files /any/path/msf_9x130_0001.edm4eic.root /any/path/msf_9x130_0002.edm4eic.root
python simulation_pipeline/40_csv_convert.py csv_eicrecon -c cfg.yaml

cat <output>/jobs/*.container.sh   # per-file container script
cat <output>/jobs/array.slurm.sh   # SLURM job-array wrapper
bash -n <output>/jobs/*.sh         # syntax check without running
```

For a stage with a `paired` block the companion files must exist: the driver checks them when
it builds the jobs.

## Legacy path — ROOT macros

`converter: macros` (the default) runs the ROOT macros in `csv_convert/`, one `root` call per
role. By hand, inside an environment with ROOT, podio, EDM4HEP and EDM4EIC:

```bash
cd simulation-pipeline/csv_convert
root -x -l -b -q 'edm4eic_trk_hits.cxx("input.edm4eic.root","input.trk_hits.csv")'
root -x -l -b -q 'edm4hep_acceptance_ppim.cxx("input.edm4hep.root","input.acceptance_ppim.csv")'
```

Each macro's entry function has the file's name and takes `(input, output)`, plus an optional event
limit (`-1` = all). `edm4eic_cal_hits` takes `(reco, sim, output)`. In a macro stage the
config lists them under `macros` (called with the input), `sim_macros` (the paired file) and
`paired_macros` (both). The job script keeps the plain CSV and adds `<out>.csv.zip`, deletes a
0-byte output so the next run retries it, and continues with the other macros when one fails.
Macro outputs use the macro-era column names
(see [Data Format](/ai-epic-background/data-format)).

## Quick visualisation

The archived [ai-epic-background](https://github.com/eic/ai-epic-background) repository has a
per-event plot script,
[`analyses/time-vs-z-plots/`](https://github.com/eic/ai-epic-background/tree/main/analyses/time-vs-z-plots),
that reads a `trk_hits` CSV (the columns `evt`, `prt_gen_status`, `trk_hit_time`,
`trk_hit_pos_z`):

```bash
python background_analysis.py <stem>.trk_hits.csv.zip 0 -o event_0_hits.png
```

It writes a `time vs z` plot of the requested event and a companion plot over the event's full
time range; hits are colored by `prt_gen_status`.
