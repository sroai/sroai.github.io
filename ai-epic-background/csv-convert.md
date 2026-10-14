# CSV Convert

::: tip eic2ai
The current converter is [eic2ai](https://github.com/sroai/eic2ai): one program reads each
ROOT file once and writes every role, with the same rows as the macros below and the unified
column names of [Data Format](/ai-epic-background/data-format). Select it per stage with
`converter: eic2ai` and `eic2ai_bin:` in the campaign config.
:::

`csv_convert/` (inside the [`simulation-pipeline`](/ai-epic-background/full-sim-pipeline) submodule)
is a set of **ROOT converter macros** that turn ePIC podio ROOT files into flat
CSV ready for analysis or ML training. There is one macro per *role* — one kind
of dump (reco particles, tracker hits, DIS kinematics, …) — rather than a single
monolithic converter.

## Naming convention

Every converter is named by the data model it reads:

- `edm4hep_*.cxx` — reads **edm4hep** (DD4hep / `npsim` output, sim level).
- `edm4eic_*.cxx` — reads **edm4eic** (`EICrecon` output, reco level).

The ROOT entry-point function inside each file has the **same name as the file**
(ROOT requires this for `root file.cxx(...)`), and each converter writes
`<input-stem>.<role>.csv`, where `<role>` is the macro name minus its
`edm4eic_` / `edm4hep_` prefix:

```
input:  msf_9x130_0001.edm4eic.root
macro:  edm4eic_reco_particles
output: msf_9x130_0001.reco_particles.csv   (+ .zip)
```

## Converters

| Macro | Reads | Output |
| --- | --- | --- |
| `edm4eic_reco_particles.cxx` | edm4eic | reco-particle dump (one row per particle) |
| `edm4eic_mc_particles.cxx` | edm4eic | MCParticle dump |
| `edm4eic_trk_hits.cxx` | edm4eic | tracker hit dump (one row per hit↔MCParticle association) |
| `edm4eic_calo_clusters.cxx` | edm4eic | calo cluster dump (one row per cluster↔MCParticle association, with `prt_origin`) |
| `edm4eic_mc_dis.cxx` | edm4eic | DIS invariants (one row per event, from `dis_*` params) |
| `edm4eic_reco_dis.cxx` | edm4eic | reconstructed DIS kinematics |
| `edm4eic_mcpart_lambda.cxx` | edm4eic | Λ MC-truth |
| `edm4eic_reco_ff_lambda.cxx` | edm4eic | Λ far-forward reco |
| `edm4hep_acceptance_ppim.cxx` | edm4hep | p·π⁻ acceptance (writes 3 CSVs: main + `*_pimin_hits` + `*_prot_hits`) |
| `edm4hep_acceptance_npi0.cxx` | edm4hep | n·π⁰ acceptance |
| `edm4hep_combinatorics_ppim.cxx` | edm4hep | p·π⁻ combinatorics |

See [Data Format](/ai-epic-background/data-format) for the exact column layout, using
`edm4eic_trk_hits` as the worked example.

## How converters are driven

You never wire these macros up by hand for a campaign. A single job generator,
`simulation_pipeline/40_csv_convert.py <stage>`, reads the stage's dataset cards
and emits one job per input ROOT file that runs exactly the macros the config's
`<stage>.macros` list names:

```yaml
csv_eicrecon:
  macros: [edm4eic_mc_dis, edm4eic_reco_particles, edm4eic_trk_hits]
```

`40_csv_convert.py csv_dd4hep` runs the `edm4hep_*` macros a config names;
`40_csv_convert.py csv_eicrecon` the `edm4eic_*` ones. The script is the same for
both — which data model is read is entirely the config's business. See
[Running the Converter](/ai-epic-background/csv-convert-running) and the
[Full-Sim Pipeline](/ai-epic-background/full-sim-pipeline).

## Pipeline

![.edm4eic.root / .edm4hep.root files → edm4*_*.cxx converter macros → .csv files → Python plots and AI/ML training](/diagrams/csv-convert-flow.svg)

## Why this design?

We use the **edm4eic** and **edm4hep** C++ libraries to read ePIC simulation data
because they provide convenient navigation between linked objects (hits →
particles → vertices) through PODIO relations.

We store the extracted data as **CSV** because:

1. **Easy to produce in C++** — just format and write lines, no extra dependencies.
2. **Easy to plot with Python** — `pandas.read_csv()` + matplotlib, especially convenient
   when an LLM is generating the plot code.
3. **Easy for AI / ML** — CSV loads directly into numpy, pandas, and PyTorch datasets.
4. **Easy for students** — no special libraries needed to inspect or work with the data.

## Continue reading

- [Running the Converter](/ai-epic-background/csv-convert-running) — run one macro by hand, or generate jobs for a whole campaign.
- [Batch on SLURM](/ai-epic-background/csv-convert-snakemake) — how CSV jobs are queued as SLURM arrays.
- [Data Format](/ai-epic-background/data-format) — exact column layout of the CSV.
