# Campaigns

A "campaign" is a coherent production run with a fixed container image, a fixed
beam-energy set, and a fixed output base directory. Each one lives in its own
**self-contained** YAML config under `configs/` in the
[`simulation-pipeline`](/ai-epic-background/full-sim-pipeline) submodule — no inheritance, no base
files.

## Existing campaigns

| Config file                       | Notes                                                    |
| --------------------------------- | -------------------------------------------------------- |
| `config-msf-26-07.yaml`           | Meson-structure, July 2026 production                    |
| `config-msf-26-07-background.yaml`| Same, with the background cocktail merged in             |
| `config-off-26-06.yaml`           | Official ePIC campaign — RECO already on Rucio, CSV only |

## Config layout

Each config is fully self-contained, and each stage is a **top-level block** with
its own `input` / `output` (stages chain by `${...}` interpolation). Excerpt from
`config-off-26-06.yaml`:

```yaml
# Base directory — everything else is relative to this
base_dir: "/work/eic3/users/romanov/dis-csv-2026-06"

# Container image (pin a stable tag for reproducibility) + bind mounts
container: "/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:26.06.0-stable"
bind_dirs:
  - "${base_dir}"

# Beam-energy combinations to process (electron x proton GeV)
energies: ["5x41", "9x100", "9x130", "9x275"]

event_count: 5000

# Farm etiquette (see the pipeline README): logs off /work, 2G/CPU, batching.
farm_out_dir: "/farm_out/romanov"
slurm_mem_per_cpu: "2G"
slurm_files_per_job: 20

# generate_datasets writes cards under <datasets_dir>/<stage>/
datasets_dir: "${base_dir}/datasets"

# A csv stage: where CSVs land + which converter macros run.
csv_eicrecon:
  output: "${base_dir}/csv_eicrecon"
  macros:
    - edm4eic_trk_hits
    - edm4eic_calo_clusters
    - edm4eic_mc_particles
    - edm4eic_reco_particles
```

The variables `${base_dir}`, `${energy}`, and cross-stage references like
`${afterburner.output}` are interpolated by the pipeline at render time.

## Starting a new campaign

1. Copy the closest existing config (e.g. `cp configs/config-off-26-06.yaml
   configs/config-off-26-08.yaml`).
2. Update `base_dir` to your new output root.
3. Pin `container:` to whatever `eic_xl` tag you want to lock in.
4. Adjust `energies`, `event_count`, and each csv stage's `macros:` if needed.
5. Mint dataset cards, then run the stages in order (cards first, jobs second):

   ```bash
   generate_datasets afterburner -c configs/config-off-26-08.yaml
   python simulation_pipeline/10_create_afterburner_jobs.py -c configs/config-off-26-08.yaml
   # ... npsim, eicrecon ...
   generate_datasets csv_eicrecon -c configs/config-off-26-08.yaml
   python simulation_pipeline/40_csv_convert.py csv_eicrecon -c configs/config-off-26-08.yaml
   ```

   Each stage renders the per-input scripts and a SLURM array submitter into
   `${base_dir}/<stage>/.../jobs/`.

6. Submit each stage's `submit_all_slurm_jobs.sh` when its inputs are ready.

   Official campaigns whose RECO is already on Rucio skip the local sim chain
   entirely — mint cards with `generate_datasets csv_eicrecon --rucio` and go
   straight to the CSV stage.

## "saveall" variant

`21_create_npsim_saveall_jobs.py` runs `npsim` with **all** sensitive volumes
saving hits — including the tracking volume itself. This produces dramatically
larger outputs but is what you want for background occupancy / AI training:
every Geant4 hit is preserved, not just the ones in normal readout volumes.

The `npsim_saveall` config block points at this branch of the pipeline.
