# EIC AI Background

Full-simulation pipeline, background mixing and CSV datasets for machine learning with
the ePIC detector at the Electron-Ion Collider.

## Scope

The project produces background-mixed ePIC simulations and converts them to flat CSV for
ML training and detector-occupancy studies. It has three parts:

1. **Simulation pipeline** —
   [JeffersonLab/msf-simulation-pipeline](https://github.com/JeffersonLab/msf-simulation-pipeline).
   Python scripts that generate SLURM job arrays for each stage of the ePIC chain
   (afterburner `abconv` → optional signal + background merge → `npsim` → `EICrecon` → CSV)
   on the JLab farm. Stages from the afterburner onward read dataset cards: YAML file lists
   made from a farm directory or, for official campaigns, from Rucio. One self-contained YAML config per
   campaign sets inputs, outputs, container image and converter roles.
2. **CSV conversion** — [sroai/eic2ai](https://github.com/sroai/eic2ai), a single-pass C++
   program (submodule of the pipeline). It reads each input once — the `.edm4eic.root` file
   and, for roles that need simulation hits, its paired `.edm4hep.root` — and writes every
   requested role
   (tracker hits, calorimeter hits, reco particles, DIS kinematics, …) as
   `<stem>.<role>.csv.zip`. It supersedes the per-role ROOT macros in the pipeline's
   `csv_convert/`: same rows, unified column names. `40_csv_convert.py` runs either one;
   a config selects eic2ai with `converter: eic2ai`, and the macros stay the default
   otherwise.
3. **Analyses** — earlier Python analyses on the CSVs, kept in the archived
   [eic/ai-epic-background](https://github.com/eic/ai-epic-background/tree/main/analyses)
   repository.

## Pipeline at a glance

```
generator HepMC
  → abconv (afterburner)        *.hepmc3.tree.root       stage 10
  → SignalBackgroundMerger      *.bg.hepmc3.tree.root    stage 11 (background campaigns)
  → npsim                       *.edm4hep.root           stage 20 / 22
  → EICrecon                    *.edm4eic.root           stage 30
  → eic2ai or csv_convert       <stem>.<role>.csv(.zip)  40_csv_convert.py
```

Stage 11 mixes each signal event with the official ePIC background cocktails
(synchrotron radiation; electron-beam bremsstrahlung, Coulomb and Touschek; proton beam
gas) into a 2 µs timeframe with the
`SignalBackgroundMerger` binary from [eic/HEPMC_Merger](https://github.com/eic/HEPMC_Merger).
EIC has since moved timeframe building to [eic/TimeframeBuilder](https://github.com/eic/TimeframeBuilder);
the pipeline has not switched. Details on the [Backgrounds](/ai-epic-background/background) page.

## Pages

- [Full-Sim Pipeline](/ai-epic-background/full-sim-pipeline) — stages, job creator and
  campaign configs.
- [Backgrounds](/ai-epic-background/background) — the merge step, cocktails and
  generator-status offsets.
- [CSV Convert](/ai-epic-background/csv-convert) — eic2ai and the ROOT macros, roles and
  how to run them.
- [Data Format](/ai-epic-background/data-format) — column layout of every CSV role.
- [Available Datasets](/ai-epic-background/data) — background-mixed datasets on Rucio.
- [AI / ML Datasets](/ai-epic-background/ai-datasets) — loading the CSVs in pandas, numpy
  and PyTorch.

## Repositories

| What | Repository |
| ---- | ---------- |
| Simulation pipeline, campaign configs, background cocktails, ROOT macros | [JeffersonLab/msf-simulation-pipeline](https://github.com/JeffersonLab/msf-simulation-pipeline) |
| `eic2ai` converter (submodule of the pipeline) | [sroai/eic2ai](https://github.com/sroai/eic2ai) |
| This website | [sroai/sroai.github.io](https://github.com/sroai/sroai.github.io) |
| Earlier analyses and documentation (archived) | [eic/ai-epic-background](https://github.com/eic/ai-epic-background) |
