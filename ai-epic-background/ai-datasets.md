# AI / ML Datasets

The CSVs written by [eic2ai](https://github.com/sroai/eic2ai) are the input of the
AI studies on this site. This page covers how they are loaded, labeled and joined;
[Data Format](/ai-epic-background/data-format) lists every column with its unit.

## Files and events

- One conversion run (a reco file, with its paired sim file for `cal_hits`) gives
  one file per role, named by the reco file stem: `<stem>.<role>.csv.zip`, a ZIP
  with a single CSV entry. pandas reads it directly; no unzip step is needed.
- `evt` is the 0-based entry counter of the input file and the join key of every
  role of that file. It restarts at 0 in every file, so a dataset built from many
  files needs a file index next to `evt`.
- In background-mixed samples one entry is one 2 µs timeframe: exactly one signal
  event plus Poisson-sampled background from the beam-induced sources. The signal
  time varies from frame to frame. Our pipeline mixes with `SignalBackgroundMerger`;
  its successor, [TimeframeBuilder](https://github.com/eic/TimeframeBuilder), is being prepared for ePIC production.
  Details: [Backgrounds](/ai-epic-background/background).
- `event_index` has one row per processed entry: its row count is the event count
  of the conversion, and `event_number` maps `evt` to `EventHeader.eventNumber`.

## Labels

Every row that carries a particle has `prt_origin`:

| `prt_origin` | Meaning | Typical use |
| ------------ | ------- | ----------- |
| `1`, `2` | signal particle, or its Geant4 secondary | keep (signal) |
| `3`, `4` | background particle, or its Geant4 secondary | reject (background) |
| `0` | unknown | drop or report separately |

`prt_gen_status` is the generator status: `1`/`2` for signal, `>= 1000` for
background (the merger's per-source offset tells which source), `0` for particles
created by Geant4. Use `prt_origin` for the signal/background class, since it also
classifies Geant4 secondaries by their generator ancestor; use `prt_gen_status`
to split background by source.

The `prt_*`, `sim_*`, `n_contrib` and `label_purity` columns are truth. Model
inputs come from the detector-level blocks: `trk_hit_*`, `cal_hit_*`, `clu_*`,
`rec_*`.

## Loading with pandas

```python
import pandas as pd

COLUMNS = ["evt", "prt_origin", "prt_gen_status",
           "trk_hit_system_id", "trk_hit_pos_x", "trk_hit_pos_y", "trk_hit_pos_z",
           "trk_hit_time", "trk_hit_edep"]

hits = pd.read_csv("k_lambda_18x275_5000evt_0022.trk_hits.csv.zip", usecols=COLUMNS)

hits = hits[hits["prt_origin"] != 0]
hits["is_background"] = hits["prt_origin"] >= 3
events = {evt: group.reset_index(drop=True) for evt, group in hits.groupby("evt")}
```

Several files of one sample, with a file index so that `(file, evt)` names one
event:

```python
from pathlib import Path

paths = sorted(Path("csv/18x275").glob("*.trk_hits.csv.zip"))
hits = pd.concat(
    [pd.read_csv(path, usecols=COLUMNS).assign(file=file_index)
     for file_index, path in enumerate(paths)],
    ignore_index=True)
```

Files written before 2026-09-30 by the `csv_convert/` macros use older column
names; `rename_dataframe(df, role)` from `column_renames.py` in the
[eic2ai](https://github.com/sroai/eic2ai) repository renames a loaded frame.

## Large files: convert once to parquet

`trk_hits` files of background-mixed samples are large, and most studies need a
small subset of the columns. Reading the CSV once with `usecols` and explicit
dtypes and writing parquet makes later reads fast. Explicit dtypes also prevent
wrong inference, e.g. `label_purity` read as an integer when the first rows all
hold `1`.

```python
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

DTYPES = {
    "evt": "int64", "prt_origin": "int8", "prt_gen_status": "int32",
    "trk_hit_system_id": "int16",
    "trk_hit_pos_x": "float32", "trk_hit_pos_y": "float32", "trk_hit_pos_z": "float32",
    "trk_hit_time": "float32", "trk_hit_edep": "float32",
}

source = "k_lambda_18x275_5000evt_0022.trk_hits.csv.zip"
target = source.removesuffix(".csv.zip") + ".parquet"

writer = None
for chunk in pd.read_csv(source, usecols=list(DTYPES), dtype=DTYPES, chunksize=5_000_000):
    table = pa.Table.from_pandas(chunk, preserve_index=False)
    if writer is None:
        writer = pq.ParquetWriter(target, table.schema, compression="zstd")
    writer.write_table(table)
writer.close()
```

## Time inside the frame

Background hits arrive throughout the 2 µs frame, and the signal sits at a
different time in each frame, so a fixed cut on `trk_hit_time` does not separate signal from
background. For truth studies, time relative to the signal start is more useful:

```python
is_signal = hits["prt_origin"].isin([1, 2])
signal_start = hits[is_signal].groupby("evt")["trk_hit_time"].min()
hits["time_since_signal"] = hits["trk_hit_time"] - hits["evt"].map(signal_start)
```

`signal_start` uses truth; a model has to find the signal time from the hits.

## Calorimeter hits

`cal_hits` labels each digitized calorimeter hit from the simulated cell with the
same `cellID`. A cell with several contributing particles takes the energy-majority
`prt_origin`, and `label_purity` is that class's energy fraction. A hit without a
simulated cell has `n_contrib = 0` and `prt_origin = 0`; filter on `prt_origin`
to keep labeled hits.

```python
cal = pd.read_csv(
    "k_lambda_18x275_5000evt_0022.cal_hits.csv.zip",
    usecols=["evt", "cal_hit_collection", "cal_hit_pos_x", "cal_hit_pos_y", "cal_hit_pos_z",
             "cal_hit_energy", "cal_hit_time", "n_contrib", "label_purity", "prt_origin"],
    dtype={"label_purity": "float32"})

matched = cal[cal["prt_origin"] != 0]
clean = matched[matched["label_purity"] > 0.9]      # example cut: cells dominated by one class
per_detector = matched.groupby("cal_hit_collection")["prt_origin"].value_counts()
```

## Joining roles

```python
particles = pd.read_csv("k_lambda_18x275_5000evt_0022.mc_particles.csv.zip",
                        usecols=["evt", "prt_index", "prt_sim_status", "prt_parent_index"])
hits = pd.read_csv("k_lambda_18x275_5000evt_0022.trk_hits.csv.zip")
hits = hits.merge(particles, on=["evt", "prt_index"], how="left")
```

`(evt, prt_index)` joins `trk_hits` and `calo_clusters` rows to `mc_particles`;
all three read the reco file's `MCParticles`. `cal_hits` takes its particle from
the sim file.

## PyTorch Dataset

One item per event: per-hit detector features and a per-hit background label.

```python
import pandas as pd
import torch
from torch.utils.data import Dataset

FEATURES = ["trk_hit_pos_x", "trk_hit_pos_y", "trk_hit_pos_z",
            "trk_hit_time", "trk_hit_edep", "trk_hit_system_id"]

class TrackerHitsDataset(Dataset):
    def __init__(self, path: str):
        hits = pd.read_csv(path, usecols=["evt", "prt_origin", *FEATURES])
        hits = hits[hits["prt_origin"] != 0]
        self.events = [group for _, group in hits.groupby("evt")]

    def __len__(self):
        return len(self.events)

    def __getitem__(self, index):
        event = self.events[index]
        x = torch.tensor(event[FEATURES].to_numpy(), dtype=torch.float32)
        y = torch.tensor((event["prt_origin"] >= 3).to_numpy(), dtype=torch.float32)
        return x, y
```

Events have different hit counts, so a `DataLoader` needs `batch_size=1` or a
`collate_fn` that pads. For many files, read from parquet and keep the
`(file, evt)` key.

## Tasks these files serve

- **Tracker-hit background rejection** — classify `trk_hits` rows as signal
  (`prt_origin` 1, 2) or background (3, 4) from `trk_hit_*` features.
- **Signal localization in time** — find the time window of the signal inside the
  2 µs frame before classifying hits.
- **Calorimeter-hit background rejection** — the same task on `cal_hits`, with
  `label_purity` as a measure of label quality.
- **Event classification** — classify events from their `reco_particles` rows,
  e.g. by physics process or Q² range.
