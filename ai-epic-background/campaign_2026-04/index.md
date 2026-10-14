# Campaign 26.04.1-stable

::: warning Earlier campaign
This page records an earlier campaign. Newer background-mixed campaigns
(26.07.0, 26.07.1) and our local productions are listed on
[Available Datasets](/ai-epic-background/data), the current catalog.
:::

CSV conversion of the **`26.04.1-stable`** ePIC background-mixed campaign.

::: info Naming note
The campaign is labelled **26.04** (software release `26.04.1-stable`), but the
DIDs were registered in **May 2026** (`created_at: 2026-05-05`). The `26.04` in
the name refers to the software/release line, not the production date.
:::

## What this campaign contains

Background-mixed simulation with exactly one signal event per 2&nbsp;µs frame
(`Bkg_Exact1S_2us`) and the gold-coated (10&nbsp;µm) beampipe configuration:
DIS/NC at 10x100 and 10x275 GeV, minQ2 = 1, 10, 100, 1000. Each dataset has a
**FULL** (npsim, `edm4hep`) and a **RECO** (EICrecon, `*.eicrecon.edm4eic.root`)
partition in Rucio, under DIDs like:

```
epic:/RECO/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=1
```

Key parameters (from each dataset's Rucio metadata):

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

The simulation pipeline handles official campaigns with Rucio dataset cards:
the card's `files:` are the Rucio `root://` PFNs, and each job runs the
configured converter (`edm4eic_*` ROOT macros or eic2ai) on them. See
[CSV Convert](/ai-epic-background/csv-convert) for the converters and
[Data Format](/ai-epic-background/data-format) for the CSV columns.

1. **`generate_datasets csv_eicrecon --rucio -c <config>`** — lists the DIDs
   matching the config's `rucio_did_pattern` (and `rucio_did_filters`, e.g.
   `is_background_mixed=true`) and writes one **dataset card** YAML per DID into
   `<datasets_dir>/csv_eicrecon/`.
2. **`40_csv_convert.py csv_eicrecon -c <config>`** — reads those cards and
   generates the conversion jobs, one output directory per dataset.

No config for 26.04.1 is kept in `simulation-pipeline/configs/`;
`config-off-26-06.yaml` is the current example of a Rucio-driven conversion.

## Output layout

The Rucio path tree is **not** mirrored. Each dataset collapses to one flat
directory (slug), and each ROOT file gives one CSV per role, named after the
input file:

```
<csv_eicrecon.output>/
  Bkg_Exact1S_2us_GoldCt_10um_DIS_NC_10x100_q2-gt-1/
    <stem>.trk_hits.csv.zip
    <stem>.calo_clusters.csv.zip
    ...
  Bkg_Exact1S_2us_GoldCt_10um_DIS_NC_10x275_q2-gt-1/
    ...
```

- **Directory slug** joins the DID path below `epic_craterlake/` with `_`,
  with `minQ2=1` rewritten to `q2-gt-1` (no `=` in names).
- **`<stem>`** is the ROOT file name without `.eicrecon.edm4eic.root`.
- The ROOT-macro converter also keeps the unzipped `<stem>.<role>.csv`; eic2ai
  writes the `.csv.zip` only.

## Dataset cards

Each dataset has a YAML card written by `generate_datasets --rucio` carrying
the DID, slug, beam energy, output directory, the Rucio metadata, and the full
file list:

```yaml
dataset: epic:/RECO/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=1
slug: Bkg_Exact1S_2us_GoldCt_10um_DIS_NC_10x100_q2-gt-1
stage: csv_eicrecon
energy: 10x100
output: <csv_eicrecon.output>/Bkg_Exact1S_2us_GoldCt_10um_DIS_NC_10x100_q2-gt-1
metadata:
  source: rucio
  rucio_metadata:
    software_release: 26.04.1-stable
    electron_beam_energy_gev: 10
    ion_beam_energy_gev: 100
    q2_min_gev2: 1
    is_background_mixed: true
n_files: 123
files:
  - root://.../<stem>.eicrecon.edm4eic.root
```
