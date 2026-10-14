# Campaigns

A campaign is one production run with a fixed container image, a fixed set of
beam energies and a fixed output base directory. Each campaign is one
**self-contained** YAML file under `configs/` in the
[simulation pipeline](/ai-epic-background/full-sim-pipeline) — no inheritance,
no base files. The file is also the record of what ran where.

## Existing campaigns

| Config file | Stages and notes |
| --- | --- |
| `config-msf-26-07.yaml` | Meson-structure, July 2026: `afterburner` → `npsim` → `eicrecon` (B0 truth-seeding `flags`) → `csv_dd4hep`, `csv_eicrecon`, `csv_cal` (paired). Energies 5x41, 9x100, 9x130, 9x275 |
| `config-msf-26-07-background.yaml` | Same signal with ePIC background cocktails: `afterburner` → `bg_merger` → `npsim_background` → `eicrecon` → `csv_eicrecon` |
| `config-msf-26-06-background.yaml` | June 2026 background campaign (10x100, 10x130, 18x275), CSV re-conversion in September 2026. Sim and reco exist; only `csv_background` (paired, macros including `edm4eic_cal_hits`) runs |
| `config-off-26-06.yaml` | Official ePIC DIS NC campaign 26.06.0. RECO is on Rucio; only `csv_eicrecon` runs, on `root://` PFNs |
| `config-phase10-cal.yaml` | Background frames of the June 2026 campaign, 10x130 and 10x100: `csv_phase10` with `eic2ai`, roles `trk_hits`, `cal_hits`, `reco_dis`, `event_index` |
| `config-phase10-cal-18x275.yaml` | The same conversion for 18x275 |
| `config-phase12-disnc.yaml` | ePIC campaign 26.07.0 background-mixed DIS NC 10x100 (`Bkg_Exact1S_2us`), split into three minimum-Q² slices: `csv_phase12` with `eic2ai`. Needs the `eic_xl:26.07.0-stable` image to read the 26.07 data model |
| `config-ilreco-2026-07.yaml` | ilreco EMCal profile tables: stage 90 only, no input files; `profiles` and `calsim` blocks |

The `energies` list is normally beam energies; in `config-phase12-disnc.yaml`
the entries are slice keys (`10x100_minQ2_1`, …) that only label cards and
output directories.

## Config layout

Each stage is a **top-level block** with its own `input`, `pattern` and
`output`; stages chain by `${...}` interpolation. Excerpt from
`config-msf-26-07.yaml`:

```yaml
base_dir: "/work/eic3/users/romanov/meson-structure-2026-07"
container: "/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:26.06-stable/"
bind_dirs: ["${base_dir}"]
energies: ["5x41", "9x100", "9x130", "9x275"]
event_count: 1000
farm_out_dir: "/farm_out/romanov"
slurm_mem_per_cpu: "2G"
datasets_dir: "${base_dir}/datasets"
slurm_files_per_job: 20

afterburner:                                        # 10_create_afterburner_jobs.py
  input:   "${base_dir}/eg-hepmc/${energy}-priority"
  pattern: "*.hepmc"
  output:  "${base_dir}/afterburner/${energy}-priority"

npsim:                                              # 20_create_npsim_jobs.py
  input:   "${afterburner.output}"
  pattern: "*.hepmc3.tree.root"
  output:  "${base_dir}/dd4hep/${energy}"

csv_cal:                                            # 40_csv_convert.py csv_cal
  input:   "${eicrecon.output}"
  pattern: "*.edm4eic.root"
  paired:
    dir:    "${npsim.output}"
    suffix: ".edm4hep.root"
  output:  "${base_dir}/csv-cal/${energy}"
  macros:
    - edm4eic_cal_hits
```

A csv stage that uses `eic2ai` instead of the macros, from
`config-phase12-disnc.yaml`:

```yaml
converter: "eic2ai"
eic2ai_bin: "/work/eic3/users/romanov/optim/submodules/simulation-pipeline/eic2ai/build-eic_xl-26.07/eic2ai"
slurm_tmp_disk: "10G"
staging_headroom_gb: 3

csv_phase12:                                        # 40_csv_convert.py csv_phase12
  input:   "${eicrecon.output}"
  pattern: "*.edm4eic.root"
  paired:
    dir:    "${npsim_background.output}"
    suffix: ".edm4hep.root"
  output:  "${base_dir}/csv-2026-09-phase12/${energy}"
  roles: [trk_hits, cal_hits, reco_dis, event_index]
```

OmegaConf resolves `${base_dir}`, `${energy}` (bound per card) and cross-stage
references such as `${afterburner.output}`. A stage block whose data already
exists can hold only `output` and serve as a path anchor, as `npsim_background`
does in the conversion-only configs.

### Keys

| Key | Read by | Meaning |
| --- | --- | --- |
| `base_dir`, `container`, `bind_dirs`, `energies`, `event_count` | all | Output root, image, bind mounts, per-energy cards, events per job |
| `datasets_dir` | `generate_datasets`, stages | Cards go to `<datasets_dir>/<stage>/` |
| `farm_out_dir`, `slurm_mem_per_cpu` | all stages | SLURM log base (never `/work`), memory per CPU (default `2G`) |
| `slurm_files_per_job`, `slurm_array_throttle`, `slurm_tmp_disk`, `staging_headroom_gb` | stage 40 | Files per array task (default 20), max simultaneous tasks, node-local disk request, staging space margin in GB (default 25) |
| `<stage>.input`, `.pattern`, `.output` | `generate_datasets`, stages | Where the local glob looks and where outputs go |
| `eicrecon.flags` | stage 30 | Extra `eicrecon` options |
| `background_configs`, `background_config_dir`, `strip_xrootd_prefix` | stages 11, 22 | Cocktail JSON per energy, its directory, `root://` → local path |
| `macros`, `sim_macros`, `paired_macros`, `paired`, `roles` | stage 40 | Which roles a csv stage produces and from which input |
| `converter`, `eic2ai_bin`, `eic2ai_args`, `csv_convert_dir` | stage 40 | `macros` (default) or `eic2ai`; binary path inside the container; macro directory override |
| `rucio_did_pattern`, `rucio_did_filters`, `max_files_per_dataset` | `generate_datasets --rucio` | DID discovery and an optional file cap (0 = all) |
| `profiles`, `calsim`, `slurm_time` | stage 90 | Profile-table scan, calsim geometry and response, walltime per energy |

## Starting a new campaign

1. Copy the closest existing config, e.g.
   `cp configs/config-msf-26-07.yaml configs/config-msf-26-10.yaml`.
2. Set `base_dir` to the new output root.
3. Pin `container:` to the `eic_xl` tag to use. The image must match the data
   model of its inputs: 26.07 files are not readable with a 26.06 image.
4. Adjust `energies`, `event_count` and each csv stage's roles.
5. For each stage in order, write the cards, then the jobs:

   ```bash
   generate_datasets afterburner -c configs/config-msf-26-10.yaml
   python simulation_pipeline/10_create_afterburner_jobs.py -c configs/config-msf-26-10.yaml
   # ... npsim, eicrecon ...
   generate_datasets csv_eicrecon -c configs/config-msf-26-10.yaml
   python simulation_pipeline/40_csv_convert.py csv_eicrecon -c configs/config-msf-26-10.yaml
   ```

   A stage's cards can be written only after the previous stage's outputs
   exist, because the local producer globs `<stage>.input`. Each generator
   writes the scripts into `<dataset output>/jobs/` and prints the path of the
   all-datasets submit script at the end.

6. Submit `submit_all_slurm_jobs.sh` (in the common parent of the stage's
   dataset output directories) when the inputs are ready, or a single
   dataset's `jobs/submit_jobs.sh`. Check what was submitted with
   `squeue -u $USER -h -o '%j' | sort | uniq -c`.

Official campaigns whose RECO is already on Rucio skip the local chain: set
`rucio_did_pattern`, write cards with `generate_datasets csv_eicrecon --rucio -c <cfg>`
and run `40_csv_convert.py` directly. Rucio cards are one per dataset DID; each
dataset's outputs go to `<output>/<dataset-slug>/`, e.g.
`DIS_NC_10x100_q2-gt-1`.

To test job generation without the farm, write a card from a fake file list
with `generate_datasets <stage> -c <cfg> --energy 9x130 --files a.root b.root`
and read the emitted scripts; stages never open their inputs while generating
jobs. Paired csv stages are the exception: they check that each companion
file exists.

## "saveall" variant

`21_create_npsim_saveall_jobs.py` differs from stage 20 in one option:
`--part.userParticleHandler=""` instead of `Geant4TVUserParticleHandler`. The
TV handler drops from the `MCParticles` truth record every secondary created
outside the tracking volume. With the empty handler, secondaries created
anywhere in the detector (calorimeter showers, beam pipe, magnets) can stay in
`MCParticles`, subject to `npsim`'s general keep rules, and outputs are larger.
Stage 22 (`npsim_background`) runs with the empty handler as well.

The stage reads the `npsim_saveall` config block; none of the current configs
defines one.
