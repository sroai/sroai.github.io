# Time-vs-Z plots

Per-event scatter plot of tracker hit time vs z-position, colored by
`prt_gen_status`. Useful as a first sanity check on a freshly produced CSV from
[`csv_convert/`](../../csv_convert/).

## Usage

```bash
python background_analysis.py <hits.csv> <event_number> [-o output.png]
```

Example:

```bash
python background_analysis.py output.csv 0 -o event_0_hits.png
```

This writes two figures:

- `event_<N>_hits.png` — `time vs z` for the requested event in the [0, 2000] ns window.
- `event_<N>_hits_full_range.png` — same plot zoomed to the event's actual time span.

Hits are colored by `prt_gen_status` (red for `prt_status == 1`, primary
generator-level particles).

## Dependencies

- `pandas`
- `matplotlib`

These are already pulled in by `csv_convert/pyproject.toml`, so running this
script inside the same `uv` venv works out of the box.
