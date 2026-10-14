# AI / ML Datasets

The CSVs produced by [`csv_convert/`](/ai-epic-background/csv-convert) are designed to drop directly
into Python data-science and ML stacks. This page covers a few common loading
patterns.

## Loading with pandas

```python
import pandas as pd

df = pd.read_csv("hits.csv")

# One DataFrame per event
events = {evt: g.reset_index(drop=True) for evt, g in df.groupby("evt")}
```

For very large files prefer `pyarrow` or chunked reading:

```python
chunks = pd.read_csv("hits.csv", chunksize=200_000)
for chunk in chunks:
    process(chunk)
```

## Loading with numpy

```python
import numpy as np

# Numeric subset for speed
cols = ["evt", "trk_hit_pos_x", "trk_hit_pos_y", "trk_hit_pos_z", "trk_hit_time"]
arr = np.genfromtxt("hits.csv", delimiter=",", names=True, usecols=cols, encoding=None)
```

## PyTorch Dataset

The simplest possible per-event Dataset that yields one tensor of hits per event:

```python
import pandas as pd
import torch
from torch.utils.data import Dataset

FEATURE_COLS = [
    "trk_hit_pos_x", "trk_hit_pos_y", "trk_hit_pos_z", "trk_hit_time",
    "trk_hit_edep", "trk_hit_system_id",
]
LABEL_COLS = ["prt_pdg", "prt_gen_status"]

class TrackerHitsDataset(Dataset):
    def __init__(self, csv_path: str):
        df = pd.read_csv(csv_path)
        self.events = [g.reset_index(drop=True) for _, g in df.groupby("evt")]

    def __len__(self):
        return len(self.events)

    def __getitem__(self, idx):
        evt = self.events[idx]
        x = torch.tensor(evt[FEATURE_COLS].to_numpy(), dtype=torch.float32)
        y = torch.tensor(evt[LABEL_COLS].to_numpy(), dtype=torch.long)
        return x, y
```

For multi-file datasets, point a Dataset at a directory of `*.csv.zip` (which is
exactly what the [CSV conversion jobs](/ai-epic-background/csv-convert-snakemake) write next to each
CSV output) and stream files lazily.

## Useful filters

A few common selections you'll want during training:

```python
# Primary particles only (generator-level, status == 1)
primary = df[df["prt_gen_status"] == 1]

# Geant4-secondaries only (status == 0)
secondary = df[df["prt_gen_status"] == 0]

# Restrict to one detector subsystem
si_barrel = df[df["trk_hit_system_name"] == "SiBarrelVertex"]

# Cut on hit time (background suppression)
in_time = df[df["trk_hit_time"].between(-5, 25)]
```

## Suggested ML targets

Some tasks the format naturally supports:

- **Background hit classification** — predict `prt_gen_status == 1` (signal) vs not.
- **PID-from-hits** — predict `prt_pdg` from per-hit features.
- **Track origin regression** — predict `prt_vtx_pos_*` from a hit cluster.
- **Subsystem prediction / detector ID auxiliary task** — predict
  `trk_hit_system_id` from spatial hit features.

Each of these only needs the columns that are already in the CSV; no further
preprocessing of the ROOT files is required.

## Schema reference

See the [Data Format](/ai-epic-background/data-format) page for the complete column list, units,
and the `HitRecord` struct that produces them.
