# ai-epic-background

Background-rich datasets and full-simulation pipelines for the **ePIC** detector at
the Electron-Ion Collider — built for both physics analysis and AI / ML training.

📖 **[Documentation site](https://eic.github.io/ai-epic-background/)**

## What's in here

```
ai-epic-background/
├── csv_convert/          # ROOT (edm4eic) → CSV converter + Snakemake workflow
├── analyses/             # Python analyses on the CSVs (one subfolder per analysis)
├── full-sim-pipeline/    # ePIC simulation orchestration (afterburner → npsim → EICrecon)
├── docs/                 # VitePress documentation site (deployed to GitHub Pages)
└── .github/workflows/    # CI: builds and deploys docs on push to main
```

### `csv_convert/`

A small C++/ROOT converter, **`trk_hits_to_csv.cxx`**, that reads
`*.edm4eic.root` files and writes one CSV row per tracker-hit-association,
joining the reconstructed hit, the simulation hit, and the linked `MCParticle`.
Comes with a CMake build, a ROOT-macro entry point, a Snakemake workflow for
batch processing, and a JLab SLURM submission helper.

Quick start (inside the `eic_xl` container):

```bash
root -x -l -b -q 'trk_hits_to_csv.cxx("input.edm4eic.root", "output.csv")'
```

### `analyses/`

Python analyses that consume the produced CSVs. Each analysis lives in its own
subfolder with scripts and a short README. Currently:

- `analyses/time-vs-z-plots/` — per-event scatter plot of tracker hit time vs z,
  colored by `prt_gen_status`.

### `full-sim-pipeline/`

Python job-creation scripts that drive the ePIC simulation chain end-to-end on
the JLab SLURM farm. One YAML config per campaign; one Singularity-wrapped script
per input file; a SLURM submitter to launch them.

Stage scripts are numbered so the order is obvious:

```
01/02_root_hepmc_*_convert.py    # ROOT ↔ HEPMC normalisation
10_create_afterburner_jobs.py    # beam-effects afterburner
20_create_npsim_jobs.py          # Geant4 detector simulation
21_create_npsim_saveall_jobs.py  # …with all hits saved (background AI training)
30_create_eicrecon_jobs.py       # reconstruction
40_create_csv_dd4hep_jobs.py     # sim-level CSV
41_create_csv_eicrecon_jobs.py   # reco-level CSV
50/51_*_analysis_jobs.py         # analysis
```

### `docs/`

VitePress site with project-specific content covering the data format, the CSV
converter, the full-sim pipeline, and how to load the CSVs into pandas / PyTorch.
Local preview:

```bash
cd docs
npm install
npm run dev
```

## License

MIT — see `LICENSE`.

## Acknowledgements

This project bundles tooling originally developed in
[`eic/example-background-data`](https://github.com/eic/example-background-data) (the
CSV converter and Snakemake workflow) and in
[`JeffersonLab/meson-structure`](https://github.com/JeffersonLab/meson-structure)
(the full-simulation pipeline and VitePress docs scaffolding).
