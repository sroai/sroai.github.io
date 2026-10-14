# Data Format

CSV files are written by [eic2ai](https://github.com/sroai/eic2ai), a single-pass
C++ converter that reads an eicrecon file (`.edm4eic.root`) and, when a role needs
it, the paired npsim file (`.edm4hep.root`) once, and writes one CSV per **role**.
The rows are identical to those of the older `csv_convert/` ROOT macros (except
the shared Λ decay codes); the column names follow one shared vocabulary (below).

`eic2ai --list-columns` prints the header of every role, `eic2ai --list-writers`
the collections each role reads. The tables on this page follow the writer
sources in `eic2ai/src/writer_*.hpp`.

## Files

```
<stem>.<role>.csv.zip     default: one deflate ZIP64 entry named <stem>.<role>.csv
<stem>.<role>.csv         --compress none
<stem>.<role>.csv.gz      --compress gz
```

`<stem>` is the reco file name without `.edm4eic.root`, so
`k_lambda_18x275_5000evt_0022.edm4eic.root` gives
`k_lambda_18x275_5000evt_0022.trk_hits.csv.zip`. pandas reads the zip directly.

A role whose writer fails leaves no file; a file that exists is complete.

## Column vocabulary

Every column is `<prefix>_<quantity>`, and `evt` (the entry counter of the input
file) is the join key of every role.

| Prefix | Object |
| ------ | ------ |
| `prt` | the MC particle behind a hit, cluster or row |
| `trk_hit` | reconstructed tracker hit |
| `cal_hit` | digitized calorimeter hit |
| `clu` | calorimeter cluster |
| `rec` | reconstructed particle |
| `sim` | simulation truth aggregated over a calorimeter cell |

Units: GeV, GeV/c, mm, ns, rad, charge in e.

### Signal or background: `prt_origin`

| Value | Meaning |
| ----- | ------- |
| `0` | unknown |
| `1` | signal particle from the generator |
| `2` | Geant4 secondary of a signal particle |
| `3` | background particle from the generator |
| `4` | Geant4 secondary of a background particle |

The background merger adds `1000` to the generator status of background
particles before Geant4 runs. Generator particles are classified by
`prt_gen_status` (`1` or `2` signal, `>= 1000` background); Geant4 secondaries
(`prt_gen_status = 0`) take the class of their first generator ancestor up the
parent chain.

## Roles

| Role | One row per | Needs |
| ---- | ----------- | ----- |
| [`trk_hits`](#trk-hits) | reconstructed tracker hit, with its MC particle | reco |
| [`cal_hits`](#cal-hits) | digitized calorimeter hit, truth-labeled from the sim cell | reco + sim |
| [`calo_clusters`](#calo-clusters) | cluster ↔ MC particle association | reco |
| [`mc_particles`](#mc-particles) | MC particle | reco |
| [`reco_particles`](#reco-particles) | reconstructed particle | reco |
| [`mc_dis`](#mc-dis) | event: generator DIS kinematics | reco |
| [`event_index`](#event-index) | processed event | any |
| `reco_dis` | event: reconstructed DIS kinematics by seven methods, with truth | reco |
| `mcpart_lambda`, `lambda_acceptance`, `reco_ff_lambda`, `acceptance_ppim`, `acceptance_npi0`, `combinatorics_ppim`, `comb_candidates` | Λ analysis tables | reco or sim |

The Λ and DIS roles serve the [Meson Structure](https://jeffersonlab.github.io/meson-structure/)
analyses; their columns are listed by `eic2ai --list-columns`.

## `trk_hits` {#trk-hits}

One row per tracker hit association (raw hit → sim hit → MC particle), joined
with the reconstructed hit. Hits from every ePIC tracker:

```
B0TrackerRawHitAssociations            MPGDBarrelRawHitAssociations
BackwardMPGDEndcapRawHitAssociations   OuterMPGDBarrelRawHitAssociations
ForwardMPGDEndcapRawHitAssociations    SiBarrelRawHitAssociations
ForwardOffMTrackerRawHitAssociations   SiBarrelVertexRawHitAssociations
ForwardRomanPotRawHitAssociations      SiEndcapTrackerRawHitAssociations
TOFBarrelRawHitAssociations            TOFEndcapRawHitAssociations
```

| Column | Type | Unit | Description |
| ------ | ---- | ---- | ----------- |
| `evt` | uint64 | | entry counter |
| `hit_index` | uint64 | | index of the hit association in its collection |
| `prt_index` | uint64 | | index of the particle in `MCParticles` |
| `prt_pdg` | int32 | | PDG code (11 e⁻, 211 π⁺, 2212 p, …) |
| `prt_gen_status` | int32 | | generator status: 1 or 2 from the generator, 0 created by Geant4 |
| `prt_origin` | int32 | | [signal or background](#signal-or-background-prt-origin) |
| `prt_energy` | double | GeV | total energy |
| `prt_charge` | float | e | electric charge |
| `prt_mom_x/y/z` | double | GeV/c | momentum |
| `prt_vtx_time` | float | ns | time at the production vertex |
| `prt_vtx_pos_x/y/z` | float | mm | production vertex |
| `prt_end_time` | float | ns | equal to `prt_vtx_time` (EDM4hep stores one particle time) |
| `prt_end_pos_x/y/z` | float | mm | endpoint |
| `trk_hit_cell_id` | uint64 | | full cellID of the reconstructed hit |
| `trk_hit_system_id` | uint64 | | detector system id (bits 0–7 of the cellID) |
| `trk_hit_system_name` | string | | detector name, e.g. `SiBarrelVertex` |
| `trk_hit_pos_x/y/z` | float | mm | reconstructed hit position |
| `trk_hit_time` | float | ns | reconstructed hit time |
| `trk_hit_pos_err_xx/yy/zz` | float | mm² | position variances |
| `trk_hit_time_err` | float | ns | time uncertainty |
| `trk_hit_edep` | float | GeV | energy deposited in the sensor |
| `trk_hit_edep_err` | float | GeV | energy deposit uncertainty |

## `cal_hits` {#cal-hits}

One row per digitized calorimeter hit. The reco file has no calorimeter hit ↔
particle association, so each hit is matched by `(evt, cellID)` to the sim hit
of the same cell in the paired `.edm4hep.root` file. A cell with several
contributing particles gets the `prt_origin` of the energy-majority class,
`label_purity` = that class's energy fraction, and the `prt_*` block of the
largest contributor of that class. A hit whose cell has no sim hit keeps its
features with `prt_origin = 0` and zeros in the `prt_*` block.

Calorimeters: `EcalBarrelScFiRecHits`, `EcalBarrelImagingRecHits`,
`EcalEndcapNRecHits`, `EcalEndcapPRecHits`, `HcalBarrelRecHits`,
`HcalEndcapNRecHits`, `HcalEndcapPInsertRecHits`, `LFHCALRecHits`,
`B0ECalRecHits`, `EcalFarForwardZDCRecHits`, `HcalFarForwardZDCRecHits`.

| Column | Type | Unit | Description |
| ------ | ---- | ---- | ----------- |
| `evt` | uint64 | | entry counter |
| `cal_hit_collection` | string | | rec-hit collection name (the detector) |
| `cal_hit_cell_id` | uint64 | | full cellID (same cell in sim and reco) |
| `cal_hit_system_id` | uint64 | | detector system id (bits 0–7 of the cellID) |
| `cal_hit_system_name` | string | | detector name |
| `cal_hit_pos_x/y/z` | float | mm | hit position |
| `cal_hit_energy` | float | GeV | calibrated energy |
| `cal_hit_energy_err` | float | GeV | energy uncertainty |
| `cal_hit_time` | float | ns | digitized time |
| `cal_hit_time_err` | float | ns | time uncertainty |
| `sim_energy` | double | GeV | sum of the cell's contribution energies (raw deposit) |
| `sim_time` | float | ns | earliest contribution time |
| `n_contrib` | int32 | | contributions in the cell |
| `label_purity` | float | | energy fraction of the majority origin class |
| `prt_index` | uint64 | | representative particle in `MCParticles` |
| `prt_pdg`, `prt_gen_status`, `prt_origin` | int32 | | as in `trk_hits` |
| `prt_energy` | double | GeV | total energy |
| `prt_charge` | float | e | electric charge |
| `prt_mom_x/y/z` | double | GeV/c | momentum |
| `prt_vtx_time` | float | ns | time at the production vertex |
| `prt_vtx_pos_x/y/z` | float | mm | production vertex |
| `prt_end_pos_x/y/z` | float | mm | endpoint |

The `cal_hit_*` columns are the detector-level features; `sim_*`, `n_contrib`,
`label_purity` and `prt_*` are truth.

## `calo_clusters` {#calo-clusters}

One row per cluster ↔ MC particle association, from every `*ClusterAssociations`
collection of the reco file (regular, truth and split-merge clusters of the
ECAL, HCAL, B0, ZDC and luminosity calorimeters).

| Column | Type | Unit | Description |
| ------ | ---- | ---- | ----------- |
| `evt` | uint64 | | entry counter |
| `clu_index` | uint64 | | index of the association in its collection |
| `clu_collection` | string | | association collection name (detector + algorithm) |
| `prt_index` … `prt_end_pos_x/y/z` | | | the particle block of `trk_hits` (with `prt_end_time`) |
| `clu_first_cell_id` | uint64 | | cellID of the first constituent hit (0 when none resolves) |
| `clu_system_id` | uint64 | | detector system id of that cellID |
| `clu_system_name` | string | | detector name (`Unknown` when no hit resolves) |
| `clu_type` | int32 | | cluster type flag |
| `clu_energy` | float | GeV | cluster energy |
| `clu_energy_err` | float | GeV | energy uncertainty |
| `clu_time` | float | ns | cluster time |
| `clu_time_err` | float | ns | time uncertainty |
| `clu_nhits` | uint32 | | hits in the cluster |
| `clu_pos_x/y/z` | float | mm | cluster position |
| `clu_pos_err_xx/yy/zz` | float | mm² | position variances |
| `clu_theta`, `clu_phi` | float | rad | intrinsic polar and azimuthal angles |
| `clu_assoc_weight` | float | | association weight |

## `mc_particles` {#mc-particles}

One row per particle of `MCParticles`.

| Column | Type | Unit | Description |
| ------ | ---- | ---- | ----------- |
| `evt` | uint64 | | entry counter |
| `prt_index` | uint64 | | index in `MCParticles` |
| `prt_pdg` | int32 | | PDG code |
| `prt_gen_status` | int32 | | 1 or 2 signal, `>= 1000` background, 0 created by Geant4 |
| `prt_sim_status` | int32 | | simulator status bit field (createdInSimulation, decayedInTracker, …) |
| `prt_origin` | int32 | | [signal or background](#signal-or-background-prt-origin) |
| `prt_mass` | double | GeV/c² | mass |
| `prt_energy` | double | GeV | total energy |
| `prt_charge` | float | e | electric charge |
| `prt_mom_x/y/z` | double | GeV/c | momentum |
| `prt_vtx_time` | float | ns | time at the production vertex |
| `prt_vtx_pos_x/y/z` | float | mm | production vertex |
| `prt_end_pos_x/y/z` | float | mm | endpoint |
| `prt_n_parents` | uint32 | | number of parents |
| `prt_n_daughters` | uint32 | | number of daughters |
| `prt_parent_index` | int64 | | index of the first parent, `-1` without parents |

`prt_index` here is the same index as `prt_index` in `trk_hits` and
`calo_clusters` (both read the reco file's `MCParticles`), so `(evt, prt_index)`
joins a hit or cluster to its full particle record.

## `reco_particles` {#reco-particles}

One row per `ReconstructedParticles` entry.

| Column | Type | Unit | Description |
| ------ | ---- | ---- | ----------- |
| `evt` | uint64 | | entry counter |
| `rec_index` | int32 | | index in `ReconstructedParticles` |
| `rec_pdg` | int32 | | PDG code assigned by reconstruction |
| `rec_charge` | float | e | electric charge |
| `rec_energy` | float | GeV | energy |
| `rec_mass` | float | GeV/c² | mass |
| `rec_mom_x/y/z` | float | GeV/c | momentum |
| `rec_ref_pos_x/y/z` | float | mm | reference point |
| `rec_pid_goodness` | float | | goodness of the PID hypothesis |
| `rec_type` | int32 | | particle type flag |
| `rec_n_clusters` | | | clusters attached |
| `rec_n_tracks` | | | tracks attached |
| `rec_n_particles` | | | daughter particles |
| `rec_n_particle_ids` | | | ParticleID hypotheses |
| `rec_n_cluster_hits` | | | calorimeter hits behind the clusters |
| `rec_n_track_measurements` | | | measurements behind the tracks |
| `rec_n_tracker_hits` | | | tracker hits behind those measurements |

## `mc_dis` {#mc-dis}

One row per event with the generator's DIS kinematics, read from the event
parameters `dis_<name>` that the generator writes. Columns: `evt`, then
`alphas`, `mx2`, `nu`, `p_rt`, `pdrest`, `pperps`, `pperpz`, `q2`, `s_e`, `s_q`,
`tempvar`, `tprime`, `tspectator`, `twopdotk`, `twopdotq`, `w`, `x_d`, `xbj`,
`y_d`, `yplus`. A missing parameter leaves an empty field.

## `event_index` {#event-index}

One row per processed event: `evt`, `event_number` (from `EventHeader`),
`reco_collections`, `sim_collections` (collections in each frame, 0 without that
file). Its row count is the event count of a complete conversion.

## Loading the CSV

```python
import pandas as pd

hits = pd.read_csv("k_lambda_18x275_5000evt_0022.trk_hits.csv.zip")

event_0 = hits[hits["evt"] == 0]
primaries = hits[hits["prt_gen_status"] == 1]

signal = hits[hits["prt_origin"].isin([1, 2])]
background = hits[hits["prt_origin"].isin([3, 4])]

hits_per_system = hits.groupby("trk_hit_system_name").size()

# Full particle record of each hit
particles = pd.read_csv("k_lambda_18x275_5000evt_0022.mc_particles.csv.zip")
hits = hits.merge(particles[["evt", "prt_index", "prt_sim_status", "prt_parent_index"]],
                  on=["evt", "prt_index"])
```

Files written by the macros before the column unification use older names
(`prt_status`, `rec_collection`, `event`, …). `eic2ai/column_renames.py` holds
the old → new table per role; `rename_dataframe(df, role)` renames a loaded file.
