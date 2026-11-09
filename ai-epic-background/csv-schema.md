---
aside: false
---

<script setup>
import { data as schema } from './csv-schema.data.mts'
</script>

# CSV Schema

[eic2ai](https://github.com/sroai/eic2ai) reads one reconstructed event file, and when a file needs it the
paired simulation file, and writes the {{ Object.keys(schema.files).length }} CSV files below
({{ schema.nColumns }} columns). Each box is one file. Click a box to list all its columns with their meaning
and unit; **Find a column** searches every file.

The columns are those of eic2ai with the 2026-11 changes. Files converted before them lack `prt_primary_*`,
`clu_link_index`, `elec_epz_*`, `mc_vtx_*` and the `mc_lam_*` / `mc_elec_index` columns of `reco_dis`, and
their `calo_clusters.clu_index` holds what is now `clu_link_index`.

<CsvSchema :schema="schema" />

## Reading the diagram

- A box is one file, `<stem>.<name>.csv.zip`; the line under its name says what one row is.
- **◆** marks the columns that identify one row of the file.
- **→** marks a column that holds the row number of another file. In `trk_hits`, `prt_index = 5`
  means the particle in the row of `mc_particles` with the same `evt` and `prt_index = 5`. In
  `mc_particles`, `prt_parent_index` points back into `mc_particles` the same way.
- `evt` is the entry number in the input file. It is in every file, so rows with equal `evt` come from the
  same event.
- A column of the Λ tables starts with a prefix that names the particle (`prot_` the proton from the Λ,
  `gamone_` the first photon of its π⁰, …); an open box shows the prefixes as headings.
- Units: GeV, GeV/c, mm, ns, rad, charge in e. An empty field means the value does not exist for that row.

[Data Format](./data-format) describes how the files are named, how hits are matched to particles and how
`prt_origin` separates signal from background.

## Joining files

```python
import pandas as pd

stem = "k_lambda_18x275_5000evt_0022"
hits = pd.read_csv(f"{stem}.trk_hits.csv.zip")
particles = pd.read_csv(f"{stem}.mc_particles.csv.zip")

# the full record of the particle behind each hit
hits = hits.merge(particles[["evt", "prt_index", "prt_sim_status", "prt_parent_index"]],
                  on=["evt", "prt_index"])

# the PDG code of that particle's parent: the same file joined to itself
parents = particles[["evt", "prt_index", "prt_pdg"]].rename(
    columns={"prt_index": "prt_parent_index", "prt_pdg": "parent_pdg"})
hits = hits.merge(parents, on=["evt", "prt_parent_index"], how="left")
```

## Editing this page

The boxes, columns and arrows come from
[`csv-schema.yaml`](https://github.com/sroai/sroai.github.io/blob/main/ai-epic-background/csv-schema.yaml)
next to this page: one line per column, `name: description [unit]`. The eic2ai repository holds this website
as a submodule, and its CI fails when a column eic2ai writes is missing from that file, listed in another
order, or has no description.
