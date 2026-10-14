# EIC AI Background

Full-simulation pipelines and CSV-based machine-learning datasets for the
ePIC detector at the Electron-Ion Collider.

## What is this project?

This site documents the **EIC AI Background** project — a set of tools for producing
and consuming background-rich datasets from full ePIC detector simulations, with a focus
on use cases for AI / ML training and physics studies of detector occupancy.

The work has three pillars:

1. **Simulation pipeline** —
   [JeffersonLab/msf-simulation-pipeline](https://github.com/JeffersonLab/msf-simulation-pipeline),
   orchestration scripts that drive the ePIC simulation chain (`afterburner` → `npsim` →
   `EICrecon`) on the JLab farm and produce reconstructed `edm4eic` ROOT files for one or
   more beam-energy campaigns.
2. **CSV conversion** — [sroai/eic2ai](https://github.com/sroai/eic2ai), a single-pass
   C++ program that reads each ROOT file once and writes every CSV role (tracker hits,
   reco particles, DIS kinematics, …), each row carrying the linked `MCParticle` truth.
   It replaces the per-role ROOT macros in the pipeline's `csv_convert/`, with identical
   output; `40_csv_convert.py` drives either one.
3. **Analyses** — standalone Python analyses on the produced CSVs, kept in the archived
   [eic/ai-epic-background](https://github.com/eic/ai-epic-background/tree/main/analyses)
   repository.

The CSV output is deliberately simple so it can be consumed by Python, by LLM-generated
plotting scripts, or fed directly into a `torch.utils.data.Dataset` for ML training.

## Quick links

- [Full-Sim Pipeline overview](/ai-epic-background/full-sim-pipeline) — end-to-end ePIC simulation chain
  runnable on JLab SLURM with reproducible per-campaign configs.
- [Backgrounds](/ai-epic-background/background) — how signal events get mixed with the official ePIC
  background cocktails into 2 µs timeframes, with all the flags and references.
- [CSV Convert](/ai-epic-background/csv-convert) — lightweight C++/ROOT converter that turns edm4eic ROOT
  files into flat CSV with full hit, particle, and detector context.
- [AI / ML datasets](/ai-epic-background/ai-datasets) — tracker hits, MC truth, and detector tags packed
  into CSVs that load directly into pandas, numpy, or PyTorch dataloaders.
- [Available datasets](/ai-epic-background/data) — current background-mixed datasets on Rucio.
- [Data format](/ai-epic-background/data-format) — exact column layout produced by the converter.

## Pipeline at a glance

![HEPMC events → afterburner ROOT → edm4hep → edm4eic → CSV hits → AI/ML training and Python analysis](/diagrams/pipeline-overview.svg)

For the background-mixing step that sits between afterburner and `npsim`, see the
[Backgrounds](/ai-epic-background/background) page.

## Why CSV?

Tracker-hit CSVs are dead simple to produce in C++ (no extra dependencies beyond
`fmt::format`) and trivial to load anywhere downstream:

- `pandas.read_csv()` for exploration and plotting
- `numpy.loadtxt` / `pyarrow` for bulk numeric work
- A few lines of Python for `torch.utils.data.Dataset`
- LLM-generated analysis scripts, which work much more reliably on flat CSV than on
  EDM4EIC's PODIO graph

See the [Data Format](/ai-epic-background/data-format) page for the exact column layout produced by the
converter.

## Reproducibility

The entire chain is reproducible by design:

- Pinned `eic_xl` Singularity containers — every job runs in the same image.
- SLURM job arrays for every stage, including CSV conversion.
- One self-contained YAML campaign config per release, checked into the repo.

So any run can be re-executed at any time, against the exact container and detector
release it was originally produced with.

## Where the code lives

| What | Repository |
| ---- | ---------- |
| Simulation pipeline, campaign configs, CSV macros | [JeffersonLab/msf-simulation-pipeline](https://github.com/JeffersonLab/msf-simulation-pipeline) |
| `eic2ai` converter (submodule of the pipeline) | [sroai/eic2ai](https://github.com/sroai/eic2ai) |
| This website | [sroai/sroai.github.io](https://github.com/sroai/sroai.github.io) |
| Earlier analyses (archived) | [eic/ai-epic-background](https://github.com/eic/ai-epic-background) |

## Where to start

- New here? Start with the [Full-Sim Pipeline overview](/ai-epic-background/full-sim-pipeline).
- Want to know how backgrounds are mixed? Go to [Backgrounds](/ai-epic-background/background).
- Looking for the data itself? See [Available datasets](/ai-epic-background/data).
- Just want flat CSV out of an existing ROOT file? Jump to [CSV Convert](/ai-epic-background/csv-convert).
