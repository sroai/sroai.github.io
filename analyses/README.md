# Analyses

Standalone Python analyses that consume the CSVs produced by
[`csv_convert/`](../csv_convert/). Each analysis lives in its own subfolder
with its scripts and a short README.

## Subfolders

| Folder              | Purpose                                                          |
| ------------------- | ---------------------------------------------------------------- |
| `time-vs-z-plots/`  | Per-event scatter plot of tracker hit time vs z, colored by `prt_gen_status`. |

## Adding a new analysis

1. Make a new subfolder named after the analysis (kebab-case).
2. Drop in your script(s) and a short README explaining inputs / outputs.
3. If you need extra deps, add them to `csv_convert/pyproject.toml` (the
   project shares a single `uv` venv) or document a separate venv in the
   subfolder's README.
