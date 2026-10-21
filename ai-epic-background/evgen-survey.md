# ePIC generator data survey

Which physics process exists at which beam energy, whether its files already
carry the 25 mrad crossing angle, how many events each holds, and how much
independent background the merged frames carry. Built from a read-only sweep of
`/volatile/eic/EPIC/EVGEN` on the JLab farm, with the crossing angle **measured**
on the beam momenta of 901 sampled files rather than inferred from path names.

**Date:** 2026-10-20 · **Scope:** 2,043 EVGEN directories, 45,647 files,
12.5 TiB. **~4.37 billion events in 48 process rows** are ready to feed to
`ddsim` with no afterburner step; ~4.66G in 58 rows counting head-on, LUND and
eic-smear sources. 18x275 and 10x100 are the only energies that are both large
and mixable.

See also [Available Datasets](/ai-epic-background/data) for the Rucio catalogue
of simulated campaigns, [CSV Datasets](/ai-epic-background/csv-datasets) for the
converted CSVs and [Backgrounds](/ai-epic-background/background) for the mixing
pipeline. The earlier survey, with the machine-background rate tables and
per-branch file listings this one drops, is kept at
[Generator Data Survey, 2026-10-15](/ai-epic-background/evgen-survey-full).

## 1. Marco's ML class table (slide 12, *Machine Learning Classes*)

Goal of the GNN, as stated on the slide: classification (Bkg vs Phy.) and
segmentation (attributed hits). Class definitions grouped as NC/CC DIS,
exclusive hadron, exclusive meson, photo-production.

|   # | Class                  | dir            | Physics Process                                                                            | Generator / source                   |
| --: | ---------------------- | -------------- | ------------------------------------------------------------------------------------------ | ------------------------------------ |
|   0 | Background             | `bkg`          | SynRad (2000), e-beam-gas/brems (3000), Coulomb (4000), Touschek (5000), p-beam-gas (6000) | dataprod / GETaLM / Xsuite / Pythia8 |
|   1 | NeutralCurrentDISQ1    | `ncdisq1`      | NC DIS, Q² ≥ 1                                                                             | Pythia8                              |
|   2 | NeutralCurrentDISQ10   | `ncdisq10`     | NC DIS, Q² ≥ 10                                                                            | Pythia8                              |
|   3 | NeutralCurrentDISQ100  | `ncdisq100`    | NC DIS, Q² ≥ 100                                                                           | Pythia8                              |
|   4 | NeutralCurrentDISQ1000 | `ncdisq1000`   | NC DIS, Q² ≥ 1000                                                                          | Pythia8                              |
|   5 | ChargedCurrentDISQ100  | `ccdisq100`    | CC DIS, Q² ≥ 100                                                                           | Pythia8                              |
|   6 | ChargedCurrentDISQ1000 | `ccdisq1000`   | CC DIS, Q² ≥ 1000                                                                          | Pythia8                              |
|   7 | DiffractiveDIS         | `ddis`         | Diffractive DIS, intact proton                                                             | RAPGAP                               |
|   8 | DVCS                   | `dvcs`         | Deeply Virtual Compton Scattering                                                          | DVCS generator                       |
|   9 | DDVCS                  | `ddvcs`        | Double DVCS (ep→eℓ⁺ℓ⁻p) — gated to BEAM=18x275                                             | EpIC (18x275/10x130 only)            |
|  10 | DVMP                   | `dvmp`         | Deeply Virtual Meson Production                                                            | EpIC                                 |
|  11 | DEMPQ3to10             | `dempq3to10`   | Deep Exclusive Meson Production, Q² ∈ [3,10]                                               | DEMPgen                              |
|  12 | DEMPQ10to20            | `dempq10to20`  | DEMP, Q² ∈ [10,20]                                                                         | DEMPgen                              |
|  13 | DEMPQ20to35            | `dempq20to35`  | DEMP, Q² ∈ [20,35]                                                                         | DEMPgen                              |
|  14 | TCS                    | `tcs`          | Timelike Compton Scattering                                                                | TCS generator                        |
|  15 | DiffractiveJPsi        | `jpsi`         | Diffractive J/ψ electroproduction, ep                                                      | lAger                                |
|  16 | JPsiPhotoproduction    | `jpsiphoto`    | Coherent J/ψ photoproduction — gated to BEAM=18x275                                        | eSTARlight (18x275 only)             |
|  17 | UChannelRho            | `urho`         | u-channel ρ exchange                                                                       | SLIGHT/GENEX                         |
|  18 | CoherentRho            | `cohrho`       | Coherent diffractive ρ off eAu (nuclear rapidity gap)                                      | Sartre                               |
|  19 | UChannelPi0            | `upi0`         | u-channel π⁰ exchange — gated to BEAM=18x275                                               | (18x275 only)                        |
|  20 | Upsilon                | `upsilon`      | Υ threshold production                                                                     | eSTARlight-family                    |
|  21 | MesonStructureFn       | `mesonsf`      | K⁺Λ exclusive meson structure function                                                     | eicMesonSFGen                        |
|  22 | CoherentPhi            | `cohphi`       | Coherent diffractive ϕ→K⁺K⁻ — off eAu (nuclear rapidity gap)                               | Sartre                               |
|  23 | Rho                    | `rho`          | Exclusive ρ→π⁺π⁻ electroproduction, ep, Q² ∈ [0,5] — npsim SIGSEGVs, unresolved            | SLIGHT                               |
|  24 | Spectroscopy           | `spectroscopy` | Exotic states X, Y, ψ(2S)                                                                  | dedicated spectroscopy generators    |
|  25 | Omega                  | `omega`        | ω neutral-decay photoproduction — gated to BEAM=18x275                                     | SLIGHT (18x275 only)                 |
|  26 | Photoproduction        | `photoprod`    | Min-bias photoproduction, Q² ∈ [0,1]                                                       | Pythia6-eic                          |

## 2. Processes with crossing-angle HepMC3 data

The tables to pick datasets from. A row qualifies when its files carry the
25 mrad crossing angle **measured** on the beams, so they are ready for `ddsim`
with no `abconv` step. Rows are keyed on **(process, collision system)** — `ep`,
`en`, `eD`, `eAu`, `eH2`, `eHe3`, `ePb` are not interchangeable — and energies
are the measured ones, which is why `SIDIS/pythia6/ep_5x41/hepmc_ip6` feeds both
the 5x41 and the 18x275 row: its file names carry the energy and both are
present in it.

> **Reading the event counts.** `k` = 10³, `M` = 10⁶, `G` = 10⁹ events. A
> `~` marks a count that was scaled rather than read file by file (section 4.2);
> without it every file of the branch was counted. `—` means not counted.

### 2.1 Events and processes per beam energy, crossing-angle data only

> **`mixable`** means all five machine-background sources for that energy are
> present on disk, so background can be added there today. 
> Only 10x100, 10x130, 10x275, 18x275 qualify; 
> 5x41 and 5x100 are short three files and the 9x points
> have no rate config at all. Energies in **bold** are the mixable ones.

| energy | processes with crossing-angle HepMC3 | events | mixable |
|---|---:|---:|---|
| 5x41 | 18 | ~1.43G | — |
| **18x275** | 24 | ~1.27G | yes |
| **10x100** | 27 | ~709M | yes |
| 5x100 | 6 | ~297M | — |
| 9x130 | 13 | ~158M | — |
| 9x275 | 15 | ~135M | — |
| 18x110 | 6 | ~97M | — |
| **10x275** | 4 | ~96M | yes |
| 18x108.41 | 2 | ~80M | — |
| **10x130** | 10 | ~51M | yes |
| 9x100 | 8 | ~42M | — |

**18x275 and 10x100 are the only energies that are both large and mixable.**
18x275 leads on events among them, 10x100 on breadth, and both can take
background today. 10x275 is mixable but carries only the DIS and SIDIS lines
(4 processes, ~96M events); its value is as a *second occupancy point* — SynRad
is 36.6 GHz there in vacuum against 3.3 GHz at 18x275 — rather than as a second
process set. 5x41 holds the largest event count of all, ~1.43G across 18
processes, with no background recipe, and the 9x points have no rate table at
all; both are worth asking for on the strength of the signal coverage already on
disk.

### 2.2 Process catalogue, crossing-angle data only

Events per energy are given inside the energy cell; the last column is the row
total.

> **Reading the event counts.** `k` = 10³, `M` = 10⁶, `G` = 10⁹ events. A
> `~` marks a count that was scaled rather than read file by file (section 4.2);
> without it every file of the branch was counted. `—` means not counted.

| process | system | energies with crossing-angle HepMC3 (events) | generator(s) | format | events |
|---|---|---|---|---|---:|
| CC DIS, Q² threshold | ep | 5x41 ~5.0M · 5x100 ~10.0M · **10x100** ~10M · **10x275** 10M · **18x275** 10M | Pythia8 (campaign) | root | ~45M |
| CC DIS, radiative, polarised | ep | 9x275 8.0M · **18x275** 4.0M | DJANGOH 4.6.10 | root | 12M |
| DEMP π⁺ / K⁺Λ / K⁺Σ⁰ | ep | 5x41 ~526M · 5x100 ~201M · 9x130 1.2M · 9x275 1.2M · **10x100** ~276M · **10x130** 2.1M · **18x275** ~108M | DEMPgen | ascii.gz, root | ~1.12G |
| DVCS | ep | 5x41 ~5.5M · **10x100** 2.0M · **18x275** 2.0M | DVCS gen (legacy) | root | ~9.5M |
| DVCS + BH + INT | ep | 5x41 2.0M · **10x100** 2.6M · **10x130** 4.6M · **18x275** 2.0M | EpIC 1.1.6 | root | 11M |
| DVCS / BH / interference | ep | 9x130 12M · 9x275 30M | EpIC 1.1.8 | root | 42M |
| DVCS on deuteron | eD | 5x41 ~6.3M · **10x100** ~6.0M | EpIC | ascii, ascii.gz | ~12M |
| DVMP / Υ (lAger legacy) | ep | **10x100** ~1.2M | lAger | ascii.gz | ~1.2M |
| DVMP J/ψ→μ⁺μ⁻ | ep | 9x130 22k · 9x275 80k · **10x130** 2.7M · **18x275** 5.3M | lAger | root | 8.2M |
| DVMP π⁰ | ep | 5x41 1.0M · 9x130 1.0M · 9x275 2.0M · **10x100** 100k · **10x130** 1.0M · **18x275** 1.0M | EpIC | root | 6.1M |
| NC DIS, Q² threshold | ep | 5x41 ~23M · 5x100 ~20M · **10x100** ~20M · **10x275** ~20M · **18x275** ~26M | Pythia8 (campaign) | ascii, root | ~109M |
| NC DIS, inclusive | ep | 5x41 ~15M · 5x100 ~16M · 9x130 ~16M · 9x275 ~16M · **10x100** ~16M · **10x130** 16M · **10x275** ~16M · **18x275** ~16M | Pythia6.428, Pythia8.316 | root | ~126M |
| NC DIS, inclusive (EEEMCal cfg) | ep | 9x275 1.0M | Pythia8.315 | root | 1.0M |
| NC/CC DIS, radiative | ep | **18x275** 3.0M | DJANGOH 4.6.21 | root | 3.0M |
| SIDIS / min-bias photoprod. | en | 5x41 130M · **10x100** 135M · **18x275** 95M | Pythia6-eic | root | 360M |
| SIDIS / min-bias photoprod. | ep | 5x41 ~286M · 5x100 50M · 9x130 37M · 9x275 39M · **10x100** 113M · **10x275** 50M · **18x275** ~264M | Pythia6-eic | root | ~838M |
| SIDIS D_s | ep | 9x275 ~1.0M | Pythia8 HFsim | root | ~1.0M |
| SIDIS D_s (eA) | eAu | 9x100 ~658k | BeAGLE HFsim | root | ~658k |
| SIDIS dijet (PGF) | ep | **18x275** 400k | Pythia6.428 dijet | root | 400k |
| SIDIS inclusive (Pythia6+LHAPDF) | ep | 9x130 50M | Pythia6-eic + LHAPDF | root | 50M |
| SIDIS open charm D⁰ | ep | 5x41 ~897k · 9x130 ~1.2M · 9x275 ~987k · **10x100** ~2.0M · **10x130** ~1.1M · **18x275** ~1.4M | Pythia8, Pythia8 HFsim | root | ~7.5M |
| SIDIS open charm D⁰ (eA) | eAu | 5x41 ~1.2M · 9x100 ~975k · **10x100** ~1.5M | BeAGLE HFsim | root | ~3.7M |
| SIDIS Λ | ep | **18x275** ~6.4M | Pythia8.306 | root | ~6.4M |
| SIDIS Λ_c | ep | 9x275 ~761k · **10x100** ~761k | Pythia8 HFsim | root | ~1.5M |
| SIDIS Λ_c (eA) | eAu | 9x100 ~469k · **10x100** ~1.2M | BeAGLE HFsim | root | ~1.7M |
| SIDIS, Q²-binned | ep | 5x41 402M · **10x100** ~67M · **18x275** ~707M | Pythia6 (IP6 era) | root | ~1.18G |
| TCS + BH interference | ep | 5x41 ~5.8M · **10x100** ~8.1M · **18x275** ~6.0M | TCS gen | root | ~20M |
| coherent J/ψ photoproduction | ep | **18x275** 2.0M | eSTARlight | root | 2.0M |
| coherent φ→K⁺K⁻, eA | eAu | 9x100 10M · **10x100** 6.9M · 18x110 ~34M | Sartre | root | ~51M |
| coherent/incoherent J/ψ, eA | eAu | 18x110 ~20M | Sartre | root | ~20M |
| coherent/incoherent ρ, eA | eAu | 9x100 10M · **10x100** 10M · 18x110 ~20M | Sartre | ascii.gz, root | ~40M |
| diffractive DIS | ep | 9x130 4.0M · 9x275 4.0M · **10x100** 5.0M | RAPGAP 3.310 | root | 13M |
| diffractive J/ψ, ePb | ePb | 18x108.41 ~14M | BeAGLE | ascii, root | ~14M |
| diffractive J/ψ, ep | ep | 5x41 66k · 5x100 118k · 9x130 19k · 9x275 69k · **10x100** 174k · **10x130** 199k · **18x275** 379k | lAger | root | 1.0M |
| diffractive φ, eA | eAu | 18x110 ~50k | Sartre/BeAGLE, eSTARlight | ascii | ~50k |
| diffractive φ, ePb/eAu | eAu | 9x100 5.0M · **10x100** 2.0M · 18x110 20M | BeAGLE | root | 27M |
| diffractive φ, ePb/eAu | ePb | 18x108.41 ~66M | BeAGLE | ascii, root | ~66M |
| double DVCS | ep | **10x130** 2.0M · **18x275** 4.0M | EpIC | root | 6.0M |
| exclusive ρ→π⁺π⁻ | ep | **10x100** ~803k | SLIGHT | ascii.gz | ~803k |
| inclusive eA DIS | eAu | 5x41 20M · 9x100 ~14M · **10x100** 20M | BeAGLE | root | ~54M |
| inclusive eA DIS | eH2 | 9x130 20M · **10x130** 21M | BeAGLE | root | 41M |
| inclusive eA DIS | eHe3 | 5x41 3.0M · 18x110 3.0M | BeAGLE | root | 6.0M |
| meson structure function K⁺Λ | ep | 5x41 1.0M · 9x100 1.0M · 9x130 1.0M · 9x275 1.0M · **10x100** 1.0M · **10x130** 1.0M · **18x275** 1.0M | eicMesonSFGen | root | 7.0M |
| spectroscopy ψ(2S)/X/Y | ep | **10x100** ~1.5M | dedicated | ascii, ascii.gz | ~1.5M |
| u-channel π⁰ | ep | **18x275** 100k | SLIGHT | root | 100k |
| u-channel ρ | ep | **10x100** 100k | SLIGHT/GENEX | root | 100k |
| Υ(1S/2S/3S) threshold | ep | 9x130 15M · 9x275 30M · **18x275** ~150k | eSTARlight 1.3.0 | root | ~45M |
| ω photoproduction | ep | **18x275** ~804k | SLIGHT | ascii.gz | ~804k |


Several processes exist in more than one collision system with different energy
coverage — `inclusive eA DIS` splits across eAu / eH2 / eHe3, `diffractive φ`
across eAu / ePb, and `SIDIS min-bias photoproduction` has an `en`
(electron–neutron) variant alongside `ep`. Those are not interchangeable, so
they stay as separate rows.

### 2.3 Coverage including degraded sources

Same rows, no longer restricted to ready-to-use data. Each energy carries a
marker for the **best source available at that energy**, and the events are
those of that best source only — a head-on copy of data that also exists
afterburned is not added on top.

| marker | the data is | what it costs to use |
|---|---|---|
| *(none)* | crossing-angle HepMC3 on `/volatile` | nothing — feed to `ddsim` |
| `(R)` | only in `RECO`, as `MCParticles` | needs an `MCParticles`→HepMC3 converter, which does not exist yet; the crossing angle is already applied. No cell carries this marker any more — see below |
| `(h)` | only head-on HepMC3 | needs `abconv` first — head-on beams cannot go into `ddsim` |
| `(L)` | only in LUND or eic-smear format | needs a format conversion |
| `(?)` | present, beams not determined | needs inspection |

A marker describes the *best* option for that branch family, so a plain energy
may also have head-on or `RECO` copies. Energies in **bold** are the mixable
ones (legend in 2.1).

> **Reading the event counts.** `k` = 10³, `M` = 10⁶, `G` = 10⁹ events. A
> `~` marks a count that was scaled rather than read file by file (section 4.2);
> without it every file of the branch was counted. `—` means not counted.

| process                          | sys  | energies, by best available source (events)                                                                             | generator(s)              | events |
| -------------------------------- | ---- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------- | -----: |
| CC DIS, Q² threshold             | ep   | 5x41 ~5.0M · 5x100 ~10.0M · **10x100** ~10M · **10x275** 10M · **18x275** 10M                                           | Pythia8 (campaign)        |   ~45M |
| CC DIS, radiative (eRHIC fmt)    | eD   | 18x137 (?) ~8.1M                                                                                                        | DJANGOH/eRHIC             |  ~8.1M |
| CC DIS, radiative (eRHIC fmt)    | ep   | **18x275** (h) ~11M                                                                                                     | DJANGOH/eRHIC             |   ~11M |
| CC DIS, radiative, polarised     | ep   | 9x275 8.0M · **18x275** 4.0M                                                                                            | DJANGOH 4.6.10            |    12M |
| DEMP K⁺Λ / K⁺Σ (LUND fmt)        | ep   | 5x41 (L) ~14M                                                                                                           | DEMPgen (legacy)          |   ~14M |
| DEMP π⁺ / K⁺Λ / K⁺Σ⁰             | ep   | 5x41 ~526M · 5x100 ~201M · 9x130 1.2M · 9x275 1.2M · **10x100** ~276M · **10x130** 2.1M · **18x275** ~108M              | DEMPgen                   | ~1.12G |
| DVCS                             | ep   | 5x41 ~5.5M · **10x100** 2.0M · **18x275** 2.0M                                                                          | DVCS gen (legacy)         |  ~9.5M |
| DVCS + BH + INT                  | ep   | 5x41 2.0M · **10x100** 2.6M · **10x130** 4.6M · **18x275** 2.0M                                                         | EpIC 1.1.6                |    11M |
| DVCS + BH + INT, coherent        | ep   | **18x275** (h) ~1.0M                                                                                                    | EpIC                      |  ~1.0M |
| DVCS / BH / interference         | ep   | 9x130 12M · 9x275 30M                                                                                                   | EpIC 1.1.8                |    42M |
| DVCS on deuteron                 | eD   | 5x41 ~6.3M · **10x100** ~6.0M                                                                                           | EpIC                      |   ~12M |
| DVMP / Υ (lAger legacy)          | ep   | **10x100** ~1.2M                                                                                                        | lAger                     |  ~1.2M |
| DVMP J/ψ→μ⁺μ⁻                    | ep   | 9x130 22k · 9x275 80k · **10x130** 2.7M · **18x275** 5.3M                                                               | lAger                     |   8.2M |
| DVMP π⁰                          | ep   | 5x41 1.0M · 9x130 1.0M · 9x275 2.0M · **10x100** 100k · **10x130** 1.0M · **18x275** 1.0M                               | EpIC                      |   6.1M |
| NC DIS, Q² threshold             | ep   | 5x41 ~23M · 5x100 ~20M · **10x100** ~20M · **10x275** ~20M · **18x275** ~26M                                            | Pythia8 (campaign)        |  ~109M |
| NC DIS, inclusive                | ep   | 5x41 ~15M · 5x100 ~16M · 9x130 ~16M · 9x275 ~16M · **10x100** ~16M · **10x130** 16M · **10x275** ~16M · **18x275** ~16M | Pythia6.428, Pythia8.316  |  ~126M |
| NC DIS, inclusive (EEEMCal cfg)  | ep   | 9x275 1.0M                                                                                                              | Pythia8.315               |   1.0M |
| NC/CC DIS, radiative             | ep   | **18x275** 3.0M                                                                                                         | DJANGOH 4.6.21            |   3.0M |
| SIDIS / min-bias photoprod.      | en   | 5x41 130M · **10x100** 135M · **18x275** 95M                                                                            | Pythia6-eic               |   360M |
| SIDIS / min-bias photoprod.      | ep   | 5x41 ~286M · 5x100 50M · 9x130 37M · 9x275 39M · **10x100** 113M · **10x275** 50M · **18x275** ~264M                    | Pythia6-eic               |  ~838M |
| SIDIS D_s                        | ep   | 9x275 ~1.0M                                                                                                             | Pythia8 HFsim             |  ~1.0M |
| SIDIS D_s (eA)                   | eAu  | 9x100 ~658k                                                                                                             | BeAGLE HFsim              |  ~658k |
| SIDIS dijet (PGF)                | ep   | **18x275** 400k                                                                                                         | Pythia6.428 dijet         |   400k |
| SIDIS inclusive (Pythia6+LHAPDF) | ep   | 9x130 50M                                                                                                               | Pythia6-eic + LHAPDF      |    50M |
| SIDIS open charm D⁰              | ep   | 5x41 ~897k · 9x130 ~1.2M · 9x275 ~987k · **10x100** ~2.0M · **10x130** ~1.1M · **18x275** ~1.4M                         | Pythia8, Pythia8 HFsim    |  ~7.5M |
| SIDIS open charm D⁰ (eA)         | eAu  | 5x41 ~1.2M · 9x100 ~975k · **10x100** ~1.5M                                                                             | BeAGLE HFsim              |  ~3.7M |
| SIDIS Λ                          | ep   | **18x275** ~6.4M                                                                                                        | Pythia8.306               |  ~6.4M |
| SIDIS Λ_c                        | ep   | 9x275 ~761k · **10x100** ~761k                                                                                          | Pythia8 HFsim             |  ~1.5M |
| SIDIS Λ_c (eA)                   | eAu  | 9x100 ~469k · **10x100** ~1.2M                                                                                          | BeAGLE HFsim              |  ~1.7M |
| SIDIS, Q²-binned                 | ep   | 5x41 402M · **10x100** ~67M · 18x100 (L) 120M · **18x275** ~707M                                                        | Pythia6 (IP6 era)         | ~1.30G |
| TCS + BH interference            | ep   | 5x41 ~5.8M · **10x100** ~8.1M · **18x275** ~6.0M                                                                        | TCS gen                   |   ~20M |
| TCS, pure                        | ep   | 5x41 (h) ~20M · 5x100 (h) ~20M · **10x100** (h) ~20M · **18x275** (h) ~20M                                              | TCS gen                   |   ~80M |
| coherent J/ψ photoproduction     | ep   | **18x275** 2.0M                                                                                                         | eSTARlight                |   2.0M |
| coherent ρ, eA                   | eAu  | 18x110 (h) ~20M                                                                                                         | Sartre                    |   ~20M |
| coherent φ→K⁺K⁻, eA              | eAu  | 9x100 10M · **10x100** 6.9M · 18x110 ~34M                                                                               | Sartre                    |   ~51M |
| coherent/incoherent J/ψ, eA      | eAu  | 18x110 ~20M                                                                                                             | Sartre                    |   ~20M |
| coherent/incoherent ρ, eA        | eAu  | 9x100 10M · **10x100** 10M · 18x110 ~20M                                                                                | Sartre                    |   ~40M |
| diffractive DIS                  | ep   | 9x130 4.0M · 9x275 4.0M · **10x100** 5.0M                                                                               | RAPGAP 3.310              |    13M |
| diffractive J/ψ, eA              | eAu  | 18x110 (h) ~20M                                                                                                         | Sartre                    |   ~20M |
| diffractive J/ψ, ePb             | ePb  | 18x108.41 ~14M                                                                                                          | BeAGLE                    |   ~14M |
| diffractive J/ψ, ep              | ep   | 5x41 66k · 5x100 118k · 9x130 19k · 9x275 69k · **10x100** 174k · **10x130** 199k · **18x275** 379k                     | lAger                     |   1.0M |
| diffractive φ, eA                | eA   | 18x110 (h) ~20M                                                                                                         | Sartre/BeAGLE             |   ~20M |
| diffractive φ, eA                | eAu  | 18x110 ~50k                                                                                                             | Sartre/BeAGLE, eSTARlight |   ~50k |
| diffractive φ, ePb/eAu           | eAu  | 9x100 5.0M · **10x100** 2.0M · 18x110 20M                                                                               | BeAGLE                    |    27M |
| diffractive φ, ePb/eAu           | ePb  | 18x108.41 ~66M                                                                                                          | BeAGLE                    |   ~66M |
| double DVCS                      | ep   | **10x130** 2.0M · **18x275** 4.0M                                                                                       | EpIC                      |   6.0M |
| exclusive ρ→π⁺π⁻                 | ep   | **10x100** ~803k · **18x275** (?) ~1.0M                                                                                 | SLIGHT                    |  ~1.8M |
| inclusive eA DIS                 | eAu  | 5x41 20M · 9x100 ~14M · **10x100** 20M                                                                                  | BeAGLE                    |   ~54M |
| inclusive eA DIS                 | eH2  | 9x130 20M · **10x130** 21M                                                                                              | BeAGLE                    |    41M |
| inclusive eA DIS                 | eHe3 | 5x41 3.0M · 18x110 3.0M                                                                                                 | BeAGLE                    |   6.0M |
| meson structure function K⁺Λ     | ep   | 5x41 1.0M · 9x100 1.0M · 9x130 1.0M · 9x275 1.0M · **10x100** 1.0M · **10x130** 1.0M · **18x275** 1.0M                  | eicMesonSFGen             |   7.0M |
| spectroscopy ψ(2S)/X/Y           | ep   | 5x100 (?) ~437k · **10x100** ~1.5M                                                                                      | dedicated                 |  ~1.9M |
| u-channel π⁰                     | ep   | **18x275** 100k                                                                                                         | SLIGHT                    |   100k |
| u-channel ρ                      | ep   | **10x100** 100k                                                                                                         | SLIGHT/GENEX              |   100k |
| u-channel ω (neutral decay)      | ep   | **18x275** (h) ~198k                                                                                                    | SLIGHT                    |  ~198k |
| Υ photoproduction (legacy)       | ep   | ? (h) ~15k                                                                                                              | eSTARlight                |   ~15k |
| Υ(1S/2S/3S) threshold            | ep   | 9x130 15M · 9x275 30M · **18x275** ~150k                                                                                | eSTARlight 1.3.0          |   ~45M |
| ω photoproduction                | ep   | **18x275** ~804k                                                                                                        | SLIGHT                    |  ~804k |

**Totals: ~4.66G events in 58 rows.** Cells by source:
133 ready, 0 `RECO`-only,
11 head-on-only, 2 needing a format
conversion, 3 undetermined.

**What the `RECO` route adds: durability, not coverage.** The 2026-10-15 survey
found exactly one (process, system, energy) combination that existed only as
`MCParticles` in a background-free `RECO` campaign — inclusive eA DIS, eHe3,
18x110. It has crossing-angle HepMC3 after all:
`DIS/BeAGLE1.03.02-1.2/eHe3/18x110` holds 3 afterburned files (3M events,
measured 25.014 mrad), which that survey had filed under 5x41 because its eHe3
row collapsed the four energies of this branch into one. So no cell here needs
`RECO` for coverage. `RECO` is still the durable copy — `RECO/26.07.1` is
tape-backed where most of EVGEN is `/volatile`-only — and the recipe for reading
`MCParticles` back out is in the
[2026-10-15 survey](/ai-epic-background/evgen-survey-full), section 5.6.

### 2.4 Events and processes per beam energy, all sources

Section 2.1 counted only ready-to-use data. This counts a process at an energy
if it is reachable **at all** — ready, via `RECO`, via `abconv`, or via a format
conversion — and the events are again those of the best source per cell.

> **`mixable`** means all five machine-background sources for that energy are
> present on disk, so background can be added there today — SynRad (status
> 2000), electron beam gas + brems (3000), Coulomb (4000), Touschek (5000) and
> proton beam gas (6000), as listed in the campaign's
> `config_data/…hgas_<E>_<pipe>….json`. It says nothing about the signal data;
> it is purely whether background can be mixed in. Only 10x100, 10x130, 10x275
> and 18x275 qualify; 5x41 and 5x100 are short three files and the 9x points
> have no rate config at all. Energies in **bold** are the mixable ones.

> **Reading the event counts.** `k` = 10³, `M` = 10⁶, `G` = 10⁹ events. A
> `~` marks a count that was scaled rather than read file by file (section 4.2);
> without it every file of the branch was counted. `—` means not counted.

| energy | processes, any source | events | ready | `(R)` | `(h)` | `(L)` | `(?)` | mixable |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 5x41 | 20 | ~1.47G | 18 | — | 1 | 1 | — | — |
| **18x275** | 29 | ~1.30G | 24 | — | 4 | — | 1 | yes |
| **10x100** | 28 | ~729M | 27 | — | 1 | — | — | yes |
| 5x100 | 8 | ~318M | 6 | — | 1 | — | 1 | — |
| 9x130 | 13 | ~158M | 13 | — | — | — | — | — |
| 18x110 | 9 | ~157M | 6 | — | 3 | — | — | — |
| 9x275 | 15 | ~135M | 15 | — | — | — | — | — |
| 18x100 | 1 | 120M | — | — | — | 1 | — | — |
| **10x275** | 4 | ~96M | 4 | — | — | — | — | yes |
| 18x108.41 | 2 | ~80M | 2 | — | — | — | — | — |
| **10x130** | 10 | ~51M | 10 | — | — | — | — | yes |
| 9x100 | 8 | ~42M | 8 | — | — | — | — | — |
| 18x137 | 1 | ~8.1M | — | — | — | — | 1 | — |
| ? | 1 | ~15k | — | — | 1 | — | — | — |
| **total** | **149** | **~4.66G** | **133** | **0** | **11** | **2** | **3** | |

The ordering barely moves against 2.1: 18x275 and 10x100 stay first and third
and stay the only large-and-mixable pair. What the extra sources buy is small
and concentrated — 18x110 gains three Sartre eA head-on samples, 18x275 gains
four head-on rows, and 18x100 exists only as
eic-smear-format Pythia6 output (120M events), which is the single largest
block of data behind a format conversion. `?` is `EXCLUSIVE/UPSILON`, a legacy Υ
photoproduction sample whose only recorded beam is a ~0.4 GeV virtual photon, so
no configuration can be read off it; `18x137` is eD
(`erhic-cc-yrad-floff_eD_18_137_*`) and `18x108.41` is the BeAGLE ePb
production.

---

## 3. Background statistics in the merged training frames

Measured 2026-10-01 on the merged, simulated frames themselves —
`/data/msf-2026-06/dd4hep-background/18x275/k_lambda_18x275_5000evt_{0022,0023}.edm4hep.root`,
107 files x 5,000 frames of 2 us. Background particles are identified by their
`generatorStatus` band — the band per source is in Marco's class table,
section 1. Geant4 secondaries carry status 0, and merging shifts only `time`, so
a particle's generator momentum and vertex survive simulation unchanged and
identify the source event.

### 3.1 What one frame holds

| band | source | per frame |
|---|---|---|
| 2000 | SynRad | 53,300 photons from 26,653 events (2 photons per event, equal momentum), times uniform over 0-2000 ns |
| 3000 | e-beam-gas | 12-48 particles from 9-33 events |
| 4000 / 5000 / 6000 | Coulomb / Touschek / p-beam-gas | none in the 10 frames read, as expected at <= 0.05 events per frame |

> **Rate check.** 26,653 SynRad events per 2,000 ns is 13.33 GHz, which is the
> **gold-coated** 13.277 GHz rate of the 10x275 cocktail family.
> The 18x275 cocktail in
> `simulation-pipeline/background_cocktails/` carries 3.324 GHz, i.e. 6,648 per
> frame, so the merge that produced these files used a different recipe than
> that file. Settle the provenance before quoting an occupancy from them.

### 3.2 The SynRad pool cycles every ~125 frames

Share of frame 0's distinct SynRad momenta that reappears in a later frame of
the same file:

| frame | 1-124 | 125 | 126 | 250 | 251 | 375 | 376 |
|---|---|---|---|---|---|---|---|
| shared with frame 0 | 0% | 59.4% | 40.6% | 19.5% | 80.6% | 0% | 68.5% |

Period 125.4 frames x 26,653 events = **~3.34 million SynRad events in the
pool**, about 90 bytes per event in the 286.8 MiB input, which is consistent.
One 5,000-frame output file therefore cycles the pool ~40 times, and the
107-file set uses each SynRad event ~4,300 times. The 0.4-frame slip per cycle
is the random walk of the read pointer driven by the per-frame Poisson count.

### 3.3 Frame k carries the same background in every file

Share of SynRad vertices common to files 0022 and 0023 at the same frame index:

| frame | 0 | 1 | 2 | 10 | 100 | 1000 | 4999 |
|---|---|---|---|---|---|---|---|
| shared | 100% | 99.96% | 99.7% | 95.5% | 96.0% | 67.3% | 53.7% |

Every `--bgFile` entry of the cocktail JSON carries `skip = 0`, and the job
generator passes it through while varying only `--rngSeed` per output file. The
seed changes the Poisson counts and the placement times, so the read pointer
random-walks around the same position in the pool instead of starting
elsewhere.

### 3.4 What that means

**The pool is the ceiling.** 3.34M SynRad events at the rate used here is
**250 us of machine background** (1.0 ms at the 18x275 cocktail's 3.324 GHz),
which supports 125 disjoint 2 us frames and no more. The reads already walk all
125, and the tiles are fair samples of the pool rather than stretches of
beamline: frames 0, 60, 100 and 3000 agree on the `vertex.z` histogram to 0.1%,
on mean cos(theta) (-0.29) and on mean photon energy (27 keV). So the input file
is in random order, and reordering the reads, randomising `skip` per job or
drawing random pool indices adds no background content. The cross-file replay
in 3.3 wastes nothing; it only decides which file carries which tile.

**Geant4 supplies the independence the pool cannot.** Each tile is re-simulated
with its own seed, ~4,300 times across the set, and the resulting hit patterns
are independent: frame 0 of 0022 and frame 0 of 0023 hold identical SynRad
generator content and share **0 of 6,566** `EcalBarrelScFiHits`. A network that
sees hits therefore gets genuinely distinct images even where the generator
events repeat. Merging after Geant4 (TimeframeBuilder's edm4hep path) gives
that axis up, which is the main physics argument for keeping SynRad merged
before simulation.

**Two things the small pool costs.**

- *No unseen background in any split.* Frame-level train/val/test splits all
  draw from the same 125 tiles, so a measured rejection or recall is
  conditioned on this one SynRad realization. A clean generalisation number
  needs a pool partition: reserve a tile range for validation and test through
  per-source `skip` windows with `nSlices` short enough to stay inside the
  window. A 12-tile window means at most 12 frames per merge job, so the held
  out sets need many small jobs with different signal chunks.
- *Error bars.* The composition component of background variance has effective
  N ~ 125; a frame-level bootstrap over the full frame count measures the
  shower component only.

**What would actually add background information.** More SynRad generator
events. The input is a 287 MiB file, so an order of magnitude more is a modest
request to the machine-background production rather than anything the merging
step can supply. Short of that, the vacuum / gold-coating pair (2.76x SynRad
with the other four sources unchanged) and the other beam energies
are the available robustness probes.

> **Both mergers read sequentially.** `SignalBackgroundMerger` (eic/HEPMC_Merger)
> consumes each background file in order and reopens it at EOF;
> eic/TimeframeBuilder advances a per-source entry index with no shuffle
> (`src/DataHandler.cc`), and in its EDM4hep path the index is never wrapped, so
> `repeat_on_eof` silently repeats one stale event past the end of the pool.
> Neither tool changes the statistics described above.


---

## 4. How the numbers were measured

### 4.1 The sweep

All of it read-only on the data, from an `ifarm2401.jlab.org` login, on
2026-10-20:

```bash
find /volatile/eic/EPIC/EVGEN -maxdepth 10 -type d          # 2,043 directories
find "$d" -maxdepth 1 -type f -printf '%s\t%f\n'            # every file, with its size
```

That gives 45,647 files in 1,271 directories holding data, 12.5 TiB in all,
including the machine-background and single-particle trees that these tables do
not cover. Reads of file contents go through the `eic_xl` image
(`/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:nightly`, bound
`-B /volatile:/volatile:ro` with a writable `TMPDIR`). The only writes anywhere on the farm were a few kB of helper scripts under
`/tmp`, removed afterwards.

### 4.2 Event counting

A **branch** is one (directory prefix, beam energy) production; a **cell** is one
(process, system, energy). Counting runs per directory and format group:

- **HepMC3 ROOT** (`.hepmc3.tree.root`): the entry count of `hepmc3_tree`, read
  from the first and the last file of the group. When the two agree — these
  productions write a fixed number of events per file — the group is
  `entries × files` and the count is **exact**. When they differ the group is
  scaled by bytes and marked `~`.
- **HepMC3 ASCII** (`.hepmc`, `.hepmc3`, `.hepmc.gz`): `E ` lines counted in the
  first 20 MB, giving events per byte, applied to the group's total size, marked
  `~`. A file smaller than the prefix is counted whole and is exact.
- **LUND** (`.lund`): the same density method on the event header lines
  (`^[0-9]+<TAB>`).
- **eic-smear ROOT** (plain `.root`): the entry count of the largest tree.

678 ROOT files, 215 ASCII files and 8 LUND
files were read this way, 901 in all out of 29,700 event samples
in 211 branches.

### 4.3 Deduplication

Counting files is not counting events, because the same events appear more than
once on disk:

- **The same sample in two formats.** 3,080 event samples exist as both
  `.hepmc3.tree.root` and `.hepmc` (the ROOT copy runs 21–32% of the ASCII size);
  the ROOT copy is counted and the ASCII copy dropped.
- **Chunked ASCII copies.** `DIFFRACTIVE_RHO_ABCONV/Sartre/Coherent` holds 1,500
  `.hepmc.gz` chunks beside 2 ROOT files; both hold the same 14.99M events.
  Where two format groups in one directory agree to within 50% they are treated
  as one sample and the larger is taken.
- **Vertex variants.** `_novtx` and `_vtxfix` re-writes of the same events share
  a stem once the tag is stripped, which is what the `DIS/NC/*/obsolete`
  directories are made of.
- **Stub conversions.** A copy smaller than 2% of the largest copy of the same
  sample is a failed conversion, not a file to count — measured legitimate ratios
  never go below 20%. `DIS/Djangoh/eD` has 9.6 kB ROOT stubs next to 10 GB
  HepMC3 files.
- **`.hist.root` sidecars** (1,860 of them, up to 12 MB each) are not event files.
- **A directory that also holds its subdirectory's events.** Within one cell, a
  sample found both in a directory and in one of its descendants is counted only
  in the descendant. `DIFFRACTIVE_RHO_ABCONV/Sartre` keeps the coherent and
  incoherent samples combined in one 13.7 GB ASCII file beside `Coherent/`
  (10.3 GB) and `Incoherent/` (3.4 GB) — the parent is the same 20M events;
  `DIS/NC/<E>/minQ2=*` sits above its own `obsolete/` copy; `SIDIS/pythia6/ep_18x100`
  above `ep_18x100/ep-18x100`. 269 samples were dropped this way. Sibling
  directories are left alone, because `Coherent/` and `Incoherent/` reuse the
  same file names for different events.
- **A production copied into another energy's tree.**
  `SIDIS/pythia6/ep_5x41/hepmc_ip6/` holds 320 files whose names say 18x275, 221
  of them byte-identical to the files in `ep_18x275/hepmc_ip6/`; they are dropped
  and the directory's genuine 5x41 files are counted at 5x41.
