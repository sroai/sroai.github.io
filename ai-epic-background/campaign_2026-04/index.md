# Campaign 26.04.1-stable

Converted (CSV) datasets produced from the **`26.04.1-stable`** ePIC
reconstruction campaign.

::: info Naming note
The campaign is labelled **26.04** (software release `26.04.1-stable`), but the
DIDs were actually registered in **May 2026** (`created_at: 2026-05-05`). The
`26.04` in the name refers to the software/release line, not the production
date.
:::

## What this campaign contains

Reconstructed background-mixed simulation, mixed at one signal event per
2&nbsp;µs frame (`Bkg_Exact1S_2us`), with the gold-coated 10&nbsp;µm beampipe
configuration. Source files are EICrecon outputs (`*.eicrecon.edm4eic.root`)
held in Rucio under DIDs like:

```
epic:/RECO/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=1
```

Key parameters (from each dataset's `rucio_metadata`):

| Field               | Value                          |
| ------------------- | ------------------------------ |
| `software_release`  | `26.04.1-stable`               |
| `data_level`        | `reconstruction`               |
| `geometry_config`   | `craterlake_<energy>`          |
| `generator`         | `pythia8`                      |
| `is_background_mixed` | `true`                       |
| `ion_species`       | `p`                            |
| beams               | electron × ion GeV (e.g. 10×100) |

## How the CSVs are produced

The conversion streams each ROOT file directly over XRootD (no local copy) and
runs the `edm4eic_*` converter macros inside the campaign container. See
[CSV Convert](/ai-epic-background/csv-convert) for the converters themselves and
[Available Datasets](/ai-epic-background/data) for the full Rucio catalogue.

Two pipeline steps drive it:

1. **`generate_datasets csv_eicrecon --rucio`** — queries Rucio
   (`is_background_mixed=true`, pattern `epic:*RECO/26.04.1*`) and writes one
   **dataset card** YAML per DID into `datasets/`.
2. **`40_csv_convert.py csv_eicrecon`** — reads those cards and generates the
   conversion jobs, one result directory per dataset, running the config's
   `csv_eicrecon.macros`.

## Output layout

The Rucio path tree is **not** mirrored. Each dataset collapses to one flat
directory (slug), and each ROOT file becomes one CSV named by its file index:

```
csv_eicrecon/
  Bkg_Exact1S_2us_GoldCt_10um_DIS_NC_10x100_q2-gt-1/
    0000.trk_hits.csv
    0000.trk_hits.csv.zip
    0001.trk_hits.csv
    ...
  Bkg_Exact1S_2us_GoldCt_10um_DIS_NC_10x275_q2-gt-1/
    ...
```

- **Directory slug** mirrors the DID path below `epic_craterlake/`, with
  `minQ2=1` rewritten to `q2-gt-1` (no `=` in names).
- **File id** is the per-file index (`0000`, `0001`, …) taken from the ROOT
  filename's trailing number.

## Dataset cards

Each dataset has a YAML card written by `generate_datasets --rucio` carrying
its DID, slug, parsed `metadata`, authoritative `rucio_metadata`, and the full
file list:

```yaml
did: epic:/RECO/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=1
slug: Bkg_Exact1S_2us_GoldCt_10um_DIS_NC_10x100_q2-gt-1
metadata:
  beam_energy: 10x100
  beam_crossing_angle: -0.025
  beam_divergence: hidiv_1
  beam_effects: true
  physics: pythia8-nc-dis
rucio_metadata:
  software_release: 26.04.1-stable
  electron_beam_energy_gev: 10
  ion_beam_energy_gev: 100
  q2_min_gev2: 1
  is_background_mixed: true
n_files: 123
files:
  - root://.../0000.eicrecon.edm4eic.root
```

<!-- TODO: dataset table generated from the YAML cards goes here. -->
