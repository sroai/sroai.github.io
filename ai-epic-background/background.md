# Backgrounds in ePIC simulation

How signal events get mixed with the official ePIC beam backgrounds into
2 µs timeframes, which tool does it, and which flags matter downstream.

::: tip TL;DR
```
generator  →  abconv (afterburner)  →  SignalBackgroundMerger  →  npsim  →  eicrecon
   (rest frame)     (beam effects        (Poisson into 2 µs       (with status-
                     applied once)        timeframes, every         offset flags)
                                          source tagged with a
                                          generator-status offset)
```
This is the chain our pipeline runs (stages 10 → 11 → 22 → 30).
The current upstream mixer is [eic/TimeframeBuilder](https://github.com/eic/TimeframeBuilder)
(executable `timeframe_builder`); our stage 11 still calls the
`SignalBackgroundMerger` binary from [eic/HEPMC\_Merger](https://github.com/eic/HEPMC_Merger).
:::

## The big picture

Background-mixed simulation is built in three independent stages.

1. **Afterburner** — applies crossing angle and beam effects to the signal.
2. **Mixer** — takes one afterburned signal file and four or five background
   files and Poisson-samples them into 2 µs timeframes. Every background
   source's particles get a fixed *generator-status offset* added, so
   downstream code can tell what came from where.
3. **npsim** — runs Geant4 on the merged HepMC3. It needs extra flags that
   declare the shifted status codes (2001, 3001, …) as "stable, propagate" and
   (2002, 3002, …) as "decayed"; otherwise these particles are not handed to
   Geant4.

## Mixing tools

### TimeframeBuilder — current upstream

**Repo:** [eic/TimeframeBuilder](https://github.com/eic/TimeframeBuilder) ·
executable `timeframe_builder` · Spack package `timeframebuilder` ·
latest release v0.9.2 (2026-10-01)

Shipped in the `eic_xl` container from `v26.08.0-stable` on
([containers spack env](https://github.com/eic/containers/blob/master/spack-environment/xl/spack.yaml);
`master` pins `timeframebuilder@0.9.2`). Earlier images, including
`eic_xl:26.06.0-stable` and `26.07.x`, have only `SignalBackgroundMerger`.

Differences from SignalBackgroundMerger:

- inputs can be `.hepmc3.tree.root` (merge before simulation) or already
  simulated `.edm4hep.root` (merge hits after simulation, keeping
  particle–hit references); the output format follows the output file
  extension;
- per-source options for bunch-crossing time discretisation, attachment of
  background vertices to the beam (`beam_angle`, `beam_speed`) and Gaussian
  time spread (`beam_spread`);
- already merged timeframe files can be used as a source (`already_merged`),
  so overlays can be built step by step;
- CI compares EICrecon output for hepmc3-merged vs edm4hep-merged inputs
  ([capybara report](https://eic.github.io/TimeframeBuilder/capybara/main/index.html)).

Configuration is a YAML file, a CLI, or both (CLI overrides YAML). Abridged
from [`configs/config_epic_18x275.yml`](https://github.com/eic/TimeframeBuilder/tree/main/configs):

```yaml
timeframe_duration: 2000.0      # ns
bunch_crossing_period: 40.0     # ns
introduce_offsets: true
sources:
  - name: signal
    input_files: [signal.edm4hep.root]
    static_number_of_events: true
    static_events_per_timeframe: 1      # one signal per frame
    use_bunch_crossing: true
    generator_status_offset: 0
  - name: electron_beamgas_brems
    input_files: [ebrems.edm4hep.root]
    static_number_of_events: false
    mean_event_frequency: 0.00031694    # GHz = events/ns (316.94 kHz)
    use_bunch_crossing: true
    attach_to_beam: true
    beam_angle: -3.141592653589793      # rad
    beam_speed: 299.792458              # mm/ns
    beam_spread: 0.003                  # ns
    generator_status_offset: 3000
    repeat_on_eof: true
  # ... synrad, coulomb, touschek, hadron beam gas, bethe_heitler, minbias
```

Other per-source keys: `skip`, `keep_weight`, `tree_name`. Global keys:
`output_file`, `max_events`, `random_seed`, `writer`.

The same settings on the command line:

```bash
timeframe_builder --config config_epic_18x275.yml \
    -o merged.edm4hep.root -n 1000 --random-seed 42 \
    --source:signal:input_files signal.edm4hep.root \
    --source:ebrems:frequency 0.00031694 \
    --source:ebrems:status_offset 3000
```

Units differ from SignalBackgroundMerger: frequencies are in **events/ns
(GHz)**, so the cocktail value 316.94 kHz becomes `0.00031694`. The timeframe
length defaults to 2000 ns in the code (`MergerConfig.h`); the README table
still says 20 ns.

### SignalBackgroundMerger — what our pipeline runs

**Repo:** [eic/HEPMC\_Merger](https://github.com/eic/HEPMC_Merger) ·
executable `SignalBackgroundMerger` · Spack package `hepmcmerger`
(`@2.4.0` in current `eic_xl`). There is no separate
`eic/SignalBackgroundMerger` repository; the binary is built from HEPMC\_Merger.

For each timeframe (`--intWindow`, default 2000 ns) the merger:

- places exactly one signal event when `--signalFreq 0` (the default);
  a nonzero kHz value Poisson-samples the signal too, so some frames are pure
  background;
- draws each background source's event count from a Poisson with mean
  `freq × window`;
- distributes events uniformly in time inside the frame;
- adds the source's status offset to every particle's generator status;
- cycles a background file from its start when it reaches the end.

| Option | Meaning |
| ------ | ------- |
| `--signalFile` | Afterburned signal `.hepmc3.tree.root` |
| `--signalFreq` | Signal rate in kHz; `0` = one signal per frame |
| `--signalSkip` | Signal events to skip |
| `--signalStatus` | Status offset for the signal (campaigns use 0) |
| `--bgFile <file> <freq kHz> [skip] [status]` | One background source; repeatable |
| `--intWindow` | Timeframe length, ns (default 2000) |
| `--nSlices` | Number of timeframes (default 10000; `-1` = whole signal file) |
| `--rngSeed` | Random seed |
| `--outputFile` | Output file (default `bgmerged.hepmc3.tree.root`) |
| `--squashTime` | Integrate, but write no time information to vertices |

## Generator-status offsets

Two conventions are in use. The campaign cocktail JSONs, and our copies of
them, swap Coulomb and Touschek relative to the
[eic.github.io background\_mixed\_samples](https://github.com/eic/eic.github.io/blob/master/_resources/background_mixed_samples.md)
page and the TimeframeBuilder ePIC configs.

| Source         | Cocktail JSONs (our runs) | eic.github.io, TimeframeBuilder configs |
| -------------- | ------------------------: | --------------------------------------: |
| signal         |                         0 |                                       0 |
| synrad         |                      2000 |                                    2000 |
| ebrems         |                      3000 |                                    3000 |
| ecoulomb       |                      4000 |                                    5000 |
| etouschek      |                      5000 |                                    4000 |
| p-beam-gas     |                      6000 |                                    6000 |
| bethe\_heitler |                         — |                    7000 (TimeframeBuilder only) |
| minbias        |                         — |                       0 (TimeframeBuilder only) |

Stable code = offset + 1, decay code = offset + 2. To tell Coulomb from
Touschek in a given sample, read the cocktail JSON that produced it. The
eic2ai converter does not need the per-source value: its `prt_origin` treats
generator status 1–2 as signal and ≥ 1000 as background, and Geant4
secondaries inherit from their first generator ancestor
([data format](/ai-epic-background/data-format#signal-or-background-prt-origin)).

## Cocktails

**Upstream:** `config_data/*.json` in
[eic/simulation\_campaign\_datasets](https://github.com/eic/simulation_campaign_datasets/tree/main/config_data)
— one cocktail per beam energy / vacuum condition. Our copies live in
[`background_cocktails/`](https://github.com/JeffersonLab/msf-simulation-pipeline/tree/main/background_cocktails)
of the pipeline repo; they match upstream except for the XrootD host (ours
still point at `root://dtn-eic.jlab.org//volatile/eic/EPIC/...`, upstream at
`root://dtn2304.jlab.org:8443//jlab-osdf-ro/eic/EPIC/volatile/...`).

Each file is a list of sources:

```json
[
  {"file": "root://.../dataprod_rel_1.0.0_synrad_18x275_run001.preproc_10000repeats.hepmc3.tree.root",
   "freq": 3324000, "skip": 0.0, "status": 2000},
  {"file": "root://.../GETaLM1.0.0-1.1_ElectronBeamGas_18GeV_emin10keV_run001.hepmc3.tree.root",
   "freq": 316.94,  "skip": 0.0, "status": 3000},
  {"file": "root://.../dataprod_rel_1.0.1_electron_coulomb_18x275_10000Ahr.hepmc3.tree.root",
   "freq": 0.86,    "skip": 0.0, "status": 4000},
  {"file": "root://.../dataprod_rel_1.0.1_electron_touschek_18x275_10000Ahr.hepmc3.tree.root",
   "freq": 0.55,    "skip": 0.0, "status": 5000},
  {"file": "root://.../pythia8.306-1.0_ProtonBeamGas_275GeV_combined.hepmc3.tree.root",
   "freq": 22.5,    "skip": 0.0, "status": 6000}
]
```

| Field    | Meaning                                                                 |
| -------- | ----------------------------------------------------------------------- |
| `file`   | XrootD URL of a prepared background HepMC3.                             |
| `freq`   | Poisson rate in **kHz** (3 324 000 kHz = 3.3 GHz for synrad).           |
| `skip`   | Background events to skip before sampling. `0.0` in all current JSONs. |
| `status` | Generator-status offset added to every particle from this source.       |

Files with `hgas` in the name add the proton beam-gas source (status 6000).

## Merge commands

### Our pipeline (stage 11)

`simulation_pipeline/11_create_background_jobs.py` reads the cocktail named in
the config's `background_configs[energy]` and writes one job per afterburned
file:

```bash
SignalBackgroundMerger \
    --rngSeed      <md5 of the file basename> \
    --nSlices      <event_count> \
    --signalFile   <afterburned>.hepmc3.tree.root \
    --signalFreq   0 \
    --signalStatus 0 \
    --bgFile <synrad>   3324000 0 2000 \
    --bgFile <ebrems>    316.94 0 3000 \
    --bgFile <coulomb>     0.86 0 4000 \
    --bgFile <touschek>    0.55 0 5000 \
    --bgFile <p-gas>       22.5 0 6000 \
    --outputFile <afterburned>.bg.hepmc3.tree.root
```

- `--intWindow` is not passed; the 2000 ns default applies.
- `skip` comes from the JSON (0) and is cast to an integer —
  SignalBackgroundMerger only reads the 3rd and 4th `--bgFile` values when they
  are plain integers.
- With `strip_xrootd_prefix: true` the `root://host/` prefix is removed and the
  files are read from the local mount (`/volatile/eic/EPIC/EVGEN/BACKGROUNDS`
  on the JLab farm).
- `--signalSkip` is not passed: one job per afterburned file, read from its
  first event.

### ePIC campaigns (archived driver)

The campaign driver
[`scripts/run.sh`](https://github.com/eic/simulation_campaign_hepmc3/blob/main/scripts/run.sh)
in eic/simulation\_campaign\_hepmc3 (archived 2026-09) ran:

```bash
SignalBackgroundMerger \
    --rngSeed     <per-job seed> \
    --nSlices     <events_per_task> \
    --signalSkip  <events consumed by earlier tasks> \
    --signalFile  <afterburned signal>.hepmc3.tree.root \
    --signalFreq  ${SIGNAL_FREQ:-0} \
    --signalStatus ${SIGNAL_STATUS:-0} \
    --intWindow   2000 \
    --bgFile <file> <freq> <skip> <status>   # one per cocktail entry
    --outputFile  <task>.hepmc3.tree.root
```

Here the per-source `<skip>` ignores the JSON value: it is
`freq × window × task index` plus a seed-driven random offset, so parallel
tasks read decorrelated parts of the same background file.

## npsim with status-offset flags

DD4hep maps generator status 1 to stable and 2 to decayed, then looks codes it
does not know up in two extra sets; any other code is marked "other" and is
not handed to Geant4 as a primary. The sets are filled from the npsim CLI:

```bash
npsim ... \
    --runType                           batch \
    --hepmc3.useHepMC3                  true \
    --physics.alternativeStableStatuses "1 2001 3001 4001 5001 6001" \
    --physics.alternativeDecayStatuses  "2 2002 3002 4002 5002 6002" \
    --inputFiles                        merged.hepmc3.tree.root \
    --outputFile                        sim.edm4hep.root
```

Our stage 22 (`22_create_npsim_background_jobs.py`) and the campaign `run.sh`
both build these lists from the cocktail: `signalStatus + 1/2` plus
`status + 1/2` for every source. A four-source cocktail gives
`"1 2001 3001 4001 5001"`; `hgas` cocktails add `6001` / `6002`.

- The alternative sets only add codes; 1 and 2 are handled before them in
  `Geant4InputAction::setGeneratorStatus`. Listing `1` and `2` is harmless.
- `--hepmc3.useHepMC3` defaults to true when DD4hep is built with HepMC3;
  both scripts set it explicitly.
- `--runType batch` is used with `--inputFiles`; the campaign used
  `--runType run` only for particle-gun steering files.

The options are defined in DD4hep
[DDG4/python/DDSim/Helper/Physics.py](https://github.com/AIDASoft/DD4hep/blob/master/DDG4/python/DDSim/Helper/Physics.py)
and exposed unchanged on the npsim CLI. In a steering file:

```python
from DDSim.DD4hepSimulation import DD4hepSimulation
SIM = DD4hepSimulation()
SIM.physics.alternativeStableStatuses = {1, 2001, 3001, 4001, 5001}
SIM.physics.alternativeDecayStatuses  = {2, 2002, 3002, 4002, 5002}
SIM.hepmc3.useHepMC3 = True
```

## Where the code lives

| What                                          | Repo                                                                                                                                |
| --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Afterburner (`abconv`)                        | [eic/afterburner](https://github.com/eic/afterburner)                                                                               |
| Current timeframe mixer (`timeframe_builder`) | [eic/TimeframeBuilder](https://github.com/eic/TimeframeBuilder)                                                                     |
| Mixer used by our pipeline (`SignalBackgroundMerger`) | [eic/HEPMC\_Merger](https://github.com/eic/HEPMC_Merger)                                                                    |
| Cocktail JSONs + CSV chunk manifests          | [eic/simulation\_campaign\_datasets](https://github.com/eic/simulation_campaign_datasets)                                            |
| Our pipeline: stages 11 / 22, cocktail copies | [JeffersonLab/msf-simulation-pipeline](https://github.com/JeffersonLab/msf-simulation-pipeline)                                     |
| Campaign driver (`run.sh`), Rucio registration | [eic/simulation\_campaign\_hepmc3](https://github.com/eic/simulation_campaign_hepmc3) — archived 2026-09                          |
| Condor / Slurm submitters                     | [eic/job\_submission\_condor](https://github.com/eic/job_submission_condor), [eic/job\_submission\_slurm](https://github.com/eic/job_submission_slurm) — both archived |
| ePIC production docs (release tags, paths)    | [eic/epic-prod](https://github.com/eic/epic-prod)                                                                                   |
| Official background-mixed sample docs         | [eic/eic.github.io / background\_mixed\_samples](https://github.com/eic/eic.github.io/blob/master/_resources/background_mixed_samples.md) |
| Spack packages                                | `hepmcmerger`, `timeframebuilder` in [eic/eic-spack](https://github.com/eic/eic-spack)                                              |

## XrootD / Rucio access

The archived campaign driver wrote outputs to
`xroots://dtn2201.jlab.org//eic/eic2/EPIC/{RECO,FULL,LOG}/<release>/<detector>/...`
and registered them to Rucio under account `eicprod`, with metadata that
includes `is_background_mixed: true|false`. The `update-data-md` skill queries
Rucio with that flag to rebuild [Data](/ai-epic-background/data).

Mixed outputs of official campaigns can be browsed at the read endpoint used
by eic.github.io:

```
root://dtn2304.jlab.org:8443//jlab-osdf-ro/eic/EPIC/volatile/FULL/<release>/epic_craterlake/Bkg_1SignalPer2usFrame/...
root://dtn2304.jlab.org:8443//jlab-osdf-ro/eic/EPIC/volatile/RECO/<release>/epic_craterlake/Bkg_1SignalPer2usFrame/...
```

Other modes: `Bkg_RealisticSignalPer2usFrame` (signal Poisson-sampled) and
`Bkg_OnlyPer2usFrame` (background only). Increment `<release>` (e.g.
`25.06.1`) to find the latest campaign; RECO is kept for every campaign, FULL
not always.
