#!/usr/bin/env python3
"""
Merge many per-run reco_particles CSVs of one dataset into a single Feather file.

Each run file (produced by csv_convert/reco_particles.cxx) is one CSV table with
one row per reconstructed particle and an ``evt`` column that restarts at 0 in
every file. CSVs converted before 2026-09-30 carry the macro-era column names
(``event``, ``px``, ...); they are renamed on load (LEGACY_COLUMNS below). When several runs are concatenated the event numbers would collide,
so we offset each file's events by the running maximum to keep them globally
unique across the whole dataset (see meson-structure/docs/data.md for how runs
relate to files).

The files may be plain ``.csv`` or zipped ``.csv.zip`` (pandas infers the
compression from the extension).

Usage
-----
    merge_reco_particles_to_feather.py run0.csv[.zip] run1.csv[.zip] ... -o out.feather
    merge_reco_particles_to_feather.py "dataset_dir/*.csv.zip" -o out.feather --glob
"""

import argparse
import glob
import re
import sys
from pathlib import Path
from typing import List

import pandas as pd

# Macro-era column names of reco_particles → the unified vocabulary of
# simulation-pipeline/eic2ai/column_renames.py (the source of this table).
LEGACY_COLUMNS = {
    "event": "evt", "id": "rec_index", "pdg": "rec_pdg", "charge": "rec_charge", "energy": "rec_energy",
    "mass": "rec_mass", "px": "rec_mom_x", "py": "rec_mom_y", "pz": "rec_mom_z",
    "ref_x": "rec_ref_pos_x", "ref_y": "rec_ref_pos_y", "ref_z": "rec_ref_pos_z",
    "pid_goodness": "rec_pid_goodness", "type": "rec_type", "n_clusters": "rec_n_clusters",
    "n_tracks": "rec_n_tracks", "n_particles": "rec_n_particles", "n_particle_ids": "rec_n_particle_ids",
    "n_cluster_hits": "rec_n_cluster_hits", "n_track_measurements": "rec_n_track_measurements",
    "n_tracker_hits": "rec_n_tracker_hits",
}


def _run_index(path: str) -> int:
    """Extract the numeric run index from a file name like ``0075.reco_particles.csv.zip``.

    Falls back to -1 when no leading number is present so the column is still
    written and the merge does not fail on unexpected names.
    """
    m = re.match(r"(\d+)", Path(path).name)
    return int(m.group(1)) if m else -1


def concat_runs_with_unique_events(files: List[str]) -> pd.DataFrame:
    """Load and concatenate per-run CSVs with globally unique event IDs (column ``evt``).

    Event IDs are made globally unique by adding an offset equal to the running
    maximum event ID seen so far. A ``run`` column records the originating file
    index so a (run, event) pair can be traced back to its source run.

    Parameters
    ----------
    files : list of str
        Paths to the per-run CSV (or CSV.zip) files, in the order to concatenate.

    Returns
    -------
    pd.DataFrame
        The concatenated table with unique ``evt`` IDs and a ``run`` column.
    """
    if not files:
        raise ValueError("No files provided for concatenation")

    dfs = []
    offset = 0
    n_skipped = 0

    for file in files:
        try:
            df = pd.read_csv(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {file}")
        except pd.errors.EmptyDataError:
            # A failed/aborted conversion job leaves a 0-byte CSV.
            # Skip it but keep the merge going.
            print(f"WARNING: skipping empty file {file}")
            n_skipped += 1
            continue
        except Exception as e:
            raise ValueError(f"Error reading CSV file {file}: {e}")

        df = df.rename(columns=LEGACY_COLUMNS)
        if "evt" not in df.columns:
            raise ValueError(f"CSV file {file} does not contain an 'evt' column")

        # Record the source run before touching the event numbering.
        df.insert(0, "run", _run_index(file))

        # Offset event IDs so they stay globally unique across all runs.
        df["evt"] = df["evt"] + offset
        offset = int(df["evt"].max()) + 1  # next file starts after this one

        dfs.append(df)
        print(
            f"Loaded {len(df):>8} particles from {file} "
            f"(events {df['evt'].min()}-{df['evt'].max()})"
        )

    if not dfs:
        raise ValueError("All input files were empty - nothing to concatenate")
    if n_skipped:
        print(f"\nWARNING: skipped {n_skipped} empty file(s) out of {len(files)}")

    combined = pd.concat(dfs, ignore_index=True)
    return combined


def merge_to_feather(files: List[str], output_file: str) -> pd.DataFrame:
    """Concatenate the given run CSVs and write the result to ``output_file``."""
    print(f"\nProcessing {len(files)} CSV file(s)...")
    df = concat_runs_with_unique_events(files)

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    df.to_feather(output_file)

    n_files = df["run"].nunique()
    n_events = int(df["evt"].nunique())
    n_particles = len(df)

    print("\n" + "=" * 60)
    print(f"Saved to:              {output_file}")
    print(f"Files saved:           {n_files}")
    print(f"Events saved (total):  {n_events}")
    print(f"Particles saved (total): {n_particles}")
    print("=" * 60)

    return df


def _expand(input_files: List[str], use_glob: bool) -> List[str]:
    if not use_glob:
        return input_files
    files: List[str] = []
    for pattern in input_files:
        matched = sorted(glob.glob(pattern))
        if matched:
            files.extend(matched)
            print(f"Pattern '{pattern}' matched {len(matched)} files")
        else:
            print(f"Warning: pattern '{pattern}' matched no files")
    return files


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Merge per-run reco_particles CSVs of a dataset into one Feather file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Explicit files
  %(prog)s run0.csv.zip run1.csv.zip -o dataset.feather

  # Glob pattern (mind the quotes so the shell does not expand it)
  %(prog)s "/data/dis_csv_2026_06/dis_nc_ep_9x130_q2_1to10/*.csv.zip" \\
      -o dis_nc_ep_9x130_q2_1to10.feather --glob
""",
    )
    parser.add_argument("input_files", nargs="+",
                        help="Input CSV/CSV.zip files, or glob patterns with --glob")
    parser.add_argument("-o", "--output", required=True, help="Output Feather file")
    parser.add_argument("--glob", action="store_true",
                        help="Treat input arguments as glob patterns")
    args = parser.parse_args()

    files = _expand(args.input_files, args.glob)
    if not files:
        print("Error: no files to process", file=sys.stderr)
        return 1

    merge_to_feather(files, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
