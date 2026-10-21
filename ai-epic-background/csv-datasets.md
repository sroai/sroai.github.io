# CSV Datasets

Where the converted CSVs are, which converter wrote them and which roles each
directory holds. The column layout of every role is on
[Data Format](/ai-epic-background/data-format); loading them in pandas, numpy
and PyTorch is on [AI / ML Datasets](/ai-epic-background/ai-datasets). The
`FULL` / `RECO` inputs they were made from are on
[Available Datasets](/ai-epic-background/data).

## Access

Everything below is on the JLab work disk, not in Rucio. On the farm the paths
work as written; from outside, prefix them with the XRootD host:

```bash
# one file
xrdcp root://sci-xrootd.jlab.org//work/eic3/users/romanov/meson-structure-2026-06/\
csv-2026-09-bkg-phase10/18x275/k_lambda_18x275_5000evt_0022.trk_hits.csv.zip .

# a whole role of a directory
xrdfs root://sci-xrootd.jlab.org ls /work/eic3/users/romanov/meson-structure-2026-06/csv-2026-09-bkg-phase10/18x275
```

The XRootD client has to be 5.9 or newer and needs a CA directory — see the
warning on the [project overview](/ai-epic-background/).

Files are named `<stem>.<role>.csv.zip`, one ZIP64 deflate entry each, which
pandas reads directly. A role whose writer fails leaves no file, so a file that
exists is complete.

## eic2ai conversions

Written by [eic2ai](https://github.com/sroai/eic2ai) with the current column
names. All four roles share `evt` as the join key.

| Directory | Signal | Beams | Roles | Pipeline config |
| --- | --- | --- | --- | --- |
| `meson-structure-2026-06/csv-2026-09-bkg-phase10/<beam>` | k-Λ exclusive, background-mixed 2 µs frames | 10x100, 10x130, 18x275 | `trk_hits`, `cal_hits`, `reco_dis`, `event_index` | `config-phase10-cal.yaml`, `config-phase10-cal-18x275.yaml` |
| `disnc-2026-07-background/csv-2026-09-phase12/10x100_minQ2_<N>` | DIS/NC of campaign 26.07.1, background-mixed | 10x100, `minQ2` = 1, 10, 100 | `trk_hits`, `cal_hits`, `reco_dis`, `event_index` | `config-phase12-disnc.yaml` |

Both live under `/work/eic3/users/romanov/`; the configs are in
[JeffersonLab/msf-simulation-pipeline](https://github.com/JeffersonLab/msf-simulation-pipeline)
`configs/`.

- **18x275 is 400 zips, not 428** — 100 stems × 4 roles. Seven of the 107 RECO
  files of the campaign are damaged at the source (five truncated, two never
  closed, so the `podio_metadata` tree is missing) and eic2ai refuses them;
  recovering them needs the RECO files re-produced upstream. The `FULL` side is
  complete.
- 10x100 and 10x130 were converted as 8 files each (5,000 events per file);
  18x275 is the full set.
- `reco_dis` carries `truth_*` from `InclusiveKinematicsTruth`, which is the
  only true-Q² source in these files: pythia8 writes no `dis_*` frame
  parameters and the background merge drops them.
- The phase-12 DIS/NC files carry edm4eic schema 81000 and need the
  `eic_xl:26.07.0-stable` container — a 26.06 container reads them with the
  collections silently missing.

## ROOT-macro conversions

Earlier CSVs from the pipeline's `csv_convert/` macros. Same rows, older column
names (`prt_status`, `event`, …); `rename_dataframe(df, role)` from
`eic2ai/column_renames.py` maps them to the current vocabulary.

| Directory | Campaign | Roles / macros |
| --- | --- | --- |
| `/work/eic3/users/romanov/meson-structure-2026-06/csv-2026-09-background/<beam>` | k-Λ background, 2026-06 | `mc_dis`, `mcpart_lambda`, `reco_particles`, `calo_clusters`, `trk_hits`, `cal_hits` |
| `/work/eic/users/romanov/epic-background-2026-05/csv_eicrecon/` | 26.05.0, ALP (EW_BSM) | eicrecon roles of that campaign |
| `/work/eic/users/romanov/epic-background-2025-10/csv_reco/` | 25.10 | reco roles of that campaign |

The 2026-05 and 2025-10 sets are under `/work/eic/`, the newer ones under
`/work/eic3/`.
