# ePIC generator data survey

A survey of the ePIC simulation data the collaboration holds — event-generator
(EVGEN) samples, `FULL` and `RECO` campaign output, and the machine-background
inputs needed to mix frames — organised as selection tables: which physics
process exists at which beam energy, whether the beam crossing angle has been
applied, and where background can be added. Built from a read-only sweep of
`/volatile`, `/cache`, `/mss` and Rucio on the JLab farm. See also
[Available Datasets](/ai-epic-background/data) for the Rucio DID catalogue and
[Backgrounds](/ai-epic-background/background) for the mixing pipeline.

**Date:** 2026-10-15 · **Scope:** 20 beam configurations, 190 physics
branches. Marco's two tables are transcribed verbatim (sections 1–3); the
availability survey (sections 5 and 8) is built from a read-only sweep of
`/volatile`, `/cache`, `/mss` and Rucio on ifarm, with the afterburner state of
every branch **measured** from the beam momenta rather than inferred from path
names (section 4).

**Summary of findings**

1. **Four energies are mixable today — 10x100, 10x130, 10x275 (vacuum and
   gold-coated 10 µm) and 18x275 (vacuum).** The campaign's per-source mixing
   configs reference 120 background files and 117 are on disk. 5x41 and 5x100
   are blocked by exactly three missing files. The 9x points have no rate table
   — but since the campaign already reuses the 10x275 electron-ring *files* for
   10x100 and 10x130 with only `freq` changed, 9x is a rate-table problem, not
   a production problem. Section 5.1.
2. **190 physics branches measured across 20 energies**, each with its
   afterburner state read from the beam momenta rather than inferred from the
   path. Section 5.2 is the catalogue, keyed on process rather than on Marco's
   class slugs; section 5.3 lists the processes his table has no row for.
3. **`RECO` is a first-class source, not a fallback.** `MCParticles` keeps the
   crossing angle and the full Pythia8 history, so `edm2hepmc` recovers usable
   generator events — including at 9x, where `FULL` has nothing at all, and from
   tape, where much of EVGEN is `/volatile`-only. Section 5.6.
4. **Three of Marco's rows that look missing are not** (`rho`, `spectroscopy`,
   `omega` — the energy is in the filename, not the path), and `tcs` is
   ambiguous: pure TCS exists **only head-on**. Section 5.7.

## 0. Sources

| What | Where |
|---|---|
| Primary slides | *Event Builder for EICRecon*, O. Partridge & M. Meyer-Conde, SRO Workshop, 2026-08-19 — [indico 33464 / contrib 128271](https://indico.bnl.gov/event/33464/contributions/128271/attachments/72151/123523/EventBuilder%20in%20EICRecon%20Partridge-Meyer.pdf) (32 slides) |
| Machine-background rates | <https://github.com/eic/simulation_campaign_datasets/tree/main/config_data> |
| Physics signal dataset listing | <https://github.com/eic/simulation_campaign_datasets> |
| generatorStatus encoding issue | <https://github.com/AIDASoft/DD4hep/issues/1657#issuecomment-5280917973> |

Tables below are transcribed from the PDF. Text extraction lost the `ff`/`fi`
ligatures (`Di ractive`, `Classi cation`, `o eAu`); those are restored here.
Nothing else is reworded — Marco's own shorthand and notes are kept verbatim.

---

## 1. Marco's ML class table (slide 12, *Machine Learning Classes*)

Goal of the GNN, as stated on the slide: classification (Bkg vs Phy.) and
segmentation (attributed hits). Class definitions grouped as NC/CC DIS,
exclusive hadron, exclusive meson, photo-production.

| # | Class | dir | Physics Process | Generator / source |
|---:|---|---|---|---|
| 0 | Background | `bkg` | SynRad (2000), e-beam-gas/brems (3000), Coulomb (4000), Touschek (5000), p-beam-gas (6000) | dataprod / GETaLM / Xsuite / Pythia8 |
| 1 | NeutralCurrentDISQ1 | `ncdisq1` | NC DIS, Q² ≥ 1 | Pythia8 |
| 2 | NeutralCurrentDISQ10 | `ncdisq10` | NC DIS, Q² ≥ 10 | Pythia8 |
| 3 | NeutralCurrentDISQ100 | `ncdisq100` | NC DIS, Q² ≥ 100 | Pythia8 |
| 4 | NeutralCurrentDISQ1000 | `ncdisq1000` | NC DIS, Q² ≥ 1000 | Pythia8 |
| 5 | ChargedCurrentDISQ100 | `ccdisq100` | CC DIS, Q² ≥ 100 | Pythia8 |
| 6 | ChargedCurrentDISQ1000 | `ccdisq1000` | CC DIS, Q² ≥ 1000 | Pythia8 |
| 7 | DiffractiveDIS | `ddis` | Diffractive DIS, intact proton | RAPGAP |
| 8 | DVCS | `dvcs` | Deeply Virtual Compton Scattering | DVCS generator |
| 9 | DDVCS | `ddvcs` | Double DVCS (ep→eℓ⁺ℓ⁻p) — gated to BEAM=18x275 | EpIC (18x275/10x130 only) |
| 10 | DVMP | `dvmp` | Deeply Virtual Meson Production | EpIC |
| 11 | DEMPQ3to10 | `dempq3to10` | Deep Exclusive Meson Production, Q² ∈ [3,10] | DEMPgen |
| 12 | DEMPQ10to20 | `dempq10to20` | DEMP, Q² ∈ [10,20] | DEMPgen |
| 13 | DEMPQ20to35 | `dempq20to35` | DEMP, Q² ∈ [20,35] | DEMPgen |
| 14 | TCS | `tcs` | Timelike Compton Scattering | TCS generator |
| 15 | DiffractiveJPsi | `jpsi` | Diffractive J/ψ electroproduction, ep | lAger |
| 16 | JPsiPhotoproduction | `jpsiphoto` | Coherent J/ψ photoproduction — gated to BEAM=18x275 | eSTARlight (18x275 only) |
| 17 | UChannelRho | `urho` | u-channel ρ exchange | SLIGHT/GENEX |
| 18 | CoherentRho | `cohrho` | Coherent diffractive ρ off eAu (nuclear rapidity gap) | Sartre |
| 19 | UChannelPi0 | `upi0` | u-channel π⁰ exchange — gated to BEAM=18x275 | (18x275 only) |
| 20 | Upsilon | `upsilon` | Υ threshold production | eSTARlight-family |
| 21 | MesonStructureFn | `mesonsf` | K⁺Λ exclusive meson structure function | eicMesonSFGen |
| 22 | CoherentPhi | `cohphi` | Coherent diffractive ϕ→K⁺K⁻ — off eAu (nuclear rapidity gap) | Sartre |
| 23 | Rho | `rho` | Exclusive ρ→π⁺π⁻ electroproduction, ep, Q² ∈ [0,5] — npsim SIGSEGVs, unresolved | SLIGHT |
| 24 | Spectroscopy | `spectroscopy` | Exotic states X, Y, ψ(2S) | dedicated spectroscopy generators |
| 25 | Omega | `omega` | ω neutral-decay photoproduction — gated to BEAM=18x275 | SLIGHT (18x275 only) |
| 26 | Photoproduction | `photoprod` | Min-bias photoproduction, Q² ∈ [0,1] | Pythia6-eic |

Classes **9, 16, 19, 25** are marked by Marco as gated to 18x275 only. Checked:
correct for `jpsiphoto` (16), `upi0` (19) and `omega` (25); `ddvcs` (9) also has
a 10x130 production. Section 5.2 carries the measured picture.

Class **23** (`rho`) is annotated "npsim SIGSEGVs, unresolved". Confirmed that
this is a *simulation* failure, not missing input: `EXCLUSIVE/RHO_ABCONV` holds
52 afterburned 10x100 files (719 MiB, `slight_10x100_Q2of0to1_rho2Pions_ab_hiAcc_*.hepmc.gz`,
measured 25.010 ± 0.156 mrad). Generator level is fine; the ddsim step is what
broke.

**A caution about this table as a target list.** Marco's `dir` slugs are ML
class names, not paths, and his row set reflects what he chose to mix in summer
2026 — not the limit of what the collaboration has. The survey below is
therefore organised by *what exists and is usable*, with Marco's slug as a
cross-reference column rather than the row key. Three of his rows that look
absent from a path-name search (`rho`, `spectroscopy`, `omega`) in fact have
data; several usable processes have no row at all.

## 2. Machine background sources (slide 10, *Signal and Background Mixing*)

Rates in kHz/GHz are from `simulation_campaign_datasets/config_data`.

| Source | Status | Vacuum | Gold Coating | File size | Effect |
|---|---:|---|---|---|---|
| Synchrotron Radiation | 2000 | 36.608 GHz | 13.277 GHz | ~78 MB | 1–2 photons per event; unique templates reused 10 000× |
| Electron bremsstrahlung radiation | 3000 | 3.177 MHz | 3.177 MHz | ~94 MB | Few-particle QED elastic scatter |
| Electron Touschek scattering | 4000 | 29.56 kHz | 29.56 kHz | ~525 MB | Intra-bunch scatter; slightly more complex final state |
| Electron Coulomb scattering processes | 5000 | 233.5 kHz | 233.5 kHz | ~6.2 GB | Full DIS final state with hadronisation |
| Proton beam gas interactions | 6000 | 31.9 kHz | 31.9 kHz | ~16.7 GB | Soft/hard hadronic production; many secondary tracks |

> **Discrepancy in the slides — resolved from the production configs.** Slide 10
> labels **4000 = Touschek** (29.56 kHz) and **5000 = Coulomb** (233.5 kHz),
> while slide 12 row 0 lists "Coulomb (4000), Touschek (5000)". The campaign's
> own mixing configs
> (`simulation_campaign_datasets/config_data/synrad_…hgas_…json`) settle it: the
> file named `…electron_coulomb_10x275…` carries `status: 4000` at
> `freq: 29.56`, and `…electron_touschek_10x275…` carries `status: 5000` at
> `freq: 233.5`. **Slide 12 is right; slide 10's two row labels are swapped**
> relative to their own rates. Use 4000 = Coulomb, 5000 = Touschek.
>
> Also note the units: `freq` in those configs is in **kHz**, so the SynRad
> `13277000` is 13.277 GHz and the `3177.25` e-beam-gas entry is 3.177 MHz —
> consistent with slide 10 once scaled by 10³.
>
> There is no separate bremsstrahlung input file despite the `egasbrems` in the
> config filenames: the single `GETaLM` electron-beam-gas sample at status 3000
> *is* the brems component. Don't go looking for a sixth file.

## 3. generatorStatus encoding (slide 11)

| Generated status range | Meaning |
|---|---|
| 0–99999 | bkg / machine background (unchanged) — 10 × 1000-wide sub-bands: SynRad, e-beam-gas/brems, Coulomb, Touschek, p-beam-gas, plus headroom for a future 6th+ source |
| 100000–199999 | `ncdisq1` |
| 200000–299999 | `ncdisq10` |
| … | … |

Per-class band = `100000 × (class index)`. Event-level information carried in
the physics event weight; frame-level in `EventBuilderFrameInfo`; AI ground
truth encoded in `generatedStatus` of the `*HitLinks` for segmentation.

Slide 31 flags an **unresolved-class problem**: hits with no truth link at all,
and an undocumented `generatorStatus` gap **[7000, 10000]**, suspected integer
overflow / signed-unsigned conversion in generation software.

---

## 4. Afterburner state: crossing angle vs head-on

**Head-on generator output cannot be fed to the DD4hep/ddsim simulation.** The
ePIC beams cross at 25 mrad; the afterburner (`abconv`) applies the crossing
angle, beam divergence and vertex smearing to a head-on HepMC file. Simulating
a head-on file against the ePIC geometry puts the beams down the wrong axis and
the result is unusable.

So **every** entry in the availability survey carries an explicit afterburner
state, and a dataset that is head-on only is *not* usable generator data for our
purpose — it is at best a candidate that first needs `abconv` run on it.

### 4.1 Naming conventions tested against measurement

The EVGEN tree marks some afterburned branches with an `_ABCONV` suffix on the
process directory, and some files carry `ab` / `_ab` / `.ab` in the filename.
**Neither is reliable**, measured today:

| Checked | Beam angle (e⁻ / p), entry 0 | Verdict |
|---|---|---|
| `EXCLUSIVE/TCS/10x100/hel_plus/tcs_10x100_10.hepmc` | `px=py=0`, `pz=-10` / `px=py=0`, `pz=+100` | **head-on** |
| `EXCLUSIVE/TCS_ABCONV/10x100/hel_plus/tcs_bh_int_ab_hiAcc_10x100_hel_plus_1.hepmc` | p `px=-2.525` → 25.2 mrad, event vertex offset present | afterburned |
| `EXCLUSIVE/DVCS/10x100/DVCS.1.10x100.hepmc` | `px=py=0` both beams | **head-on** |
| `EXCLUSIVE/DVCS_ABCONV/10x100/DVCS.1.ab.hiAcc.10x100.hepmc` | p `px=-2.525` → 25.2 mrad | afterburned |
| `EXCLUSIVE/DVCSD_ABCONV/5x41/DVCS.1-eD-ab-hiAcc-5x41.hepmc` | n `px=-1.038` → 25.3 mrad | afterburned |
| `DIS/pythia8.316-1.0/NC/noRad/ep/9x275/…_run000.hepmc3.tree.root` — **no `ab` token in path or filename** | 0.08 / **25.245 mrad** | **afterburned** |
| `DIS/NC/5x41/minQ2=1/pythia8NCDIS_5x41_minQ2=1_beamEffects_xAngle=-0.025_hiDiv_1.hepmc3.tree.root` | 0.135 ± 0.070 / **25.021 ± 0.227 mrad** | afterburned, hiDiv |
| `DDIS/rapgap3.310-2.0/noRad/ep/9x275/…_ab.hepmc3.tree.root` | 0.200 / 25.087 mrad | afterburned |
| `EXCLUSIVE/DEMP/DEMPgen-1.2.5/9x275/q2_3_10/pi+/…_ab.hepmc3.tree.root` | 0.200 / 25.087 mrad | afterburned |
| `EXCLUSIVE/MESON_SF_ABCONV/eicMesonSFGen-1.0.0/ep/9x275/…_ab_run0001` | 0.362 / 25.161 mrad | afterburned |
| `EXCLUSIVE/DVMP/EpIC1.1.8-1.0/unpolarised/9x275/hiDiv/…_ab_hiDiv_run001` | 0.247 ± 0.128 / 24.995 ± 0.124 mrad | afterburned, hiDiv |
| `SIDIS/pythia6-eic/1.3.0/ep_noradcor/9x275/q2_10to100/….ab.…` | 0.233 ± 0.129 / 24.987 ± 0.127 mrad | afterburned |

The takeaways:

- `_ABCONV` directory with a bare sibling of the same process (`TCS` vs
  `TCS_ABCONV`, `DVCS` vs `DVCS_ABCONV`) → the bare one **is** head-on. Here the
  convention holds.
- The `DIS`, `DDIS`, `SIDIS` and `EXCLUSIVE/DVMP`, `EXCLUSIVE/DEMP` trees carry
  **no `ABCONV` segment at all and are afterburned anyway**. Judging them by the
  directory name would have wrongly excluded the main DIS samples — including
  every 9 GeV-electron DIS dataset.
- So the survey classifies by **measurement**, with the path convention only as
  a cross-check.

### 4.2 Measurement method

`hepmc3.tree.root` files: open with ROOT 6.40 inside
`eicweb/eic_xl:nightly` (`gSystem.Load("libHepMC3rootIO")`), read the
`hepmc3_tree` / `hepmc3_event` branch, take the two `status == 4` particles and
compute `atan2(hypot(px,py), |pz|)`. `apptainer` needs `-B /volatile:/volatile:ro`
and a writable `TMPDIR`, or `TFile::Open` fails with "does not exist". Plain
`.hepmc` (HepMC3 ASCII) files are cheaper: `head` the file and read the `P`
lines with trailing status `4`.

Beam divergence and vertex smearing separate **hiAcc** (nominal angle, no
divergence) from **hiDiv** (realistic divergence); `DIS/NC` and
`DIS/pythia8.316-1.0` samples show vertex-z spread of 34–45 mm, i.e. realistic
beam effects. For streaming-readout / timing work `hiDiv` is the physical choice
where both exist.

**The smeared interaction point lives in two different places** depending on the
production chain, and reading only one of them gives a false "no beam effects":

- `event_pos` on the HepMC3 event (the `@ x y z t` field on the ASCII `E` line)
  — this is where the `abconv`-processed EpIC / DEMPgen / lAger / eSTARlight /
  rapgap / pythia6-eic files put it;
- `vertices[0].position` — this is where the `pythia8.316-1.0` and
  `DIS/NC` pythia8 NCDIS files put it, with `event_pos` left at zero.

The survey reads both and takes whichever is non-zero. Three ASCII branches
(`DIS/CC/{5x41,10x100,10x275}/minQ2=*`) record neither despite being
`beamEffects_xAngle=-0.025_hiDiv` productions; those are reported as *"vertex
spread not stored in this file"* rather than as having none.

### 4.3 Directory census by afterburner naming

First count of energy-named directories under `/volatile/eic/EPIC/EVGEN`
(depth ≤ 7), split by whether the path contains `ABCONV` — remembering from
4.1 that a missing `ABCONV` does **not** mean head-on:

| Energy | energy dirs total | of which under an `ABCONV` branch |
|---|---:|---:|
| 5x41 | 25 | 9 |
| 9x100 | 8 | 7 |
| 9x130 | 18 | 10 |
| 9x275 | 21 | 12 |

(Whole-tree token census, any depth: `10x100` 85, `5x41` 81, `18x275` 79,
`9x275` 43, `9x130` 42, `10x130` 41, `5x100` 24, `10x110` 22, `10x275` 18,
`10x115` 16, `10x250` 15, `10x166` 12, `9x100` 10, `9x166` 8, `18x110` 4,
`9x115` 3, `18x100` 3. The 9 GeV-electron configurations are real and
well populated, except `9x100` which is thin.)

---

## 5. Survey of available data

Target energies (7), agreed 2026-10-15:

| Priority | Energies |
|---|---|
| Asked for | **5x41, 9x100, 9x130, 9x275** |
| Added as the 10 GeV-electron counterparts, for comparison | **10x100, 10x130, 10x275** |

Wanted: **event data without background**, in order of preference:

1. **Event generator files** (HepMC / `hepmc3.tree.root`) — preferred, and only
   directly usable if afterburned (section 4).
2. **`FULL` (ddsim/DD4hep) campaign output without background mixing** — less
   preferred; already simulated, so geometry/campaign version is fixed. Every
   campaign version that has the class at that energy is reported, with the
   version named.

### 5.1 Energies with a complete background recipe

**(a) There is no `FULL` simulation at any 9 GeV-electron energy.** Checked in
all three stores: `/volatile/eic/EPIC/FULL`, `/mss/eic/EPIC/FULL` (tape) and
Rucio `epic:/FULL/*`. Zero directories or DIDs for `9x100`, `9x130`, `9x275`.
What `FULL` does have at our energies:

| Energy | `FULL` content | Campaign versions |
|---|---|---|
| 5x41 | `DIS/NC` (`minQ2=1`, `=10`, `=100`) | 23.05.2 (arches, brycecanyon), 23.06.0/1, 23.07.1/2, 23.08.0, 23.09.1, 23.11.0, 23.12.0, 25.12.0, 26.02.0, `main` |
| 10x100 | `DIS/NC` (`minQ2=1`, `=10`, `=100`); `EXCLUSIVE/UCHANNEL_RHO` (23.08.0 only) | 23.03.0 … 23.12.0, 25.12.0, 26.02.0, 26.07.1 (bkg-mixed), `main` |
| 10x275 | `DIS/NC` (`minQ2=1`) | 25.12.0, 26.02.0, 26.07.1 (bkg-mixed) |
| 9x100, 9x130, 9x275, 10x130 | **nothing** | — |

Recent campaigns keep **no signal `FULL` at all** — `FULL/26.04.1`, `26.07.0`
and `26.07.1` contain only `Bkg_Exact1S_2us`, `BACKGROUNDS` and `SINGLE`. The
signal ddsim output is not retained; only the reconstructed `RECO` partition is.

So the `FULL` fallback is only available for `ncdisq1/10/100` at 5x41, 10x100
and 10x275, from campaigns 23.x–26.02.0. **`RECO`, however, does cover 9x** —
see section 5.6, which is the practical route for the 9 GeV points.

**(b) Per-source background inputs are complete at 10x100, 10x130, 10x275
and 18x275.**

The campaign ships a complete mixing recipe per energy in
`simulation_campaign_datasets/config_data/synrad_egasbrems_egascoulomb_egastouschek_hgas_<E>_<pipe>_10000Ahr_machineruntime_<T>.json`.
Each entry is `{file, freq, skip, status}` — the EVGEN background file, its rate
in **kHz**, and the `generatorStatus` code to stamp on its particles. The five
`status` codes are exactly Marco's slide-10 set: 2000 SynRad, 3000
electron-beam-gas (incl. brems), 4000 Coulomb, 5000 Touschek, 6000
proton-beam-gas. The `hgas_`-prefixed configs are the ones to use — the
non-`hgas_` variants drop the proton-beam-gas term.

Checked every file these configs reference against `/volatile`. The configs
contain 120 file *entries*, but 99 of those are one per-run series
(`ProtonBeamGas_275GeV_run001…run100`, used only by the 18x275 10 ms config),
so there are **21 distinct input files — 18 present, 3 missing**.

| Energy | pipe variants | all five inputs on disk? |
|---|---|---|
| **10x100** | vacuum, gold 10 µm | **yes** |
| **10x130** | vacuum, gold 10 µm | **yes** |
| **10x275** | vacuum, gold 10 µm | **yes** |
| **18x275** | vacuum (50 s and 10 ms runtimes) | **yes** |
| 5x100 | vacuum | no — missing `BEAMGAS/electron/GETaLM1.0.0-1.1/5GeV/…` and `SYNRAD/dataprod_rel_1.0.0/5x100/…preproc_10000repeats…` |
| 5x41 | vacuum | no — the two above **plus** `BEAMGAS/proton/pythia8.306-1.0/41GeV/combined/…` |
| 9x100, 9x130, 9x275 | — | no config exists at all |

So **four energies are mixable today**: 10x100, 10x130, 10x275 (each with a
vacuum and a gold-coated 10 µm variant) and 18x275 (vacuum). 5x41 and 5x100 are
blocked by three absent files, not by a missing recipe.

**The campaign already substitutes electron-ring samples across hadron
energies.** This is the important precedent for 9 GeV. At 10x100 and 10x130 the
SynRad, Coulomb and Touschek inputs are literally the **10x275 files**, reused
unchanged, with only `freq` adjusted per energy; only the electron-beam-gas
(keyed on electron energy, `10GeV`) and proton-beam-gas (keyed on proton energy,
`100GeV` / `130GeV` / `275GeV`) terms are native. The same was intended at 5x41,
where SynRad is taken from `5x100`.

That means a 9 GeV mixing config is a **rate-table problem, not a
sample-production problem**: the 10 GeV ESR samples can be reused for 9x275 /
9x130 / 9x100 exactly as they already are for 10x100 and 10x130, as soon as
someone supplies the 9 GeV `freq` numbers. The proton-side terms already exist
natively at 275 GeV, 130 GeV and 100 GeV.

#### Mixing spec per energy and source

`native?` says whether the input sample belongs to that energy or is borrowed
from another. `rate` is the sum over entries with that status code; `×N` marks a
status that appears as N separate entries in the config. The 18x275 10 ms config
lists proton-beam-gas as 100 separate ~256 MB `run0NN` files at 0.225 kHz each —
summing to 22.5 kHz, the same total as the 50 s config's single `combined`
entry, so it looks like a way to avoid one 22 GiB input rather than an error.
Not verified beyond that arithmetic.

| energy | pipe | runtime | status | source | rate [kHz] | input sample | native? | on disk | size |
|---|---|---|---:|---|---:|---|---|---|---:|
| 10x100 | gold 10 µm | 50s | 2000 | SynRad | 13,277,000.00 | `10x275` | **substituted** | yes | 78.0 MiB |
| 10x100 | gold 10 µm | 50s | 3000 | e-beam-gas + brems | 3,177.25 | `10GeV` | native | yes | 6.2 GiB |
| 10x100 | gold 10 µm | 50s | 4000 | e Coulomb | 29.56 | `10x275` | **substituted** | yes | 94.1 MiB |
| 10x100 | gold 10 µm | 50s | 5000 | e Touschek | 233.50 | `10x275` | **substituted** | yes | 525.1 MiB |
| 10x100 | gold 10 µm | 50s | 6000 | p-beam-gas | 31.90 | `100GeV` | native | yes | 16.7 GiB |
| 10x100 | vacuum | 50s | 2000 | SynRad | 36,608,000.00 | `10x275` | **substituted** | yes | 287.0 MiB |
| 10x100 | vacuum | 50s | 3000 | e-beam-gas + brems | 3,177.25 | `10GeV` | native | yes | 6.2 GiB |
| 10x100 | vacuum | 50s | 4000 | e Coulomb | 29.56 | `10x275` | **substituted** | yes | 94.1 MiB |
| 10x100 | vacuum | 50s | 5000 | e Touschek | 233.50 | `10x275` | **substituted** | yes | 525.1 MiB |
| 10x100 | vacuum | 50s | 6000 | p-beam-gas | 31.90 | `100GeV` | native | yes | 16.7 GiB |
| 10x130 | gold 10 µm | 50s | 2000 | SynRad | 13,277,000.00 | `10x275` | **substituted** | yes | 78.0 MiB |
| 10x130 | gold 10 µm | 50s | 3000 | e-beam-gas + brems | 3,177.25 | `10GeV` | native | yes | 6.2 GiB |
| 10x130 | gold 10 µm | 50s | 4000 | e Coulomb | 29.56 | `10x275` | **substituted** | yes | 94.1 MiB |
| 10x130 | gold 10 µm | 50s | 5000 | e Touschek | 233.50 | `10x275` | **substituted** | yes | 525.1 MiB |
| 10x130 | gold 10 µm | 50s | 6000 | p-beam-gas | 31.97 | `130GeV` | native | yes | 1.8 GiB |
| 10x130 | vacuum | 50s | 2000 | SynRad | 36,608,000.00 | `10x275` | **substituted** | yes | 287.0 MiB |
| 10x130 | vacuum | 50s | 3000 | e-beam-gas + brems | 3,177.25 | `10GeV` | native | yes | 6.2 GiB |
| 10x130 | vacuum | 50s | 4000 | e Coulomb | 29.56 | `10x275` | **substituted** | yes | 94.1 MiB |
| 10x130 | vacuum | 50s | 5000 | e Touschek | 233.50 | `10x275` | **substituted** | yes | 525.1 MiB |
| 10x130 | vacuum | 50s | 6000 | p-beam-gas | 31.97 | `130GeV` | native | yes | 1.8 GiB |
| 10x275 | gold 10 µm | 50s | 2000 | SynRad | 13,277,000.00 | `10x275` | native | yes | 78.0 MiB |
| 10x275 | gold 10 µm | 50s | 3000 | e-beam-gas + brems | 3,177.25 | `10GeV` | native | yes | 6.2 GiB |
| 10x275 | gold 10 µm | 50s | 4000 | e Coulomb | 29.56 | `10x275` | native | yes | 94.1 MiB |
| 10x275 | gold 10 µm | 50s | 5000 | e Touschek | 233.50 | `10x275` | native | yes | 525.1 MiB |
| 10x275 | gold 10 µm | 50s | 6000 | p-beam-gas | 32.60 | `275GeV` | native | yes | 21.0 GiB |
| 10x275 | vacuum | 50s | 2000 | SynRad | 36,608,000.00 | `10x275` | native | yes | 287.0 MiB |
| 10x275 | vacuum | 50s | 3000 | e-beam-gas + brems | 3,177.25 | `10GeV` | native | yes | 6.2 GiB |
| 10x275 | vacuum | 50s | 4000 | e Coulomb | 29.56 | `10x275` | native | yes | 94.1 MiB |
| 10x275 | vacuum | 50s | 5000 | e Touschek | 233.50 | `10x275` | native | yes | 525.1 MiB |
| 10x275 | vacuum | 50s | 6000 | p-beam-gas | 32.60 | `275GeV` | native | yes | 21.0 GiB |
| 18x275 | vacuum | 10ms | 2000 | SynRad | 14,000.00 | `18x275` | native | yes | 194.9 MiB |
| 18x275 | vacuum | 10ms | 3000 | e-beam-gas + brems | 316.94 | `18GeV` | native | yes | 3.8 GiB |
| 18x275 | vacuum | 10ms | 4000 | e Coulomb | 1.30 | `18x275` | native | yes | 674.3 KiB |
| 18x275 | vacuum | 10ms | 5000 | e Touschek | 0.72 | `18x275` | native | yes | 314.5 KiB |
| 18x275 | vacuum | 10ms | 6000 | p-beam-gas ×100 | 22.50 | `275GeV` | native | yes | 244.1 MiB |
| 18x275 | vacuum | 50s | 2000 | SynRad | 3,324,000.00 | `18x275` | native | yes | 286.8 MiB |
| 18x275 | vacuum | 50s | 3000 | e-beam-gas + brems | 316.94 | `18GeV` | native | yes | 3.8 GiB |
| 18x275 | vacuum | 50s | 4000 | e Coulomb | 0.86 | `18x275` | native | yes | 3.5 MiB |
| 18x275 | vacuum | 50s | 5000 | e Touschek | 0.55 | `18x275` | native | yes | 1.7 MiB |
| 18x275 | vacuum | 50s | 6000 | p-beam-gas | 22.50 | `275GeV` | native | yes | 21.0 GiB |
| 5x100 | vacuum | 50s | 2000 | SynRad | 36,608,000.00 | `5x100` | native | **MISSING** | — |
| 5x100 | vacuum | 50s | 3000 | e-beam-gas + brems | 2,826.38 | `5GeV` | native | **MISSING** | — |
| 5x100 | vacuum | 50s | 4000 | e Coulomb | 116.57 | `5x100` | native | yes | 340.9 MiB |
| 5x100 | vacuum | 50s | 5000 | e Touschek | 1,112.30 | `5x100` | native | yes | 2.6 GiB |
| 5x100 | vacuum | 50s | 6000 | p-beam-gas | 22.00 | `100GeV` | native | yes | 16.7 GiB |
| 5x41 | vacuum | 50s | 2000 | SynRad | 36,608,000.00 | `5x100` | **substituted** | **MISSING** | — |
| 5x41 | vacuum | 50s | 3000 | e-beam-gas + brems | 2,181.97 | `5GeV` | native | **MISSING** | — |
| 5x41 | vacuum | 50s | 4000 | e Coulomb | 116.57 | `5x100` | **substituted** | yes | 340.9 MiB |
| 5x41 | vacuum | 50s | 5000 | e Touschek | 1,112.30 | `5x100` | **substituted** | yes | 2.6 GiB |
| 5x41 | vacuum | 50s | 6000 | p-beam-gas | 12.20 | `41GeV` | native | **MISSING** | — |

#### Expected events per 2 µs frame

This is the form that matters for occupancy: `freq` (kHz) × 10³ × 2×10⁻⁶ s.

| config | SynRad | e-gas+brems | Coulomb | Touschek | p-gas | total / frame |
|---|---:|---:|---:|---:|---:|---:|
| 10x100 vacuum | 73,216 | 6.35 | 0.06 | 0.47 | 0.06 | 73,223 |
| 10x100 gold 10 µm | 26,554 | 6.35 | 0.06 | 0.47 | 0.06 | 26,561 |
| 10x130 vacuum | 73,216 | 6.35 | 0.06 | 0.47 | 0.06 | 73,223 |
| 10x130 gold 10 µm | 26,554 | 6.35 | 0.06 | 0.47 | 0.06 | 26,561 |
| 10x275 vacuum | 73,216 | 6.35 | 0.06 | 0.47 | 0.07 | 73,223 |
| 10x275 gold 10 µm | 26,554 | 6.35 | 0.06 | 0.47 | 0.07 | 26,561 |
| 5x41 vacuum | 73,216 | 4.36 | 0.23 | 2.22 | 0.02 | 73,223 |
| 5x100 vacuum | 73,216 | 5.65 | 0.23 | 2.22 | 0.04 | 73,224 |
| 18x275 vacuum, 50 s | 6,648 | 0.63 | 0.00 | 0.00 | 0.04 | 6,649 |
| 18x275 vacuum, 10 ms | 28 | 0.63 | 0.00 | 0.00 | 0.05 | 29 |

Two things this makes obvious that the kHz table hides.

**There is no smooth energy dependence — there are three regimes.** SynRad is
*the same number* (36.608 GHz vacuum / 13.277 GHz gold) at 10x100, 10x130,
10x275, 5x41 and 5x100, because the configs reuse one SynRad sample with its
rate unchanged. Only 18x275 differs. So the available background regimes are
**vacuum ≈ 73k events/frame, gold ≈ 26.5k, and 18x275 ≈ 6.6k** — plus the
18x275 10 ms config at 29/frame, which is a different beast and is *not*
interchangeable with its 50 s sibling.

**Occupancy is SynRad and nothing else.** Every other source is under 7 events
per frame; Coulomb and Touschek under 2.3. Their rate ratios across energies are
dramatic but irrelevant to hit counts. The significance of those four is
qualitative: SynRad is 1–2 soft photons per event, so it is hit-level noise with
no tracks, whereas Coulomb carries a full DIS final state with hadronisation and
proton beam gas produces many secondary tracks (section 2). **Those rare sources
are the track-like background a tracking-based event builder has to reject.**
Note 5x41 has ~4× the Coulomb and Touschek of the 10 GeV points at the same
total occupancy, making it the track-background-richest configuration available.

#### Beampipe coating: rates and campaign history

`vacuum` is the bare beampipe; `GoldCoating/10um` is a 10 µm gold layer on the
inside. Synchrotron photons striking the wall are either absorbed or scattered
onward into the detector acceptance; high-Z gold absorbs the soft X-rays that
the bare low-Z wall would pass along. That is the standard rationale rather than
something verified here, but the numbers agree: **2.76× less SynRad**, with the
other four sources byte-identical. The input files show it too — the bare
`…synrad_10x275_run001.preproc_10000repeats` file is 287 MiB and the
`GoldCoating/10um/` file of the same name is 78 MiB. That 78 MB is the figure in
Marco's slide-10 "File size" column, so his table quotes the gold-coated file.

The campaign's own choice over time:

| campaign | coating used for mixed production |
|---|---|
| 25.06.1 | **vacuum** (`Synrad_18GeV_Vac_10000Ahr_…`), 18x275 only |
| 25.12.0, 26.02.0 | gold, **both 5 µm and 10 µm** |
| 26.03.0, 26.04.1, 26.07.0, 26.07.1 | gold, **10 µm only** |

Vacuum, then gold at two thicknesses, then gold 10 µm for four consecutive
campaigns. That reads as the coating being adopted and the thickness settled,
so **gold 10 µm is the configuration to train on and quote results for**, not
one of two live options. The engineering decision itself is not something this
survey can confirm — but nothing in the data contradicts it.

What that leaves us:

- **Vacuum becomes a tool, not a scenario.** 2.76× more SynRad with everything
  else identical, at all three mixable 10x energies — a free occupancy stress
  test and the high end of a rate-randomisation range. It should not be reported
  as an expected operating point.
- **5 µm is a superseded intermediate**, present in `FULL`/`RECO` for 25.12.0
  and 26.02.0 but with no shipped rate config, so not mixable without writing
  our own rate table.
- **There is no 18x275 gold SynRad sample.** So the two realistic points are
  gold-at-10x (26.5k/frame) and vacuum-at-18x275 (6.6k/frame), and the latter is
  vacuum only because nobody produced the gold version. If an 18x275 gold
  configuration matters, that is a specific and small thing to request.

### 5.2 Process catalogue

This is the table to work from. Rows are **physics processes as the data
defines them**, not Marco's class slugs; his slug is a cross-reference column
(`—` means the process has no row in his table at all). Energies listed are
those with an **afterburned** sample; `(h)` marks an energy where only
head-on data exists, so `abconv` would have to be run first.

206 branches were measured; 190 are physics (the other 16 are the background
sources of section 2). Mixable energies are in **bold**. `†` marks an energy
taken from the filename because the beams could not be parsed
(`erhic-cc-yrad-floff_eD_18_137_q2_1_evt.hepmc3` → 18x137, eD per-nucleon).

| process | system | generator(s) | energies with afterburned data | Marco slug | branches | files | size |
|---|---|---|---|---|---:|---:|---:|
| CC DIS, Q² threshold | ep | Pythia8 (campaign) | 5x41, 5x100, **10x100**, **10x275**, **18x275** | `ccdisq100/1000` | 5 | 90 | 639.6 GiB |
| CC DIS, radiative (eRHIC fmt) | eD | DJANGOH/eRHIC | 18x137(h)† | `ccdisq*` | 1 | 42 | 92.2 GiB |
| CC DIS, radiative (eRHIC fmt) | ep | DJANGOH/eRHIC | 18x275(h) | `ccdisq*` | 1 | 35 | 97.8 GiB |
| CC DIS, radiative, polarised | ep | DJANGOH 4.6.10 | 9x275 | `ccdisq* (diff. generator)` | 2 | 6 | 3.0 GiB |
| DEMP π⁺ / K⁺Λ / K⁺Σ⁰ | ep | DEMPgen | 5x41, 5x100, 9x130, 9x275, **10x100**, **10x130**, **18x275** | `dempq3to10/10to20/20to35` | 13 | 840 | 375.1 GiB |
| DVCS | ep | DVCS gen (legacy) | 5x41, **10x100**, **18x275** | `dvcs` | 6 | 65 | 32.9 GiB |
| DVCS + BH + INT | ep | EpIC 1.1.6 | 5x41, **10x100**, **10x130**, **18x275** | `dvcs` | 6 | 10 | 3.5 GiB |
| DVCS / BH / interference | ep | EpIC 1.1.8 | 9x130, 9x275 | `dvcs` | 6 | 24 | 11.3 GiB |
| DVCS on deuteron | eD | EpIC | 5x41, **10x100** | `— (eD)` | 2 | 26 | 23.9 GiB |
| DVMP / Υ (lAger legacy) | ep | lAger | **10x100** | `dvmp/upsilon` | 1 | 8 | 1.7 GiB |
| DVMP J/ψ→μ⁺μ⁻ | ep | lAger | 9x130, 9x275, **10x130**, **18x275** | `dvmp` | 4 | 4 | 3.2 GiB |
| DVMP π⁰ | ep | EpIC | 5x41, 9x130, 9x275, **10x100**, **10x130**, **18x275** | `dvmp` | 7 | 8 | 2.2 GiB |
| NC DIS, Q² threshold | ep | Pythia8 (campaign) | 5x41, 5x100, **10x100**, **10x275**, **18x275** | `ncdisq1/10/100/1000` | 8 | 328 | 2.3 TiB |
| NC DIS, inclusive | ep | Pythia6.428, Pythia8.316 | 5x41, 5x100, 9x130, 9x275, **10x100**, **10x130**, **10x275**, **18x275** | `ncdisq1/10/100/1000` | 8 | 175 | 222.6 GiB |
| NC DIS, inclusive (EEEMCal cfg) | ep | Pythia8.315 | 9x275 | `ncdisq*` | 1 | 100 | 1.8 GiB |
| NC/CC DIS, radiative | ep | DJANGOH 4.6.21 | **18x275** | `ncdisq*/ccdisq*` | 2 | 8 | 6.5 GiB |
| SIDIS / min-bias photoprod. | en | Pythia6-eic | 5x41, **10x100**, **18x275** | `photoprod` | 3 | 715 | 576.5 GiB |
| SIDIS / min-bias photoprod. | ep | Pythia6-eic | 5x41, 5x100, 9x130, 9x275, **10x100**, **10x275**, **18x275** | `photoprod` | 10 | 1141 | 1.1 TiB |
| SIDIS D_s | ep | Pythia8 HFsim | 9x275 | `—` | 1 | 1200 | 3.1 GiB |
| SIDIS D_s (eA) | eAu | BeAGLE HFsim | 9x100 | `—` | 1 | 500 | 5.8 GiB |
| SIDIS dijet (PGF) | ep | Pythia6.428 dijet | **18x275** | `—` | 1 | 100 | 972.1 MiB |
| SIDIS open charm D⁰ | ep | Pythia8, Pythia8 HFsim | 5x41, 9x130, 9x275, **10x100**, **10x130**, **18x275** | `—` | 6 | 3728 | 22.7 GiB |
| SIDIS open charm D⁰ (eA) | eAu | BeAGLE HFsim | 5x41, 9x100, **10x100** | `—` | 5 | 4900 | 15.1 GiB |
| SIDIS Λ | ep | Pythia8.306 | **18x275** | `—` | 1 | 8 | 10.5 GiB |
| SIDIS Λ_c | ep | Pythia8 HFsim | 9x275, **10x100** | `—` | 2 | 3500 | 3.7 GiB |
| SIDIS Λ_c (eA) | eAu | BeAGLE HFsim | 9x100, **10x100** | `—` | 3 | 1498 | 6.6 GiB |
| SIDIS, Q²-binned | ep | Pythia6 (IP6 era) | 5x41, **10x100**, **18x275** | `photoprod (older prod.)` | 5 | 5900 | 3.9 TiB |
| TCS + BH interference | ep | TCS gen | 5x41, **10x100**, **18x275** | `tcs` | 6 | 860 | 121.9 GiB |
| TCS, pure | ep | TCS gen — **no afterburned sample anywhere** | 5x41(h), 5x100(h), 10x100(h), 18x275(h) | `tcs` | 4 | 80 | 83.1 GiB |
| coherent J/ψ photoproduction | ep | eSTARlight | **18x275** | `jpsiphoto` | 1 | 2 | 679.2 MiB |
| coherent ρ, eA | eAu | Sartre | 18x110(h) | `cohrho` | 1 | 2 | 23.7 GiB |
| coherent φ→K⁺K⁻, eA | eAu | Sartre | 9x100, **10x100**, 18x110 | `cohphi` | 4 | 14 | 61.1 GiB |
| coherent/incoherent J/ψ, eA | eAu | Sartre | 18x110 | `— (eA)` | 2 | 8 | 32.4 GiB |
| coherent/incoherent ρ, eA | eAu | Sartre | 9x100, **10x100**, 18x110 | `cohrho` | 4 | 2012 | 48.1 GiB |
| diffractive DIS | ep | RAPGAP 3.310 | 9x130, 9x275, **10x100** | `ddis` | 5 | 5 | 14.2 GiB |
| diffractive J/ψ, eA | eAu | Sartre | 18x110(h) | `— (eA)` | 1 | 2 | 23.6 GiB |
| diffractive J/ψ, ePb | ePb | BeAGLE | 18x108.41 | `— (ePb)` | 1 | 54 | 112.5 GiB |
| diffractive J/ψ, ep | ep | lAger | 5x41, 5x100, 9x130, 9x275, **10x100**, **10x130**, **18x275** | `jpsi` | 7 | 7 | 437.7 MiB |
| diffractive φ, eA | eAu | Sartre/BeAGLE, eSTARlight | 18x110 | `cohphi` | 2 | 3 | 23.7 GiB |
| diffractive φ, eA | ep | Sartre/BeAGLE | 18x110(h) | `cohphi` | 1 | 200 | 72.0 GiB |
| diffractive φ, ePb/eAu | eAu | BeAGLE | 9x100, **10x100** | `cohphi` | 2 | 200 | 35.8 GiB |
| diffractive φ, ePb/eAu | ePb | BeAGLE | 18x108.41 | `cohphi` | 1 | 54 | 608.6 GiB |
| double DVCS | ep | EpIC | **10x130**, **18x275** | `ddvcs` | 2 | 6 | 2.3 GiB |
| exclusive ρ→π⁺π⁻ | ep | SLIGHT | **10x100**, unknown(h) | `rho` | 3 | 56 | 1.5 GiB |
| inclusive eA DIS | eAu | BeAGLE | 5x41, 9x100, **10x100** | `—` | 5 | 815 | 94.3 GiB |
| inclusive eA DIS | eH2 | BeAGLE | 9x130, **10x130** | `—` | 5 | 221 | 73.3 GiB |
| inclusive eA DIS | eHe3 | BeAGLE | 5x41 | `—` | 1 | 3 | 3.2 GiB |
| meson structure function K⁺Λ | ep | eicMesonSFGen | 5x41, 9x100, 9x130, 9x275, **10x100**, **10x130**, **18x275** | `mesonsf` | 7 | 3800 | 2.9 GiB |
| spectroscopy ψ(2S)/X/Y | ep | dedicated | **10x100** | `spectroscopy` | 2 | 30 | 2.6 GiB |
| u-channel π⁰ | ep | SLIGHT | **18x275** | `upi0` | 1 | 1 | 36.3 MiB |
| u-channel ρ | ep | SLIGHT/GENEX | **10x100** | `urho` | 1 | 1 | 35.6 MiB |
| u-channel ω (neutral decay) | ep | SLIGHT | 18x275(h) | `— (not upi0/omega)` | 1 | 10 | 250.6 MiB |
| Υ photoproduction (legacy) | ep | eSTARlight | unknown(h) | `upsilon` | 1 | 3 | 9.5 MiB |
| Υ(1S/2S/3S) threshold | ep | eSTARlight 1.3.0 | 9x130, 9x275 | `upsilon` | 6 | 450 | 14.1 GiB |
| ω photoproduction | ep | SLIGHT | **18x275** | `omega` | 2 | 98 | 1.4 GiB |

### 5.3 Processes with no row in Marco's table

Afterburned, ready to use, and absent from his 27 rows. Ordered by how much
there is.

| process | system | generator | energies | files | size |
|---|---|---|---|---:|---:|
| diffractive J/ψ, ePb | ePb | BeAGLE | 18x108.41 | 54 | 112.5 GiB |
| inclusive eA DIS | eAu | BeAGLE | 5x41, 9x100, **10x100** | 815 | 94.3 GiB |
| inclusive eA DIS | eH2 | BeAGLE | 9x130, **10x130** | 221 | 73.3 GiB |
| coherent/incoherent J/ψ, eA | eAu | Sartre | 18x110 | 8 | 32.4 GiB |
| DVCS on deuteron | eD | EpIC | 5x41, **10x100** | 26 | 23.9 GiB |
| SIDIS open charm D⁰ | ep | Pythia8, Pythia8 HFsim | 5x41, 9x130, 9x275, **10x100**, **10x130**, **18x275** | 3728 | 22.7 GiB |
| SIDIS open charm D⁰ (eA) | eAu | BeAGLE HFsim | 5x41, 9x100, **10x100** | 4900 | 15.1 GiB |
| SIDIS Λ | ep | Pythia8.306 | **18x275** | 8 | 10.5 GiB |
| SIDIS Λ_c (eA) | eAu | BeAGLE HFsim | 9x100, **10x100** | 1498 | 6.6 GiB |
| SIDIS D_s (eA) | eAu | BeAGLE HFsim | 9x100 | 500 | 5.8 GiB |
| SIDIS Λ_c | ep | Pythia8 HFsim | 9x275, **10x100** | 3500 | 3.7 GiB |
| inclusive eA DIS | eHe3 | BeAGLE | 5x41 | 3 | 3.2 GiB |
| SIDIS D_s | ep | Pythia8 HFsim | 9x275 | 1200 | 3.1 GiB |
| SIDIS dijet (PGF) | ep | Pythia6.428 dijet | **18x275** | 100 | 972.1 MiB |

### 5.4 Per-energy detail

`events/file` is the entry count of the largest file in the branch. Beam angle
is `mean ± rms` over 20 events, with the beam energy the file itself reports.

#### 10x100 — mixable (background recipe complete)

| process | branch | generator | system | files | size | events/file | e⁻ / hadron beam [mrad @ GeV] | beam effects | tape |
|---|---|---|---|---:|---:|---:|---|---|---|
| CC DIS, Q² threshold | `DIS/CC` | Pythia8 (campaign) | ep | 20 | 133.5 GiB | — | 0.162+-0.078@E10.0 / 25.030+-0.226@E100.0 | not recorded | — |
| DEMP π⁺ / K⁺Λ / K⁺Σ⁰ | `EXCLUSIVE/DEMP/DEMPgen-1.1.0` | DEMPgen | ep | 390 | 3.2 GiB | 29,342 | 0.185+-0.092@E10.0 / 25.012+-0.190@E100.0 | z 31 mm, t 33.41 ns | — |
| DEMP π⁺ / K⁺Λ / K⁺Σ⁰ | `EXCLUSIVE/DEMP/DEMPgen-1.2.0` | DEMPgen | ep | 60 | 93.1 GiB | 5,451,937 | 0.185+-0.092@E10.0 / 25.012+-0.190@E100.0 | z 31 mm, t 33.41 ns | — |
| DEMP π⁺ / K⁺Λ / K⁺Σ⁰ | `EXCLUSIVE/DEMP/DEMPgen-1.2.2` | DEMPgen | ep | 3 | 287.5 MiB | 457,311 | 0.185+-0.092@E10.0 / 25.012+-0.190@E100.0 | z 31 mm, t 33.41 ns | — |
| DVCS | `EXCLUSIVE/DVCS` | DVCS gen (legacy) | ep | 1 | 823.1 MiB | — | 0.000+-0.000@E10.0 / 0.000+-0.000@E100.0 | **head-on** | — |
| DVCS | `EXCLUSIVE/DVCS_ABCONV` | DVCS gen (legacy) | ep | 12 | 5.8 GiB | — | 0.151+-0.075@E10.0 / 25.010+-0.156@E100.0 | z 31 mm, t 33.41 ns | — |
| DVCS + BH + INT | `EXCLUSIVE/DVCS_ABCONV/EpIC_v1.1.6-1.2` | EpIC 1.1.6 | ep | 2 | 843.6 MiB | 1,300,000 | 0.151+-0.075@E10.0 / 25.010+-0.156@E100.0 | z 31 mm, t 33.41 ns | — |
| DVCS on deuteron | `EXCLUSIVE/DVCSD_ABCONV` | EpIC | eD | 14 | 11.8 GiB | — | 0.151+-0.075@E10.0 / 25.010+-0.156@E100.0 | z 31 mm, t 33.41 ns | — |
| DVMP / Υ (lAger legacy) | `EXCLUSIVE/DVMP/lAger` | lAger | ep | 8 | 1.7 GiB | — | 0.000+-0.000@E10.0 / 25.000+-0.000@E100.0 | not recorded | — |
| DVMP π⁰ | `EXCLUSIVE/DVMP/EpIC1.0.0-1.0` | EpIC | ep | 1 | 24.8 MiB | 100,000 | 0.000+-0.000@E10.0 / 0.000+-0.000@E100.0 | **head-on** | — |
| DVMP π⁰ | `EXCLUSIVE/DVMP/EpIC1.0.0-1.1` | EpIC | ep | 1 | 48.0 MiB | 100,000 | 0.151+-0.075@E10.0 / 25.010+-0.156@E100.0 | z 31 mm, t 33.41 ns | — |
| NC DIS, Q² threshold | `DIS/NC` | Pythia8 (campaign) | ep | 5 | 139.7 GiB | 1,000,000 | 0.145+-0.089@E10.0 / 24.995+-0.243@E100.0 | z 32 mm, t 34.02 ns | — |
| NC DIS, Q² threshold | `DIS/NC` | Pythia8 (campaign) | ep | 62 | 378.7 GiB | — | 0.145+-0.089@E10.0 / 24.995+-0.243@E100.0 | not recorded | — |
| NC DIS, inclusive | `DIS/pythia8.316-1.0/NC/noRad/ep` | Pythia8.316 | ep | 20 | 27.6 GiB | 1,000,000 | 0.142+-0.064@E10.0 / 25.004+-0.247@E100.0 | z 39 mm, t 39.99 ns | — |
| SIDIS / min-bias photoprod. | `SIDIS/pythia6-eic/1.0.0` | Pythia6-eic | ep | 50 | 60.2 GiB | 1,000,000 | 0.185+-0.092@E10.0 / 25.012+-0.190@E100.0 | z 31 mm, t 33.41 ns | — |
| SIDIS / min-bias photoprod. | `SIDIS/pythia6-eic/1.1.0/en_noradcor` | Pythia6-eic | en | 278 | 216.6 GiB | 2,000,000 | 0.185+-0.092@E10.0 / 25.012+-0.190@E100.0 | z 31 mm, t 33.41 ns | — |
| SIDIS / min-bias photoprod. | `SIDIS/pythia6-eic/1.2.0/ep_noradcor` | Pythia6-eic | ep | 80 | 85.6 GiB | 2,000,000 | 0.185+-0.092@E10.0 / 25.012+-0.190@E100.0 | z 31 mm, t 33.41 ns | — |
| SIDIS open charm D⁰ | `SIDIS/D0_ABCONV/pythia8.306-1.1` | Pythia8 | ep | 20 | 5.5 GiB | 99,031 | 0.185+-0.092@E10.0 / 25.012+-0.190@E100.0 | z 31 mm, t 33.41 ns | — |
| SIDIS open charm D⁰ (eA) | `SIDIS/D0_ABCONV/HFsim-BeAGLE/BeAGLE1.03.01-1.0/eAu` | BeAGLE HFsim | eAu | 998 | 1.9 GiB | 723 | 0.143+-0.066@E10.0 / 24.992+-0.183@E100.8 | z 31 mm, t 33.41 ns | — |
| SIDIS open charm D⁰ (eA) | `SIDIS/D0_ABCONV/HFsim-BeAGLE/BeAGLE1.03.01-2.0/eAu` | BeAGLE HFsim | eAu | 998 | 1.9 GiB | 723 | 0.143+-0.066@E10.0 / 24.992+-0.183@E100.8 | z 31 mm, t 33.41 ns | — |
| SIDIS Λ_c | `SIDIS/Lc_ABCONV/HFsim-PYTHIA/pythia8.306-1.2/ep` | Pythia8 HFsim | ep | 2500 | 1.7 GiB | 303 | 0.185+-0.092@E10.0 / 25.012+-0.190@E100.0 | z 31 mm, t 33.41 ns | — |
| SIDIS Λ_c (eA) | `SIDIS/Lc_ABCONV/HFsim-BeAGLE/BeAGLE1.03.01-1.0/eAu` | BeAGLE HFsim | eAu | 499 | 1.3 GiB | 1,321 | 0.143+-0.066@E10.0 / 24.964+-0.106@E100.8 | z 31 mm, t 33.41 ns | — |
| SIDIS Λ_c (eA) | `SIDIS/Lc_ABCONV/HFsim-BeAGLE/BeAGLE1.03.01-2.0/eAu` | BeAGLE HFsim | eAu | 499 | 1.3 GiB | 1,321 | 0.143+-0.066@E10.0 / 24.964+-0.106@E100.8 | z 31 mm, t 33.41 ns | — |
| SIDIS, Q²-binned | `SIDIS/pythia6/ep_10x100/hepmc_ip6/noradcor` | Pythia6 (IP6 era) | ep | 240 | 404.2 GiB | — | 0.185+-0.092@E10.0 / 25.012+-0.190@E100.0 | z 31 mm, t 33.41 ns | — |
| TCS + BH interference | `EXCLUSIVE/TCS/TCS_BH_TCS+BH` | TCS gen | ep | 20 | 20.8 GiB | — | 0.000+-0.000@E10.0 / 0.000+-0.000@E100.0 | **head-on** | — |
| TCS + BH interference | `EXCLUSIVE/TCS_ABCONV` | TCS gen | ep | 320 | 23.9 GiB | — | 0.151+-0.075@E10.0 / 25.010+-0.156@E100.0 | z 31 mm, t 33.41 ns | — |
| TCS, pure | `EXCLUSIVE/TCS` | TCS gen | ep | 20 | 20.8 GiB | — | 0.000+-0.000@E10.0 / 0.000+-0.000@E100.0 | **head-on** | — |
| coherent φ→K⁺K⁻, eA | `EXCLUSIVE/DIFFRACTIVE_PHI_ABCONV/sartre1.39-1.0/eAu/coherent/bsat` | Sartre | eAu | 1 | 2.4 GiB | 6,894,738 | 0.143+-0.066@E10.0 / 25.013+-0.185@E100.0 | z 31 mm, t 33.41 ns | — |
| coherent/incoherent ρ, eA | `EXCLUSIVE/DIFFRACTIVE_RHO_ABCONV/sartre1.39-1.1/eAu/coherent/bsat` | Sartre | eAu | 1 | 3.5 GiB | 10,000,000 | 0.151+-0.075@E10.0 / 25.010+-0.156@E100.0 | z 31 mm, t 33.41 ns | — |
| diffractive DIS | `DDIS/rapgap3.310-1.0/noRad/ep` | RAPGAP 3.310 | ep | 1 | 5.4 GiB | 5,000,000 | 0.185+-0.092@E10.0 / 25.012+-0.190@E100.0 | z 31 mm, t 33.41 ns | — |
| diffractive J/ψ, ep | `EXCLUSIVE/DIFFRACTIVE_JPSI_ABCONV/lAger3.6.1-1.0` | lAger | ep | 1 | 74.6 MiB | 174,056 | 0.185+-0.092@E10.0 / 25.012+-0.190@E100.0 | z 31 mm, t 33.41 ns | — |
| diffractive φ, ePb/eAu | `EXCLUSIVE/DIFFRACTIVE_PHI_ABCONV/BeAGLE1.03.02-1.1/eAu` | BeAGLE | eAu | 100 | 1.2 GiB | 20,000 | 0.151+-0.075@E10.0 / 25.010+-0.156@E100.9 | z 31 mm, t 33.41 ns | — |
| exclusive ρ→π⁺π⁻ | `EXCLUSIVE/RHO` | SLIGHT | ep | 2 | 177.6 MiB | — | 0.000+-0.000@E10.0 / 0.000+-0.000@E100.0 | **head-on** | — |
| exclusive ρ→π⁺π⁻ | `EXCLUSIVE/RHO_ABCONV` | SLIGHT | ep | 52 | 719.0 MiB | — | 0.151+-0.075@E10.0 / 25.010+-0.156@E100.0 | z 31 mm, t 33.41 ns | — |
| inclusive eA DIS | `DIS/BeAGLE1.03.02-1.0/eAu` | BeAGLE | eAu | 200 | 12.6 GiB | 50,000 | 0.143+-0.066@E10.0 / 25.013+-0.185@E100.9 | z 31 mm, t 33.41 ns | — |
| inclusive eA DIS | `DIS/BeAGLE1.03.02-2.0/eAu` | BeAGLE | eAu | 200 | 12.6 GiB | 50,000 | 0.143+-0.066@E10.0 / 25.013+-0.185@E100.9 | z 31 mm, t 33.41 ns | — |
| meson structure function K⁺Λ | `EXCLUSIVE/MESON_SF_ABCONV/eicMesonSFGen-1.0.0/ep` | eicMesonSFGen | ep | 200 | 425.8 MiB | 5,000 | 0.185+-0.092@E10.0 / 25.012+-0.190@E100.0 | z 31 mm, t 33.41 ns | — |
| spectroscopy ψ(2S)/X/Y | `EXCLUSIVE/SPECTROSCOPY` | dedicated | ep | 6 | 339.9 MiB | — | 0.000+-0.000@E10.0 / 0.000+-0.000@E100.0 | **head-on** | — |
| spectroscopy ψ(2S)/X/Y | `EXCLUSIVE/SPECTROSCOPY_ABCONV` | dedicated | ep | 24 | 2.2 GiB | — | 0.151+-0.075@E10.0 / 25.010+-0.156@E100.0 | z 31 mm, t 33.41 ns | — |
| u-channel ρ | `EXCLUSIVE/UCHANNEL_RHO` | SLIGHT/GENEX | ep | 1 | 35.6 MiB | 100,000 | 0.185+-0.092@E10.0 / 25.012+-0.190@E100.0 | z 31 mm, t 33.41 ns | — |

#### 10x130 — mixable (background recipe complete)

| process | branch | generator | system | files | size | events/file | e⁻ / hadron beam [mrad @ GeV] | beam effects | tape |
|---|---|---|---|---:|---:|---:|---|---|---|
| DEMP π⁺ / K⁺Λ / K⁺Σ⁰ | `EXCLUSIVE/DEMP/DEMPgen-1.2.3` | DEMPgen | ep | 9 | 264.4 MiB | 101,871 | 0.151+-0.075@E10.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |
| DEMP π⁺ / K⁺Λ / K⁺Σ⁰ | `EXCLUSIVE/DEMP/DEMPgen-1.2.4` | DEMPgen | ep | 3 | 331.3 MiB | 400,309 | 0.151+-0.075@E10.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |
| DVCS + BH + INT | `EXCLUSIVE/DVCS_ABCONV/EpIC_v1.1.6-1.0` | EpIC 1.1.6 | ep | 1 | 324.9 MiB | 1,000,000 | 0.151+-0.075@E10.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |
| DVCS + BH + INT | `EXCLUSIVE/DVCS_ABCONV/EpIC_v1.1.6-1.1` | EpIC 1.1.6 | ep | 1 | 324.9 MiB | 1,000,000 | 0.151+-0.075@E10.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |
| DVCS + BH + INT | `EXCLUSIVE/DVCS_ABCONV/EpIC_v1.1.6-1.2` | EpIC 1.1.6 | ep | 2 | 843.7 MiB | 1,300,000 | 0.151+-0.075@E10.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |
| DVMP J/ψ→μ⁺μ⁻ | `EXCLUSIVE/DVMP/JPsi_MuMu_ABCONV/lAger3.6.1-1.0` | lAger | ep | 1 | 1.1 GiB | 2,732,981 | 0.151+-0.075@E10.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |
| DVMP π⁰ | `EXCLUSIVE/DVMP/EpIC1.1.6-1.0/unpolarised` | EpIC | ep | 1 | 374.3 MiB | 1,000,000 | 0.151+-0.075@E10.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |
| NC DIS, inclusive | `DIS/pythia6.428-1.0/NC/noRad/ep` | Pythia6.428 | ep | 40 | 25.0 GiB | 500,000 | 0.151+-0.075@E10.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |
| SIDIS open charm D⁰ | `SIDIS/D0_ABCONV/HFsim-PYTHIA/pythia8.312-2.0/ep` | Pythia8 HFsim | ep | 700 | 2.7 GiB | 1,531 | 0.185+-0.092@E10.0 / 25.012+-0.190@E130.0 | z 31 mm, t 33.41 ns | — |
| diffractive J/ψ, ep | `EXCLUSIVE/DIFFRACTIVE_JPSI_ABCONV/lAger3.6.1-1.0` | lAger | ep | 1 | 85.3 MiB | 199,430 | 0.151+-0.075@E10.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |
| double DVCS | `EXCLUSIVE/DDVCS_ABCONV/EpIC1.1.6-1.1` | EpIC | ep | 2 | 774.1 MiB | 1,000,000 | 0.151+-0.075@E10.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |
| inclusive eA DIS | `DIS/BeAGLE1.03.02-1.0/eH2` | BeAGLE | eH2 | 1 | 1.3 GiB | 1,000,000 | 0.151+-0.075@E10.0 / 25.009+-0.156@E130.3 | z 31 mm, t 33.41 ns | — |
| inclusive eA DIS | `DIS/BeAGLE1.03.02-1.3/eH2/en` | BeAGLE | eH2 | 10 | 12.8 GiB | 1,000,000 | 0.151+-0.075@E10.0 / 25.009+-0.156@E130.3 | z 31 mm, t 33.41 ns | — |
| inclusive eA DIS | `DIS/BeAGLE1.03.02-1.3/eH2/ep` | BeAGLE | eH2 | 10 | 12.8 GiB | 1,000,000 | 0.151+-0.075@E10.0 / 25.009+-0.156@E130.1 | z 31 mm, t 33.41 ns | — |
| meson structure function K⁺Λ | `EXCLUSIVE/MESON_SF_ABCONV/eicMesonSFGen-1.0.0/ep` | eicMesonSFGen | ep | 200 | 425.5 MiB | 5,000 | 0.151+-0.075@E10.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |

#### 10x275 — mixable (background recipe complete)

| process | branch | generator | system | files | size | events/file | e⁻ / hadron beam [mrad @ GeV] | beam effects | tape |
|---|---|---|---|---:|---:|---:|---|---|---|
| CC DIS, Q² threshold | `DIS/CC` | Pythia8 (campaign) | ep | 20 | 165.7 GiB | — | 0.232+-0.140@E10.0 / 25.003+-0.124@E275.0 | not recorded | — |
| NC DIS, Q² threshold | `DIS/NC` | Pythia8 (campaign) | ep | 5 | 171.3 GiB | 1,000,000 | 0.228+-0.100@E10.0 / 25.023+-0.092@E275.0 | z 25 mm, t 25.31 ns | — |
| NC DIS, Q² threshold | `DIS/NC` | Pythia8 (campaign) | ep | 60 | 441.3 GiB | — | 0.228+-0.100@E10.0 / 25.023+-0.092@E275.0 | not recorded | — |
| NC DIS, inclusive | `DIS/pythia8.316-1.0/NC/noRad/ep` | Pythia8.316 | ep | 20 | 31.5 GiB | 1,000,000 | 0.213+-0.156@E10.0 / 25.026+-0.133@E275.0 | z 25 mm, t 28.22 ns | — |
| SIDIS / min-bias photoprod. | `SIDIS/pythia6-eic/1.0.0` | Pythia6-eic | ep | 50 | 75.5 GiB | 1,000,000 | 0.268+-0.134@E10.0 / 25.006+-0.102@E275.1 | z 26 mm, t 28.84 ns | — |

#### 18x275 — mixable (background recipe complete)

| process | branch | generator | system | files | size | events/file | e⁻ / hadron beam [mrad @ GeV] | beam effects | tape |
|---|---|---|---|---:|---:|---:|---|---|---|
| CC DIS, Q² threshold | `DIS/CC` | Pythia8 (campaign) | ep | 20 | 184.7 GiB | — | 0.284+-0.129@E18.0 / 24.957+-0.133@E274.9 | not recorded | — |
| CC DIS, radiative (eRHIC fmt) | `DIS/Djangoh/ep` | DJANGOH/eRHIC | ep | 35 | 97.8 GiB | — | 0.000+-0.000@E18.0 / 0.000+-0.000@E275.0 | **head-on** | — |
| DEMP π⁺ / K⁺Λ / K⁺Σ⁰ | `EXCLUSIVE/DEMP/DEMPgen-1.2.0` | DEMPgen | ep | 60 | 37.6 GiB | 2,271,515 | 0.286+-0.131@E18.0 / 25.008+-0.127@E275.1 | z 26 mm, t 29.28 ns | — |
| DEMP π⁺ / K⁺Λ / K⁺Σ⁰ | `EXCLUSIVE/DEMP/DEMPgen-1.2.2` | DEMPgen | ep | 3 | 260.8 MiB | 452,229 | 0.286+-0.131@E18.0 / 25.008+-0.127@E275.1 | z 26 mm, t 29.28 ns | — |
| DVCS | `EXCLUSIVE/DVCS` | DVCS gen (legacy) | ep | 1 | 823.3 MiB | — | 0.000+-0.000@E18.0 / 0.000+-0.000@E275.0 | **head-on** | — |
| DVCS | `EXCLUSIVE/DVCS_ABCONV` | DVCS gen (legacy) | ep | 12 | 5.8 GiB | — | 0.126+-0.058@E18.0 / 25.002+-0.055@E275.1 | z 26 mm, t 29.28 ns | — |
| DVCS + BH + INT | `EXCLUSIVE/DVCS_ABCONV/EpIC_v1.1.6-1.2` | EpIC 1.1.6 | ep | 2 | 648.0 MiB | 1,000,000 | 0.126+-0.058@E18.0 / 25.002+-0.055@E275.1 | z 26 mm, t 29.28 ns | — |
| DVMP J/ψ→μ⁺μ⁻ | `EXCLUSIVE/DVMP/JPsi_MuMu_ABCONV/lAger3.6.1-1.0` | lAger | ep | 1 | 2.1 GiB | 5,329,042 | 0.126+-0.058@E18.0 / 25.002+-0.055@E275.1 | z 26 mm, t 29.28 ns | — |
| DVMP π⁰ | `EXCLUSIVE/DVMP/EpIC1.1.6-1.1/unpolarised` | EpIC | ep | 1 | 375.1 MiB | 1,000,000 | 0.286+-0.131@E18.0 / 25.008+-0.127@E275.1 | z 26 mm, t 29.28 ns | — |
| NC DIS, Q² threshold | `DIS/NC` | Pythia8 (campaign) | ep | 70 | 515.9 GiB | — | 0.274+-0.144@E18.0 / 24.980+-0.126@E275.0 | not recorded | — |
| NC DIS, inclusive | `DIS/pythia8.316-1.0/NC/noRad/ep` | Pythia8.316 | ep | 20 | 33.9 GiB | 1,000,000 | 0.247+-0.132@E18.0 / 24.980+-0.102@E275.0 | z 40 mm, t 37.22 ns | — |
| NC/CC DIS, radiative | `DIS/DJANGOH4.6.21-1.0/NC/Rad/ep` | DJANGOH 4.6.21 | ep | 4 | 3.2 GiB | 493,566 | 0.286+-0.131@E18.0 / 25.008+-0.127@E275.1 | z 26 mm, t 29.28 ns | — |
| NC/CC DIS, radiative | `DIS/DJANGOH4.6.21-1.0/NC/noRad/ep` | DJANGOH 4.6.21 | ep | 4 | 3.3 GiB | 499,611 | 0.286+-0.131@E18.0 / 25.008+-0.127@E275.1 | z 26 mm, t 29.28 ns | — |
| SIDIS / min-bias photoprod. | `SIDIS/pythia6-eic/1.0.0` | Pythia6-eic | ep | 50 | 69.9 GiB | 1,000,000 | 0.286+-0.131@E18.0 / 25.008+-0.127@E275.1 | z 26 mm, t 29.28 ns | — |
| SIDIS / min-bias photoprod. | `SIDIS/pythia6-eic/1.1.0/en_noradcor` | Pythia6-eic | en | 258 | 183.9 GiB | 1,000,000 | 0.286+-0.131@E18.0 / 25.008+-0.127@E275.1 | z 26 mm, t 29.28 ns | — |
| SIDIS / min-bias photoprod. | `SIDIS/pythia6-eic/1.2.0/ep_noradcor` | Pythia6-eic | ep | 320 | 311.3 GiB | 2,000,000 | 0.286+-0.131@E18.0 / 25.008+-0.127@E275.1 | z 26 mm, t 29.28 ns | — |
| SIDIS dijet (PGF) | `SIDIS/DIJET_ABCONV/pythia6.428-dijet-v1.0/PGF/noRC/ep` | Pythia6.428 dijet | ep | 100 | 972.1 MiB | 4,000 | 0.286+-0.131@E18.0 / 25.008+-0.127@E275.1 | z 26 mm, t 29.28 ns | — |
| SIDIS open charm D⁰ | `SIDIS/D0_ABCONV/pythia8.306-1.0` | Pythia8 | ep | 8 | 6.8 GiB | 180,161 | 0.286+-0.131@E18.0 / 25.008+-0.127@E275.1 | z 26 mm, t 29.28 ns | — |
| SIDIS Λ | `SIDIS/Lambda_ABCONV/pythia8.306-1.0` | Pythia8.306 | ep | 8 | 10.5 GiB | 398,185 | 0.286+-0.131@E18.0 / 25.008+-0.127@E275.1 | z 26 mm, t 29.28 ns | — |
| SIDIS, Q²-binned | `SIDIS/pythia6/ep_18x275/hepmc_ip6/noradcor` | Pythia6 (IP6 era) | ep | 960 | 1.4 TiB | — | 0.286+-0.131@E18.0 / 25.008+-0.127@E275.1 | z 26 mm, t 29.28 ns | — |
| SIDIS, Q²-binned | `SIDIS/pythia6/ep_18x275/hepmc_ip6/radcor` | Pythia6 (IP6 era) | ep | 300 | 506.2 GiB | — | 0.286+-0.131@E18.0 / 25.008+-0.127@E275.1 | z 26 mm, t 29.28 ns | — |
| SIDIS, Q²-binned | `SIDIS/pythia6/ep_5x41/hepmc_ip6/noradcor` ⚠ dir label says ? | Pythia6 (IP6 era) | ep | 740 | 1.4 TiB | 2,000,000 | 0.286+-0.131@E18.0 / 25.008+-0.127@E275.1 | z 26 mm, t 29.28 ns | — |
| TCS + BH interference | `EXCLUSIVE/TCS/TCS_BH_TCS+BH` | TCS gen | ep | 20 | 20.8 GiB | — | 0.000+-0.000@E18.0 / 0.000+-0.000@E275.0 | **head-on** | — |
| TCS + BH interference | `EXCLUSIVE/TCS_ABCONV` | TCS gen | ep | 240 | 17.9 GiB | — | 0.126+-0.058@E18.0 / 25.002+-0.055@E275.1 | z 26 mm, t 29.28 ns | — |
| TCS, pure | `EXCLUSIVE/TCS` | TCS gen | ep | 20 | 20.8 GiB | — | 0.000+-0.000@E18.0 / 0.000+-0.000@E275.0 | **head-on** | — |
| coherent J/ψ photoproduction | `EXCLUSIVE/PHOTOPRODUCTION_JPSI_ABCONV/coherent_ep/eSTARlight1.3.0-1.0` | eSTARlight | ep | 2 | 679.2 MiB | 1,000,000 | 0.286+-0.131@E18.0 / 25.008+-0.127@E275.2 | z 26 mm, t 29.28 ns | — |
| diffractive J/ψ, ep | `EXCLUSIVE/DIFFRACTIVE_JPSI_ABCONV/lAger3.6.1-1.0` | lAger | ep | 1 | 161.6 MiB | 379,402 | 0.286+-0.131@E18.0 / 25.008+-0.127@E275.1 | z 26 mm, t 29.28 ns | — |
| double DVCS | `EXCLUSIVE/DDVCS_ABCONV/EpIC1.1.6-1.0` | EpIC | ep | 4 | 1.5 GiB | 1,000,000 | 0.286+-0.131@E18.0 / 25.008+-0.127@E275.1 | z 26 mm, t 29.28 ns | — |
| meson structure function K⁺Λ | `EXCLUSIVE/MESON_SF_ABCONV/eicMesonSFGen-1.0.0/ep` | eicMesonSFGen | ep | 200 | 430.2 MiB | 5,000 | 0.286+-0.131@E18.0 / 25.008+-0.127@E275.1 | z 26 mm, t 29.28 ns | — |
| u-channel π⁰ | `EXCLUSIVE/UCHANNEL_PI0` | SLIGHT | ep | 1 | 36.3 MiB | 100,000 | 0.286+-0.131@E18.0 / 25.008+-0.127@E275.2 | z 26 mm, t 29.28 ns | — |
| u-channel ω (neutral decay) | `EXCLUSIVE/omega` | SLIGHT | ep | 10 | 250.6 MiB | — | 0.000+-0.000@E18.0 / 0.000+-0.000@E275.1 | **head-on** | — |
| ω photoproduction | `EXCLUSIVE/OMEGA` | SLIGHT | ep | 2 | 201.8 MiB | — | 0.000+-0.000@E18.0 / 0.000+-0.000@E275.1 | **head-on** | — |
| ω photoproduction | `EXCLUSIVE/OMEGA_ABCONV` | SLIGHT | ep | 96 | 1.2 GiB | — | 0.126+-0.058@E18.0 / 25.002+-0.055@E275.2 | z 26 mm, t 29.28 ns | — |

#### 9x100 — no background recipe yet

| process | branch | generator | system | files | size | events/file | e⁻ / hadron beam [mrad @ GeV] | beam effects | tape |
|---|---|---|---|---:|---:|---:|---|---|---|
| SIDIS D_s (eA) | `SIDIS/Ds_ABCONV/HFsim-BeAGLE/BeAGLE1.03.02-1.0/eAu` | BeAGLE HFsim | eAu | 500 | 5.8 GiB | 1,358 | 0.143+-0.066@E9.0 / 25.013+-0.185@E100.9 | z 31 mm, t 33.41 ns | — |
| SIDIS open charm D⁰ (eA) | `SIDIS/D0_ABCONV/HFsim-BeAGLE/BeAGLE1.03.02-1.0/eAu` | BeAGLE HFsim | eAu | 1000 | 8.5 GiB | 1,026 | 0.143+-0.066@E9.0 / 25.013+-0.185@E100.9 | z 31 mm, t 33.41 ns | — |
| SIDIS Λ_c (eA) | `SIDIS/Lc_ABCONV/HFsim-BeAGLE/BeAGLE1.03.02-1.0/eAu` | BeAGLE HFsim | eAu | 500 | 4.1 GiB | 937 | 0.143+-0.066@E9.0 / 25.013+-0.185@E100.9 | z 31 mm, t 33.41 ns | — |
| coherent φ→K⁺K⁻, eA | `EXCLUSIVE/DIFFRACTIVE_PHI_ABCONV/sartre1.39-1.3/eAu/coherent/bsat` | Sartre | eAu | 1 | 3.5 GiB | 10,000,000 | 0.143+-0.066@E9.0 / 25.013+-0.185@E100.0 | z 31 mm, t 33.41 ns | — |
| coherent/incoherent ρ, eA | `EXCLUSIVE/DIFFRACTIVE_RHO_ABCONV/sartre1.39-1.4/eAu/coherent/bsat` | Sartre | eAu | 1 | 3.5 GiB | 10,000,000 | 0.143+-0.066@E9.0 / 25.013+-0.185@E100.0 | z 31 mm, t 33.41 ns | — |
| diffractive φ, ePb/eAu | `EXCLUSIVE/DIFFRACTIVE_PHI_ABCONV/BeAGLE1.03.02-3.1/eAu` | BeAGLE | eAu | 100 | 34.6 GiB | 50,000 | 0.143+-0.066@E9.0 / 25.013+-0.185@E100.9 | z 31 mm, t 33.41 ns | — |
| inclusive eA DIS | `DIS/BeAGLE1.03.02-3.1/eAu` | BeAGLE | eAu | 15 | 49.2 GiB | 397,054 | 0.143+-0.066@E9.0 / 25.013+-0.185@E100.9 | z 31 mm, t 33.41 ns | — |
| meson structure function K⁺Λ | `EXCLUSIVE/MESON_SF_ABCONV/eicMesonSFGen-1.0.0/ep` | eicMesonSFGen | ep | 1000 | 408.9 MiB | 1,000 | 0.185+-0.092@E9.0 / 25.012+-0.190@E100.0 | z 31 mm, t 33.41 ns | — |

#### 9x130 — no background recipe yet

| process | branch | generator | system | files | size | events/file | e⁻ / hadron beam [mrad @ GeV] | beam effects | tape |
|---|---|---|---|---:|---:|---:|---|---|---|
| DEMP π⁺ / K⁺Λ / K⁺Σ⁰ | `EXCLUSIVE/DEMP/DEMPgen-1.2.5` | DEMPgen | ep | 3 | 296.2 MiB | 400,078 | 0.151+-0.075@E9.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |
| DVCS / BH / interference | `EXCLUSIVE/DVCS_ABCONV/EpIC_v1.1.8-1.4/BH_ONLY` | EpIC 1.1.8 | ep | 2 | 551.4 MiB | 1,000,000 | 0.151+-0.075@E9.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |
| DVCS / BH / interference | `EXCLUSIVE/DVCS_ABCONV/EpIC_v1.1.8-1.4/DVCS_BH` | EpIC 1.1.8 | ep | 8 | 2.2 GiB | 1,000,000 | 0.151+-0.075@E9.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |
| DVCS / BH / interference | `EXCLUSIVE/DVCS_ABCONV/EpIC_v1.1.8-1.4/DVCS_ONLY` | EpIC 1.1.8 | ep | 2 | 554.3 MiB | 1,000,000 | 0.151+-0.075@E9.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |
| DVMP J/ψ→μ⁺μ⁻ | `EXCLUSIVE/DVMP/JPsi_MuMu_ABCONV/lAger3.6.1-1.1` | lAger | ep | 1 | 8.8 MiB | 22,458 | 0.151+-0.075@E9.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |
| DVMP π⁰ | `EXCLUSIVE/DVMP/EpIC1.1.8-1.0/unpolarised` | EpIC | ep | 1 | 339.9 MiB | 1,000,000 | 0.151+-0.075@E9.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |
| NC DIS, inclusive | `DIS/pythia8.316-1.0/NC/noRad/ep` | Pythia8.316 | ep | 20 | 28.2 GiB | 1,000,000 | 0.160+-0.088@E9.0 / 25.010+-0.223@E130.0 | z 32 mm, t 33.89 ns | — |
| SIDIS / min-bias photoprod. | `SIDIS/pythia6-eic/1.3.0/ep_noradcor` | Pythia6-eic | ep | 80 | 61.3 GiB | 2,000,000 | 0.151+-0.075@E9.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |
| SIDIS open charm D⁰ | `SIDIS/D0_ABCONV/HFsim-PYTHIA/pythia8.316-1.0/ep` | Pythia8 HFsim | ep | 1000 | 3.0 GiB | 1,186 | 0.151+-0.075@E9.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |
| diffractive DIS | `DDIS/rapgap3.310-2.0/ewRad/ep` | RAPGAP 3.310 | ep | 1 | 2.1 GiB | 2,000,000 | 0.151+-0.075@E9.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |
| diffractive DIS | `DDIS/rapgap3.310-2.0/noRad/ep` | RAPGAP 3.310 | ep | 1 | 2.1 GiB | 2,000,000 | 0.151+-0.075@E9.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |
| diffractive J/ψ, ep | `EXCLUSIVE/DIFFRACTIVE_JPSI_ABCONV/lAger3.7.0-1.0` | lAger | ep | 1 | 7.7 MiB | 19,034 | 0.151+-0.075@E9.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |
| inclusive eA DIS | `DIS/BeAGLE1.03.02-3.1/eH2/en` | BeAGLE | eH2 | 100 | 23.3 GiB | 100,000 | 0.151+-0.075@E9.0 / 25.009+-0.156@E130.3 | z 31 mm, t 33.41 ns | — |
| inclusive eA DIS | `DIS/BeAGLE1.03.02-3.1/eH2/ep` | BeAGLE | eH2 | 100 | 23.1 GiB | 100,000 | 0.151+-0.075@E9.0 / 25.009+-0.156@E130.1 | z 31 mm, t 33.41 ns | — |
| meson structure function K⁺Λ | `EXCLUSIVE/MESON_SF_ABCONV/eicMesonSFGen-1.0.0/ep` | eicMesonSFGen | ep | 1000 | 408.6 MiB | 1,000 | 0.151+-0.075@E9.0 / 25.009+-0.156@E130.0 | z 31 mm, t 33.41 ns | — |
| Υ(1S/2S/3S) threshold | `EXCLUSIVE/UPSILON_ABCONV/eSTARlight1.3.0-1.0/Upsilon1S` | eSTARlight 1.3.0 | ep | 50 | 1.6 GiB | 100,000 | 0.151+-0.075@E9.0 / 25.009+-0.156@E130.1 | z 31 mm, t 33.41 ns | — |
| Υ(1S/2S/3S) threshold | `EXCLUSIVE/UPSILON_ABCONV/eSTARlight1.3.0-1.0/Upsilon2S` | eSTARlight 1.3.0 | ep | 50 | 1.6 GiB | 100,000 | 0.151+-0.075@E9.0 / 25.009+-0.156@E130.1 | z 31 mm, t 33.41 ns | — |
| Υ(1S/2S/3S) threshold | `EXCLUSIVE/UPSILON_ABCONV/eSTARlight1.3.0-1.0/Upsilon3S` | eSTARlight 1.3.0 | ep | 50 | 1.6 GiB | 100,000 | 0.151+-0.075@E9.0 / 25.009+-0.156@E130.1 | z 31 mm, t 33.41 ns | — |

#### 9x275 — no background recipe yet

| process | branch | generator | system | files | size | events/file | e⁻ / hadron beam [mrad @ GeV] | beam effects | tape |
|---|---|---|---|---:|---:|---:|---|---|---|
| CC DIS, radiative, polarised | `DIS/DJANGOH4.6.10-2.0/CC/Rad/eMinus-pMinus` | DJANGOH 4.6.10 | ep | 3 | 1.5 GiB | 999,955 | 0.268+-0.134@E9.0 / 25.006+-0.102@E275.1 | z 26 mm, t 28.84 ns | — |
| CC DIS, radiative, polarised | `DIS/DJANGOH4.6.10-2.0/CC/Rad/eMinus-pPlus` | DJANGOH 4.6.10 | ep | 3 | 1.5 GiB | 999,949 | 0.268+-0.134@E9.0 / 25.006+-0.102@E275.1 | z 26 mm, t 28.84 ns | — |
| DEMP π⁺ / K⁺Λ / K⁺Σ⁰ | `EXCLUSIVE/DEMP/DEMPgen-1.2.5` | DEMPgen | ep | 3 | 295.7 MiB | 400,770 | 0.148+-0.074@E9.0 / 25.002+-0.056@E275.1 | z 26 mm, t 28.84 ns | — |
| DVCS / BH / interference | `EXCLUSIVE/DVCS_ABCONV/EpIC_v1.1.8-1.4/BH_ONLY` | EpIC 1.1.8 | ep | 2 | 1.3 GiB | 2,500,000 | 0.148+-0.074@E9.0 / 25.002+-0.056@E275.1 | z 26 mm, t 28.84 ns | — |
| DVCS / BH / interference | `EXCLUSIVE/DVCS_ABCONV/EpIC_v1.1.8-1.4/DVCS_BH` | EpIC 1.1.8 | ep | 8 | 5.4 GiB | 2,500,000 | 0.148+-0.074@E9.0 / 25.002+-0.056@E275.1 | z 26 mm, t 28.84 ns | — |
| DVCS / BH / interference | `EXCLUSIVE/DVCS_ABCONV/EpIC_v1.1.8-1.4/DVCS_ONLY` | EpIC 1.1.8 | ep | 2 | 1.3 GiB | 2,500,000 | 0.148+-0.074@E9.0 / 25.002+-0.056@E275.1 | z 26 mm, t 28.84 ns | — |
| DVMP J/ψ→μ⁺μ⁻ | `EXCLUSIVE/DVMP/JPsi_MuMu_ABCONV/lAger3.6.1-1.1` | lAger | ep | 1 | 31.2 MiB | 80,058 | 0.148+-0.074@E9.0 / 25.002+-0.056@E275.1 | z 26 mm, t 28.84 ns | — |
| DVMP π⁰ | `EXCLUSIVE/DVMP/EpIC1.1.8-1.0/unpolarised` | EpIC | ep | 2 | 679.7 MiB | 1,000,000 | 0.268+-0.134@E9.0 / 25.006+-0.102@E275.1 | z 26 mm, t 28.84 ns | — |
| NC DIS, inclusive | `DIS/pythia8.316-1.0/NC/noRad/ep` | Pythia8.316 | ep | 20 | 31.1 GiB | 999,999 | 0.234+-0.134@E9.0 / 24.995+-0.104@E275.0 | z 28 mm, t 25.74 ns | — |
| NC DIS, inclusive (EEEMCal cfg) | `DIS/pythia8.315-1.2/EEEMCal/NC/noRad/ep` | Pythia8.315 | ep | 100 | 1.8 GiB | 10,000 | 0.228+-0.117@E9.0 / 24.988+-0.120@E275.0 | z 24 mm, t 25.11 ns | — |
| SIDIS / min-bias photoprod. | `SIDIS/pythia6-eic/1.3.0/ep_noradcor` | Pythia6-eic | ep | 81 | 68.9 GiB | 2,000,000 | 0.268+-0.134@E9.0 / 25.006+-0.102@E275.1 | z 26 mm, t 28.84 ns | — |
| SIDIS D_s | `SIDIS/Ds_ABCONV/HFsim-PYTHIA/pythia8.316-1.1/ep` | Pythia8 HFsim | ep | 1200 | 3.1 GiB | 897 | 0.268+-0.134@E9.0 / 25.006+-0.102@E275.1 | z 26 mm, t 28.84 ns | — |
| SIDIS open charm D⁰ | `SIDIS/D0_ABCONV/HFsim-PYTHIA/pythia8.316-1.0/ep` | Pythia8 HFsim | ep | 1000 | 2.8 GiB | 1,026 | 0.268+-0.134@E9.0 / 25.006+-0.102@E275.1 | z 26 mm, t 28.84 ns | — |
| SIDIS Λ_c | `SIDIS/Lc_ABCONV/HFsim-PYTHIA/pythia8.316-1.0/ep` | Pythia8 HFsim | ep | 1000 | 2.0 GiB | 740 | 0.268+-0.134@E9.0 / 25.006+-0.102@E275.1 | z 26 mm, t 28.84 ns | — |
| diffractive DIS | `DDIS/rapgap3.310-2.0/ewRad/ep` | RAPGAP 3.310 | ep | 1 | 2.3 GiB | 2,000,000 | 0.148+-0.074@E9.0 / 25.002+-0.056@E275.1 | z 26 mm, t 28.84 ns | — |
| diffractive DIS | `DDIS/rapgap3.310-2.0/noRad/ep` | RAPGAP 3.310 | ep | 1 | 2.2 GiB | 2,000,000 | 0.148+-0.074@E9.0 / 25.002+-0.056@E275.1 | z 26 mm, t 28.84 ns | — |
| diffractive J/ψ, ep | `EXCLUSIVE/DIFFRACTIVE_JPSI_ABCONV/lAger3.7.0-1.0` | lAger | ep | 1 | 28.0 MiB | 68,977 | 0.148+-0.074@E9.0 / 25.002+-0.056@E275.1 | z 26 mm, t 28.84 ns | — |
| meson structure function K⁺Λ | `EXCLUSIVE/MESON_SF_ABCONV/eicMesonSFGen-1.0.0/ep` | eicMesonSFGen | ep | 1000 | 410.7 MiB | 1,000 | 0.268+-0.134@E9.0 / 25.006+-0.102@E275.1 | z 26 mm, t 28.84 ns | — |
| Υ(1S/2S/3S) threshold | `EXCLUSIVE/UPSILON_ABCONV/eSTARlight1.3.0-1.0/Upsilon1S` | eSTARlight 1.3.0 | ep | 100 | 3.1 GiB | 100,000 | 0.268+-0.134@E9.0 / 25.006+-0.102@E275.1 | z 26 mm, t 28.84 ns | — |
| Υ(1S/2S/3S) threshold | `EXCLUSIVE/UPSILON_ABCONV/eSTARlight1.3.0-1.0/Upsilon2S` | eSTARlight 1.3.0 | ep | 100 | 3.1 GiB | 100,000 | 0.268+-0.134@E9.0 / 25.006+-0.102@E275.1 | z 26 mm, t 28.84 ns | — |
| Υ(1S/2S/3S) threshold | `EXCLUSIVE/UPSILON_ABCONV/eSTARlight1.3.0-1.0/Upsilon3S` | eSTARlight 1.3.0 | ep | 100 | 3.1 GiB | 100,000 | 0.268+-0.134@E9.0 / 25.006+-0.102@E275.1 | z 26 mm, t 28.84 ns | — |

#### 5x41 — background recipe blocked (3 files missing)

| process | branch | generator | system | files | size | events/file | e⁻ / hadron beam [mrad @ GeV] | beam effects | tape |
|---|---|---|---|---:|---:|---:|---|---|---|
| CC DIS, Q² threshold | `DIS/CC` | Pythia8 (campaign) | ep | 10 | 45.6 GiB | — | 0.156+-0.081@E5.0 / 24.939+-0.257@E41.0 | not recorded | — |
| DEMP π⁺ / K⁺Λ / K⁺Σ⁰ | `EXCLUSIVE/DEMP/DEMPgen-1.1.0` | DEMPgen | ep | 180 | 4.2 GiB | 78,936 | 0.170+-0.073@E5.0 / 25.016+-0.197@E41.0 | z 33 mm, t 35.69 ns | — |
| DEMP π⁺ / K⁺Λ / K⁺Σ⁰ | `EXCLUSIVE/DEMP/DEMPgen-1.2.0` | DEMPgen | ep | 60 | 171.9 GiB | 9,868,034 | 0.170+-0.073@E5.0 / 25.016+-0.197@E41.0 | z 33 mm, t 35.69 ns | — |
| DEMP π⁺ / K⁺Λ / K⁺Σ⁰ | `EXCLUSIVE/DEMP/DEMPgen-1.2.2` | DEMPgen | ep | 6 | 613.6 MiB | 553,488 | 0.170+-0.073@E5.0 / 25.016+-0.197@E41.0 | z 33 mm, t 35.69 ns | — |
| DVCS | `EXCLUSIVE/DVCS` | DVCS gen (legacy) | ep | 3 | 2.4 GiB | — | 0.000+-0.000@E5.0 / 0.000+-0.000@E41.0 | **head-on** | — |
| DVCS | `EXCLUSIVE/DVCS_ABCONV` | DVCS gen (legacy) | ep | 36 | 17.3 GiB | — | 0.170+-0.073@E5.0 / 25.016+-0.197@E41.0 | z 33 mm, t 35.69 ns | — |
| DVCS + BH + INT | `EXCLUSIVE/DVCS_ABCONV/EpIC_v1.1.6-1.2` | EpIC 1.1.6 | ep | 2 | 649.2 MiB | 1,000,000 | 0.170+-0.073@E5.0 / 25.016+-0.197@E41.0 | z 33 mm, t 35.69 ns | — |
| DVCS on deuteron | `EXCLUSIVE/DVCSD_ABCONV` | EpIC | eD | 12 | 12.1 GiB | — | 0.170+-0.073@E5.0 / 25.016+-0.197@E41.0 | z 33 mm, t 35.69 ns | — |
| DVMP π⁰ | `EXCLUSIVE/DVMP/EpIC1.1.6-1.1/unpolarised` | EpIC | ep | 1 | 372.6 MiB | 1,000,000 | 0.170+-0.073@E5.0 / 25.016+-0.197@E41.0 | z 33 mm, t 35.69 ns | — |
| NC DIS, Q² threshold | `DIS/NC` | Pythia8 (campaign) | ep | 5 | 90.6 GiB | 999,990 | 0.149+-0.082@E5.0 / 25.016+-0.186@E41.0 | z 32 mm, t 33.32 ns | — |
| NC DIS, Q² threshold | `DIS/NC` | Pythia8 (campaign) | ep | 61 | 240.6 GiB | — | 0.149+-0.082@E5.0 / 25.016+-0.186@E41.0 | not recorded | — |
| NC DIS, inclusive | `DIS/pythia8.316-1.0/NC/noRad/ep` | Pythia8.316 | ep | 15 | 20.2 GiB | 999,994 | 0.136+-0.055@E5.0 / 25.015+-0.217@E41.0 | z 45 mm, t 44.07 ns | — |
| SIDIS / min-bias photoprod. | `SIDIS/pythia6-eic/1.0.0` | Pythia6-eic | ep | 50 | 59.7 GiB | 1,000,000 | 0.170+-0.073@E5.0 / 25.016+-0.197@E41.0 | z 33 mm, t 35.69 ns | — |
| SIDIS / min-bias photoprod. | `SIDIS/pythia6-eic/1.1.0/en_noradcor` | Pythia6-eic | en | 179 | 175.9 GiB | 2,000,000 | 0.170+-0.073@E5.0 / 25.016+-0.197@E41.0 | z 33 mm, t 35.69 ns | — |
| SIDIS / min-bias photoprod. | `SIDIS/pythia6-eic/1.2.0/ep_noradcor` | Pythia6-eic | ep | 330 | 266.2 GiB | 2,000,000 | 0.170+-0.073@E5.0 / 25.016+-0.197@E41.0 | z 33 mm, t 35.69 ns | — |
| SIDIS open charm D⁰ | `SIDIS/D0_ABCONV/HFsim-PYTHIA/pythia8.306-1.2/ep` | Pythia8 HFsim | ep | 1000 | 1.9 GiB | 887 | 0.170+-0.073@E5.0 / 25.016+-0.197@E41.0 | z 33 mm, t 35.69 ns | — |
| SIDIS open charm D⁰ (eA) | `SIDIS/D0_ABCONV/HFsim-BeAGLE/BeAGLE1.03.01-1.0/eAu` | BeAGLE HFsim | eAu | 952 | 1.4 GiB | 612 | 0.163+-0.071@E5.0 / 25.008+-0.248@E41.3 | z 52 mm, t 54.43 ns | — |
| SIDIS open charm D⁰ (eA) | `SIDIS/D0_ABCONV/HFsim-BeAGLE/BeAGLE1.03.01-2.0/eAu` | BeAGLE HFsim | eAu | 952 | 1.4 GiB | 612 | 0.163+-0.071@E5.0 / 25.008+-0.248@E41.3 | z 52 mm, t 54.43 ns | — |
| SIDIS, Q²-binned | `SIDIS/pythia6/ep_5x41/hepmc_ip6/radcor` | Pythia6 (IP6 era) | ep | 3660 | 187.4 GiB | — | 0.170+-0.073@E5.0 / 25.016+-0.197@E41.0 | z 33 mm, t 35.69 ns | — |
| TCS + BH interference | `EXCLUSIVE/TCS/TCS_BH_TCS+BH` | TCS gen | ep | 20 | 20.8 GiB | — | 0.000+-0.000@E5.0 / 0.000+-0.000@E41.0 | **head-on** | — |
| TCS + BH interference | `EXCLUSIVE/TCS_ABCONV` | TCS gen | ep | 240 | 17.9 GiB | — | 0.170+-0.073@E5.0 / 25.016+-0.197@E41.0 | z 33 mm, t 35.69 ns | — |
| TCS, pure | `EXCLUSIVE/TCS` | TCS gen | ep | 20 | 20.8 GiB | — | 0.000+-0.000@E5.0 / 0.000+-0.000@E41.0 | **head-on** | — |
| diffractive J/ψ, ep | `EXCLUSIVE/DIFFRACTIVE_JPSI_ABCONV/lAger3.6.1-1.0` | lAger | ep | 1 | 29.3 MiB | 66,327 | 0.170+-0.073@E5.0 / 25.016+-0.197@E41.0 | z 33 mm, t 35.69 ns | — |
| inclusive eA DIS | `DIS/BeAGLE1.03.02-1.0/eAu` | BeAGLE | eAu | 200 | 9.9 GiB | 50,000 | 0.163+-0.071@E5.0 / 25.018+-0.253@E41.4 | z 52 mm, t 54.43 ns | — |
| inclusive eA DIS | `DIS/BeAGLE1.03.02-1.2/eHe3` | BeAGLE | eHe3 | 3 | 3.2 GiB | 1,000,000 | 0.163+-0.071@E5.0 / 25.018+-0.253@E41.2 | z 52 mm, t 54.43 ns | — |
| inclusive eA DIS | `DIS/BeAGLE1.03.02-2.0/eAu` | BeAGLE | eAu | 200 | 10.0 GiB | 50,000 | 0.163+-0.071@E5.0 / 25.018+-0.253@E41.4 | z 52 mm, t 54.43 ns | — |
| meson structure function K⁺Λ | `EXCLUSIVE/MESON_SF_ABCONV/eicMesonSFGen-1.0.0/ep` | eicMesonSFGen | ep | 200 | 423.7 MiB | 5,000 | 0.170+-0.073@E5.0 / 25.016+-0.197@E41.0 | z 33 mm, t 35.69 ns | — |

#### 5x100 — background recipe blocked (3 files missing)

| process | branch | generator | system | files | size | events/file | e⁻ / hadron beam [mrad @ GeV] | beam effects | tape |
|---|---|---|---|---:|---:|---:|---|---|---|
| CC DIS, Q² threshold | `DIS/CC` | Pythia8 (campaign) | ep | 20 | 110.1 GiB | — | 0.234+-0.092@E5.0 / 25.046+-0.190@E100.1 | not recorded | — |
| DEMP π⁺ / K⁺Λ / K⁺Σ⁰ | `EXCLUSIVE/DEMP/DEMPgen-1.2.0` | DEMPgen | ep | 60 | 62.8 GiB | 3,663,830 | 0.236+-0.106@E5.0 / 25.011+-0.179@E100.0 | z 31 mm, t 33.41 ns | — |
| NC DIS, Q² threshold | `DIS/NC` | Pythia8 (campaign) | ep | 60 | 330.5 GiB | — | 0.213+-0.090@E5.0 / 24.957+-0.257@E100.0 | not recorded | — |
| NC DIS, inclusive | `DIS/pythia8.316-1.0/NC/noRad/ep` | Pythia8.316 | ep | 20 | 25.0 GiB | 1,000,000 | 0.197+-0.109@E5.0 / 25.029+-0.177@E100.0 | z 40 mm, t 39.45 ns | — |
| SIDIS / min-bias photoprod. | `SIDIS/pythia6-eic/1.0.0` | Pythia6-eic | ep | 50 | 64.7 GiB | 1,000,000 | 0.236+-0.106@E5.0 / 25.011+-0.179@E100.0 | z 31 mm, t 33.41 ns | — |
| TCS, pure | `EXCLUSIVE/TCS` | TCS gen | ep | 20 | 20.8 GiB | — | 0.000+-0.000@E5.0 / 0.000+-0.000@E100.0 | **head-on** | — |
| diffractive J/ψ, ep | `EXCLUSIVE/DIFFRACTIVE_JPSI_ABCONV/lAger3.6.1-1.0` | lAger | ep | 1 | 51.0 MiB | 117,730 | 0.236+-0.106@E5.0 / 25.011+-0.179@E100.0 | z 31 mm, t 33.41 ns | — |

#### 18x108.41 (ePb)

| process | branch | generator | system | files | size | events/file | e⁻ / hadron beam [mrad @ GeV] | beam effects | tape |
|---|---|---|---|---:|---:|---:|---|---|---|
| diffractive J/ψ, ePb | `EXCLUSIVE/DIFFRACTIVE_JPSI_ABCONV/BeAGLE/ePb_18x108.41_tau10_B1.1_Jpsi_highstats` | BeAGLE | ePb | 54 | 112.5 GiB | — | 0.106+-0.068@E18.0 / 25.014+-0.186@E109.4 | z 31 mm, t 33.83 ns | — |
| diffractive φ, ePb/eAu | `EXCLUSIVE/DIFFRACTIVE_PHI_ABCONV/BeAGLE/ePb_18x108.41_tau10_B1.1_Phi_highstats` | BeAGLE | ePb | 54 | 608.6 GiB | — | 0.106+-0.068@E18.0 / 25.014+-0.186@E109.3 | z 31 mm, t 33.83 ns | — |

#### 18x110 (eAu)

| process | branch | generator | system | files | size | events/file | e⁻ / hadron beam [mrad @ GeV] | beam effects | tape |
|---|---|---|---|---:|---:|---:|---|---|---|
| coherent ρ, eA | `EXCLUSIVE/DIFFRACTIVE_RHO/Sartre` | Sartre | eAu | 2 | 23.7 GiB | — | 0.000+-0.000@E18.0 / 0.000+-0.000@E110.0 | **head-on** | — |
| coherent φ→K⁺K⁻, eA | `EXCLUSIVE/DIFFRACTIVE_PHI_ABCONV/Sartre/Coherent` | Sartre | eAu | 8 | 46.1 GiB | — | 0.106+-0.068@E18.0 / 25.014+-0.186@E110.0 | z 31 mm, t 33.83 ns | — |
| coherent φ→K⁺K⁻, eA | `EXCLUSIVE/DIFFRACTIVE_PHI_ABCONV/Sartre/Incoherent` | Sartre | eAu | 4 | 9.1 GiB | — | 0.106+-0.068@E18.0 / 25.014+-0.186@E110.0 | z 31 mm, t 33.83 ns | — |
| coherent/incoherent J/ψ, eA | `EXCLUSIVE/DIFFRACTIVE_JPSI_ABCONV/Sartre/Coherent` | Sartre | eAu | 4 | 24.8 GiB | — | 0.106+-0.068@E18.0 / 25.014+-0.186@E110.0 | z 31 mm, t 33.83 ns | — |
| coherent/incoherent J/ψ, eA | `EXCLUSIVE/DIFFRACTIVE_JPSI_ABCONV/Sartre/Incoherent` | Sartre | eAu | 4 | 7.5 GiB | — | 0.106+-0.068@E18.0 / 25.014+-0.186@E110.0 | z 31 mm, t 33.83 ns | — |
| coherent/incoherent ρ, eA | `EXCLUSIVE/DIFFRACTIVE_RHO_ABCONV/Sartre/Coherent` | Sartre | eAu | 1504 | 30.7 GiB | — | 0.106+-0.068@E18.0 / 25.014+-0.186@E110.0 | z 31 mm, t 33.83 ns | — |
| coherent/incoherent ρ, eA | `EXCLUSIVE/DIFFRACTIVE_RHO_ABCONV/Sartre/Incoherent` | Sartre | eAu | 506 | 10.3 GiB | — | 0.106+-0.068@E18.0 / 25.014+-0.186@E110.0 | z 31 mm, t 33.83 ns | — |
| diffractive J/ψ, eA | `EXCLUSIVE/DIFFRACTIVE_JPSI/Sartre` | Sartre | eAu | 2 | 23.6 GiB | — | 0.000+-0.000@E18.0 / 0.000+-0.000@E110.0 | **head-on** | — |
| diffractive φ, eA | `EXCLUSIVE/DIFFRACTIVE_PHI/BeAGLE` | Sartre/BeAGLE | ep | 200 | 72.0 GiB | — | 0.000+-0.000@E18.0 / 0.000+-0.000@E111.0 | **head-on** | — |
| diffractive φ, eA | `EXCLUSIVE/DIFFRACTIVE_PHI/Sartre` | Sartre/BeAGLE | eAu | 2 | 23.7 GiB | — | 0.000+-0.000@E18.0 / 0.000+-0.000@E110.0 | **head-on** | — |
| diffractive φ, eA | `EXCLUSIVE/DIFFRACTIVE_PHI_ABCONV/eSTARLight` | eSTARlight | eAu | 1 | 54.0 MiB | — | 0.106+-0.068@E18.0 / 25.014+-0.186@E109.8 | z 31 mm, t 33.83 ns | — |

#### Energy not determined (eD, beams did not parse)

| process | branch | generator | system | files | size | events/file | e⁻ / hadron beam [mrad @ GeV] | beam effects | tape |
|---|---|---|---|---:|---:|---:|---|---|---|
| CC DIS, radiative (eRHIC fmt) | `DIS/Djangoh/eD` | DJANGOH/eRHIC | eD | 42 | 92.2 GiB | — | ? / ? | **head-on** | — |
| exclusive ρ→π⁺π⁻ | `EXCLUSIVE/rho` | SLIGHT | ep | 2 | 666.2 MiB | — | ? / ? | **head-on** | — |
| Υ photoproduction (legacy) | `EXCLUSIVE/UPSILON/v1` | eSTARlight | ep | 3 | 9.5 MiB | — | ? / 0.536+-0.727@E0.4 | **head-on** | — |


### 5.5 Usability caveats per branch

#### Head-on branches requiring `abconv`

| process | branch | energy | files | size | afterburned alternative at the same energy |
|---|---|---|---:|---:|---|
| CC DIS, radiative (eRHIC fmt) | `DIS/Djangoh/ep` | 18x275 | 35 | 97.8 GiB | **no — only head-on** |
| CC DIS, radiative (eRHIC fmt) | `DIS/Djangoh/eD` | unknown | 42 | 92.2 GiB | **no — only head-on** |
| DVCS | `EXCLUSIVE/DVCS` | 10x100 | 1 | 823.1 MiB | yes |
| DVCS | `EXCLUSIVE/DVCS` | 18x275 | 1 | 823.3 MiB | yes |
| DVCS | `EXCLUSIVE/DVCS` | 5x41 | 3 | 2.4 GiB | yes |
| DVMP π⁰ | `EXCLUSIVE/DVMP/EpIC1.0.0-1.0` | 10x100 | 1 | 24.8 MiB | yes |
| TCS + BH interference | `EXCLUSIVE/TCS/TCS_BH_TCS+BH` | 10x100 | 20 | 20.8 GiB | yes |
| TCS + BH interference | `EXCLUSIVE/TCS/TCS_BH_TCS+BH` | 18x275 | 20 | 20.8 GiB | yes |
| TCS + BH interference | `EXCLUSIVE/TCS/TCS_BH_TCS+BH` | 5x41 | 20 | 20.8 GiB | yes |
| TCS, pure | `EXCLUSIVE/TCS` | 10x100 | 20 | 20.8 GiB | **no — only head-on** |
| TCS, pure | `EXCLUSIVE/TCS` | 18x275 | 20 | 20.8 GiB | **no — only head-on** |
| TCS, pure | `EXCLUSIVE/TCS` | 5x100 | 20 | 20.8 GiB | **no — only head-on** |
| TCS, pure | `EXCLUSIVE/TCS` | 5x41 | 20 | 20.8 GiB | **no — only head-on** |
| coherent ρ, eA | `EXCLUSIVE/DIFFRACTIVE_RHO/Sartre` | 18x110 | 2 | 23.7 GiB | **no — only head-on** |
| diffractive J/ψ, eA | `EXCLUSIVE/DIFFRACTIVE_JPSI/Sartre` | 18x110 | 2 | 23.6 GiB | **no — only head-on** |
| diffractive φ, eA | `EXCLUSIVE/DIFFRACTIVE_PHI/BeAGLE` | 18x110 | 200 | 72.0 GiB | **no — only head-on** |
| diffractive φ, eA | `EXCLUSIVE/DIFFRACTIVE_PHI/Sartre` | 18x110 | 2 | 23.7 GiB | yes |
| exclusive ρ→π⁺π⁻ | `EXCLUSIVE/RHO` | 10x100 | 2 | 177.6 MiB | yes |
| exclusive ρ→π⁺π⁻ | `EXCLUSIVE/rho` | unknown | 2 | 666.2 MiB | **no — only head-on** |
| spectroscopy ψ(2S)/X/Y | `EXCLUSIVE/SPECTROSCOPY` | 10x100 | 6 | 339.9 MiB | yes |
| u-channel ω (neutral decay) | `EXCLUSIVE/omega` | 18x275 | 10 | 250.6 MiB | **no — only head-on** |
| Υ photoproduction (legacy) | `EXCLUSIVE/UPSILON/v1` | unknown | 3 | 9.5 MiB | **no — only head-on** |
| ω photoproduction | `EXCLUSIVE/OMEGA` | 18x275 | 2 | 201.8 MiB | yes |

23 head-on branches; **12** of them have no afterburned
equivalent at the same energy, so those are the only ones where running
`abconv` ourselves would actually add coverage:

- `DIS/Djangoh/ep` — CC DIS, radiative (eRHIC fmt), ep, 18x275, 35 files, 97.8 GiB
- `DIS/Djangoh/eD` — CC DIS, radiative (eRHIC fmt), eD, unknown, 42 files, 92.2 GiB
- `EXCLUSIVE/DIFFRACTIVE_PHI/BeAGLE` — diffractive φ, eA, ep, 18x110, 200 files, 72.0 GiB
- `EXCLUSIVE/DIFFRACTIVE_RHO/Sartre` — coherent ρ, eA, eAu, 18x110, 2 files, 23.7 GiB
- `EXCLUSIVE/DIFFRACTIVE_JPSI/Sartre` — diffractive J/ψ, eA, eAu, 18x110, 2 files, 23.6 GiB
- `EXCLUSIVE/TCS` — TCS, pure, ep, 18x275, 20 files, 20.8 GiB
- `EXCLUSIVE/TCS` — TCS, pure, ep, 10x100, 20 files, 20.8 GiB
- `EXCLUSIVE/TCS` — TCS, pure, ep, 5x100, 20 files, 20.8 GiB
- `EXCLUSIVE/TCS` — TCS, pure, ep, 5x41, 20 files, 20.8 GiB
- `EXCLUSIVE/rho` — exclusive ρ→π⁺π⁻, ep, unknown, 2 files, 666.2 MiB
- `EXCLUSIVE/omega` — u-channel ω (neutral decay), ep, 18x275, 10 files, 250.6 MiB
- `EXCLUSIVE/UPSILON/v1` — Υ photoproduction (legacy), ep, unknown, 3 files, 9.5 MiB

#### Non-HepMC formats

These hold physics we want but not in a form `ddsim` reads. Found while
sweeping; none were measurable with the HepMC reader.

| branch | format | note |
|---|---|---|
| `EXCLUSIVE/KLambda/Q2_{3,5}`, `EXCLUSIVE/KSigma/Q2_{3,5}` | LUND `.lund` | DEMPgen legacy, `5on41`; 40 files, 8.6 GiB |
| `EXCLUSIVE/meson_MC` | LUND `.dat` | K⁺Λ `10on100`; 6 files, 2.5 GiB |
| `SIDIS/pythia6/ep_5x41/{noradcor,radcor}` | `.hist.root` | histograms only, not events |
| `SIDIS/pythia6/ep_18x100/ep-18x100` | eic-smear `.root` | not HepMC; 60 files, 112 GiB |
| `Djangoh/ep`, `DIS/Djangoh/eD` | eic-smear `.root` / `.hepmc3` | eRHIC-era CC DIS; `.hepmc3` beams did not parse — inspect before use |
| `EXCLUSIVE/UPSILON/v1` | `.hepmc` | records a ~0.4 GeV virtual photon as the beam, with no e/p beam pair — a photoproduction generator convention. Needs the beam pair reconstructed before `abconv`; 3 files, 9.5 MiB |
| `EXCLUSIVE/DVCS+BH+INT.coherent` | single file literally named `18x275`, no extension | 823.3 MiB, excluded from the measurement sweep by the extension filter — **not measured**, afterburner state unknown |

#### One directory is mislabelled

`SIDIS/pythia6/ep_5x41/hepmc_ip6/noradcor` is named 5x41 but its files are
`ep_noradcor.18x275_*` and the beams measure **18x275** (0.286 / 25.008 mrad
at 18.0 / 275.1 GeV). 740 files, 1.4 TiB. Trust the beams, not the path —
this is the one case in 206 branches where the two disagree.

### 5.6 Generator events recovered from `FULL` / `RECO`

The simulated campaign files keep the generator record, so a background-free
`FULL` or `RECO` file can be turned back into HepMC3 by reading `MCParticles`
and dropping the Geant4 secondaries. Checked today on two files:

**`RECO/26.07.1/epic_craterlake/EXCLUSIVE/DVCS_ABCONV/EpIC_v1.1.8-1.4/DVCS_BH/9x275/q2_1_100/emhLm`**
(`…emhLm.0000.eicrecon.edm4eic.root`, 585 MiB, 6849 events, 1304 branches):

- `MCParticles` is present.
- `generatorStatus == 4` gives both beams with the **crossing angle intact** —
  0.200 mrad (e⁻) and 25.087 mrad (p), identical to the parent EVGEN file.
- The beams' `vertex` and `time` carry the smeared interaction point
  (−0.0620, −0.0047, +7.7080) mm, t = −0.0356 ns — matching the EVGEN
  `event_pos`.
- `generatorStatus` histogram of event 0: `{0: 99, 1: 3, 4: 2, 13: 1}` — 5 of
  105 particles are generator-level, the other 99 are Geant4 secondaries.

**`RECO/main/epic_craterlake/Test/…/DIS/NC/18x275/minQ2=1`** (pythia8 NCDIS,
`beamEffects_xAngle=-0.025_hiDiv`), 20 events:

- `generatorStatus` totals `{0: 21, 1: 175, 2: 94, 4: 20, 21: 20, 23: 13,
  41: 4, 42: 4, 43: 4, 44: 6, 61: 10, 62: 14, 63: 13, 71: 13}` — the **full
  Pythia8 record** survives: hard process (21, 23), ISR/FSR (41–44),
  hadronisation (61–63, 71), final state (1). Not just final-state particles,
  so the HepMC3 event can be rebuilt faithfully, not merely approximated.
- Beam angles preserved (0.142 / 24.732 mrad), **but** here the beam particles'
  `vertex` and `time` are exactly zero even though the production is `hiDiv`.
  Checked where it went instead: the `generatorStatus == 1` particles carry it —
  over 10 events their production vertex has z mean +19.6 mm, **rms 39.5 mm**,
  and time rms **0.127 ns**, matching the 35–45 mm vertex-z spread of the parent
  EVGEN files. In event 0 every primary shares one vertex
  (+0.1387, +0.0073, −49.6093) mm at t = +0.116 ns while both beams sit at
  exactly (0, 0, 0, 0). So in this chain the interaction point is on the
  daughters, not on the beams.

So, for the recipe:

1. **Select on `generatorStatus`:** keep 1–4 and the Pythia8 process codes,
   drop `0` (Geant4 secondaries). `0` is the only status that is unambiguously
   not from the generator.
2. **The crossing angle comes for free** — it is already in the momenta, so no
   `abconv` step and no risk of double-applying it.
3. **Read the interaction point per production, don't assume.** Beam-particle
   `vertex`/`time` for the EpIC-style chains, daughter vertices for pythia8
   NCDIS. For timing work this has to be checked for each branch used.
4. **Only background-free branches.** The background-mixed campaign output
   lives under a `Bkg_*` or `BACKGROUNDS` path segment (`Bkg_Exact1S_2us`,
   `Bkg_Exactly1SignalPer2usFrame`, `Bkg_RealisticSignalPer2usFrame`,
   `Bkg_OnlyPer2usFrame`, `Bkg_1SignalPer2usFrame`). Everything in the table
   below has no such segment. 35 background-mixed RECO directories at these
   energies were excluded from it.
5. Marco's `generatorStatus` banding (section 3: 0–99999 background,
   100000 × class for signal) is **his own merged production's convention**,
   not what these campaign files carry — here `generatorStatus` is the plain
   HepMC/Pythia8 status. Don't decode one with the other's scheme.

#### Background-free `RECO` coverage

Campaign versions listed per cell; `main`/`try*`/`Test` paths excluded, and the
35 background-mixed (`Bkg_*` / `BACKGROUNDS`) directories at these energies left
out — we mix ourselves, so only the background-free branches are listed.

Scanned for 5x41, 9x100, 9x130, 9x275, 10x100, 10x130, 10x275 across campaigns
25.10.4 → 26.07.3 and `main`.

**18x275, 5x100 and 18x110** were scanned separately over 25.12.0 → 26.07.1.
18x275 turns out to have the **broadest background-free `RECO` coverage of any
energy** — 15 distinct branches, more than the 9x set:

| RECO branch (background-free) | **18x275** | 5x100 | 18x110 |
|---|---|---|---|
| `DIS/BeAGLE1.03.02-1.2/eHe3` | — | — | 26.02.0, 26.03.1, 26.04.1, 26.07.1 |
| `DIS/CC` | 26.02.0, 26.04.1, 26.07.0, 26.07.1 | 26.02.0, 26.04.1, 26.07.0, 26.07.1 | — |
| `DIS/NC` | 26.02.0, 26.04.1, 26.07.0, 26.07.1 | 26.02.0, 26.04.1, 26.07.0, 26.07.1 | — |
| `DIS/pythia8.316-1.0/NC/noRad/ep` | 26.05.0, 26.06.0, 26.07.1 | 26.05.0, 26.07.1 | — |
| `EXCLUSIVE/DDVCS_ABCONV/EpIC1.1.6-1.0` | 26.02.0, 26.04.1 | — | — |
| `EXCLUSIVE/DIFFRACTIVE_JPSI_ABCONV/lAger3.6.1-1.0` | 26.02.0, 26.04.1, 26.07.1 | 26.02.0, 26.04.1, 26.07.1 | — |
| `EXCLUSIVE/DVCS_ABCONV/EpIC_v1.1.6-1.2` | 26.02.0, 26.04.1 | — | — |
| `EXCLUSIVE/DVMP/EpIC1.1.6-1.1/unpolarised` | 26.02.0, 26.07.1 | — | — |
| `EXCLUSIVE/DVMP/JPsi_MuMu_ABCONV/lAger3.6.1-1.0` | 26.02.0, 26.04.1, 26.07.1 | — | — |
| `EXCLUSIVE/MESON_SF_ABCONV/eicMesonSFGen-1.0.0/ep` | 26.02.0, 26.03.1, 26.04.1, 26.07.1 | — | — |
| `EXCLUSIVE/PHOTOPRODUCTION_JPSI_ABCONV/coherent_ep/eSTARlight1.3.0-1.0` | 26.02.0, 26.04.1 | — | — |
| `SIDIS/D0_ABCONV/pythia8.306-1.0` | 26.02.0, 26.04.1 | — | — |
| `SIDIS/DIJET_ABCONV/pythia6.428-dijet-v1.0/PGF/noRC/ep` | 26.02.0, 26.03.1, 26.04.1 | — | — |
| `SIDIS/pythia6-eic/1.2.0/ep_noradcor` | 26.04.1 | — | — |

`DIS/NC` and `DIS/CC` at 18x275 go back to 22.11.x and
`EXCLUSIVE/{DVCS,TCS}_ABCONV/18x275` to 22.11.3, so older campaigns add more
still. Note that 26.02.0 and 26.04.1 carry processes that 26.07.1 dropped
(`DDVCS_ABCONV`, `DVCS_ABCONV`, `PHOTOPRODUCTION_JPSI_ABCONV`,
`SIDIS/D0_ABCONV`, `SIDIS/DIJET_ABCONV`, `SIDIS/pythia6-eic/1.2.0`) — for
18x275 the newest campaign is **not** the most complete one.

| RECO branch (background-free) | 5x41 | **9x100** | **9x130** | **9x275** | 10x100 | 10x130 | 10x275 | detector |
|---|---|---|---|---|---|---|---|---|
| `DDIS/rapgap3.310-1.0/noRad/ep` | — | — | — | — | 25.12.0, 26.02.0, 26.03.1, 26.04.1, 26.07.1 | — | — | craterlake |
| `DDIS/rapgap3.310-2.0/ewRad/ep` | — | — | 26.07.1 | 26.07.1 | — | — | — | craterlake |
| `DDIS/rapgap3.310-2.0/noRad/ep` | — | — | 26.07.1 | 26.07.1 | — | — | — | craterlake |
| `DIS/BeAGLE1.03.02-1.0/eAu` | 25.12.0 | — | — | — | 25.12.0 | — | — | craterlake_without_zdc |
| `DIS/BeAGLE1.03.02-1.0/eH2` | — | — | — | — | — | 25.12.0, 26.03.1 | — | craterlake |
| `DIS/BeAGLE1.03.02-1.2/eHe3` | 25.12.0, 26.02.0, 26.03.1, 26.04.1, 26.07.1 | — | — | — | — | — | — | craterlake |
| `DIS/BeAGLE1.03.02-1.3/eH2/en` | — | — | — | — | — | 26.03.1, 26.04.1 | — | craterlake |
| `DIS/BeAGLE1.03.02-1.3/eH2/ep` | — | — | — | — | — | 26.03.1, 26.04.1 | — | craterlake |
| `DIS/BeAGLE1.03.02-2.0/eAu` | 26.02.0, 26.03.1, 26.04.1 | — | — | — | 26.02.0, 26.03.1, 26.04.1 | — | — | craterlake_without_zdc |
| `DIS/BeAGLE1.03.02-3.1/eAu` | — | 26.07.1 | — | — | — | — | — | craterlake |
| `DIS/BeAGLE1.03.02-3.1/eH2/en` | — | — | 26.07.1 | — | — | — | — | craterlake |
| `DIS/BeAGLE1.03.02-3.1/eH2/ep` | — | — | 26.07.1 | — | — | — | — | craterlake |
| `DIS/CC` | 25.12.0, 26.02.0, 26.04.1, 26.07.0, 26.07.1 | — | — | — | 25.12.0, 26.02.0, 26.04.1, 26.07.0, 26.07.1 | — | 25.12.0, 26.02.0, 26.04.1, 26.07.0, 26.07.1 | craterlake |
| `DIS/DJANGOH4.6.10-2.0/CC/Rad/eMinus-pMinus` | — | — | — | 26.07.1 | — | — | — | craterlake |
| `DIS/DJANGOH4.6.10-2.0/CC/Rad/eMinus-pPlus` | — | — | — | 26.07.1 | — | — | — | craterlake |
| `DIS/NC` | 25.12.0, 26.02.0, 26.03.0, 26.04.1, 26.07.1 | — | — | — | 25.12.0, 26.02.0, 26.03.0, 26.04.1, 26.07.0, 26.07.1 | — | 25.12.0, 26.02.0, 26.03.0, 26.04.1, 26.07.0, 26.07.1 | craterlake |
| `DIS/pythia6.428-1.0/NC/noRad/ep` | — | — | — | — | — | 25.12.0, 26.03.1, 26.04.1 | — | craterlake |
| `DIS/pythia8.315-1.2/EEEMCal/NC/noRad/ep` | — | — | — | 26.07.1 | — | — | — | craterlake |
| `DIS/pythia8.316-1.0/NC/noRad/ep` | 26.05.0 | — | 26.05.0, 26.06.0, 26.07.1 | 26.05.0, 26.06.0, 26.07.1 | 26.05.0, 26.06.0, 26.07.1 | — | 26.05.0, 26.06.0, 26.07.1 | craterlake |
| `EXCLUSIVE/DDVCS_ABCONV/EpIC1.1.6-1.1` | — | — | — | — | — | 26.03.1, 26.04.1 | — | craterlake |
| `EXCLUSIVE/DEMP/DEMPgen-1.2.2` | 25.12.0 | — | — | — | 25.12.0 | — | — | craterlake |
| `EXCLUSIVE/DEMP/DEMPgen-1.2.3` | — | — | — | — | — | 25.12.0 | — | craterlake |
| `EXCLUSIVE/DEMP/DEMPgen-1.2.4` | — | — | — | — | — | 25.12.0, 26.02.0, 26.04.1 | — | craterlake |
| `EXCLUSIVE/DEMP/DEMPgen-1.2.5` | — | — | 26.07.1 | 26.07.1 | — | — | — | craterlake |
| `EXCLUSIVE/DIFFRACTIVE_JPSI_ABCONV/lAger3.6.1-1.0` | 25.12.0, 26.02.0, 26.04.1, 26.07.1 | — | — | — | 25.12.0, 26.02.0, 26.04.1, 26.07.1 | 25.12.0, 26.02.0, 26.04.1 | — | craterlake |
| `EXCLUSIVE/DIFFRACTIVE_JPSI_ABCONV/lAger3.7.0-1.0` | — | — | 26.07.1 | 26.07.1 | — | — | — | craterlake |
| `EXCLUSIVE/DIFFRACTIVE_PHI_ABCONV/BeAGLE1.03.02-1.1/eAu` | — | — | — | — | 25.12.0, 26.02.0, 26.04.1 | — | — | craterlake |
| `EXCLUSIVE/DIFFRACTIVE_PHI_ABCONV/BeAGLE1.03.02-3.1/eAu` | — | 26.07.1 | — | — | — | — | — | craterlake |
| `EXCLUSIVE/DIFFRACTIVE_PHI_ABCONV/sartre1.39-1.0/eAu/coherent/bsat` | — | — | — | — | 25.12.0, 26.02.0, 26.04.1 | — | — | craterlake |
| `EXCLUSIVE/DIFFRACTIVE_PHI_ABCONV/sartre1.39-1.3/eAu/coherent/bsat` | — | 26.07.1 | — | — | — | — | — | craterlake |
| `EXCLUSIVE/DIFFRACTIVE_RHO_ABCONV/sartre1.39-1.1/eAu/coherent/bsat` | — | — | — | — | 25.12.0, 26.02.0, 26.04.1 | — | — | craterlake |
| `EXCLUSIVE/DIFFRACTIVE_RHO_ABCONV/sartre1.39-1.4/eAu/coherent/bsat` | — | 26.07.1 | — | — | — | — | — | craterlake |
| `EXCLUSIVE/DVCS_ABCONV` | 25.12.0 | — | — | — | 25.12.0 | — | — | craterlake |
| `EXCLUSIVE/DVCS_ABCONV/EpIC_v1.1.6-1.1` | — | — | — | — | — | 25.12.0 | — | craterlake |
| `EXCLUSIVE/DVCS_ABCONV/EpIC_v1.1.6-1.2` | 26.02.0, 26.04.1 | — | — | — | 26.02.0, 26.04.1 | 26.02.0, 26.04.1 | — | craterlake |
| `EXCLUSIVE/DVCS_ABCONV/EpIC_v1.1.8-1.4/BH_ONLY` | — | — | 26.07.1 | 26.07.1 | — | — | — | craterlake |
| `EXCLUSIVE/DVCS_ABCONV/EpIC_v1.1.8-1.4/DVCS_BH` | — | — | 26.07.1 | 26.07.1 | — | — | — | craterlake |
| `EXCLUSIVE/DVCS_ABCONV/EpIC_v1.1.8-1.4/DVCS_ONLY` | — | — | 26.07.1 | 26.07.1 | — | — | — | craterlake |
| `EXCLUSIVE/DVMP/EpIC1.1.6-1.0/unpolarised` | — | — | — | — | — | 25.12.0, 26.02.0 | — | craterlake |
| `EXCLUSIVE/DVMP/EpIC1.1.6-1.1/unpolarised` | 25.12.0, 26.02.0, 26.07.1 | — | — | — | — | — | — | craterlake |
| `EXCLUSIVE/DVMP/EpIC1.1.8-1.0/unpolarised` | — | — | 26.07.1 | 26.07.1 | — | — | — | craterlake |
| `EXCLUSIVE/DVMP/JPsi_MuMu_ABCONV/lAger3.6.1-1.0` | — | — | — | — | — | 25.12.0, 26.02.0, 26.04.1 | — | craterlake |
| `EXCLUSIVE/DVMP/JPsi_MuMu_ABCONV/lAger3.6.1-1.1` | — | — | 26.07.1 | 26.07.1 | — | — | — | craterlake |
| `EXCLUSIVE/MESON_SF_ABCONV/eicMesonSFGen-1.0.0/ep` | 26.02.0, 26.03.1, 26.04.1, 26.07.1 | 26.07.1 | 26.07.1 | 26.07.1 | 26.02.0, 26.03.1, 26.04.1, 26.07.1 | 26.02.0, 26.03.1, 26.04.1 | — | craterlake |
| `EXCLUSIVE/UCHANNEL_RHO` | — | — | — | — | 25.12.0 | — | — | craterlake |
| `EXCLUSIVE/UPSILON_ABCONV/eSTARlight1.3.0-1.0/Upsilon1S` | — | — | 26.07.1 | 26.07.1 | — | — | — | craterlake |
| `EXCLUSIVE/UPSILON_ABCONV/eSTARlight1.3.0-1.0/Upsilon2S` | — | — | 26.07.1 | 26.07.1 | — | — | — | craterlake |
| `EXCLUSIVE/UPSILON_ABCONV/eSTARlight1.3.0-1.0/Upsilon3S` | — | — | 26.07.1 | 26.07.1 | — | — | — | craterlake |
| `SIDIS/D0_ABCONV/HFsim-BeAGLE/BeAGLE1.03.01-2.0/eAu` | 25.12.0, 26.03.1, 26.04.1 | — | — | — | 25.12.0, 26.03.1, 26.04.1 | — | — | craterlake_without_zdc |
| `SIDIS/D0_ABCONV/HFsim-BeAGLE/BeAGLE1.03.02-1.0/eAu` | — | 26.07.1 | — | — | — | — | — | craterlake |
| `SIDIS/D0_ABCONV/HFsim-PYTHIA/pythia8.306-1.2/ep` | 25.12.0, 26.02.0, 26.03.1, 26.04.1 | — | — | — | — | — | — | craterlake |
| `SIDIS/D0_ABCONV/HFsim-PYTHIA/pythia8.312-2.0/ep` | — | — | — | — | — | 26.03.1, 26.04.1 | — | craterlake |
| `SIDIS/D0_ABCONV/HFsim-PYTHIA/pythia8.316-1.0/ep` | — | — | 26.07.1 | 26.07.1 | — | — | — | craterlake |
| `SIDIS/D0_ABCONV/pythia8.306-1.1` | — | — | — | — | 25.12.0, 26.02.0, 26.03.0, 26.04.1 | — | — | craterlake |
| `SIDIS/Ds_ABCONV/HFsim-BeAGLE/BeAGLE1.03.02-1.0/eAu` | — | 26.07.1 | — | — | — | — | — | craterlake |
| `SIDIS/Ds_ABCONV/HFsim-PYTHIA/pythia8.316-1.1/ep` | — | — | — | 26.07.1 | — | — | — | craterlake |
| `SIDIS/Lc_ABCONV/HFsim-BeAGLE/BeAGLE1.03.01-2.0/eAu` | — | — | — | — | 25.12.0, 26.03.1, 26.04.1 | — | — | craterlake_without_zdc |
| `SIDIS/Lc_ABCONV/HFsim-BeAGLE/BeAGLE1.03.02-1.0/eAu` | — | 26.07.1 | — | — | — | — | — | craterlake |
| `SIDIS/Lc_ABCONV/HFsim-PYTHIA/pythia8.306-1.2/ep` | — | — | — | — | 25.12.0, 26.02.0, 26.03.1, 26.04.1 | — | — | craterlake |
| `SIDIS/Lc_ABCONV/HFsim-PYTHIA/pythia8.316-1.0/ep` | — | — | — | 26.07.1 | — | — | — | craterlake |
| `SIDIS/pythia6-eic/1.0.0` | — | — | — | — | 26.03.0 | — | 26.03.0 | craterlake |
| `SIDIS/pythia6-eic/1.2.0/ep_noradcor` | — | — | — | — | 26.04.1 | — | — | craterlake |
| `SIDIS/pythia6-eic/1.3.0/ep_noradcor` | — | — | 26.07.1 | 26.07.1 | — | — | — | craterlake |
| `Test/2025-10-17_14-30-00/EXCLUSIVE/DVCS_ABCONV` | main | — | — | — | — | — | — | craterlake |
| `Test/2025-11-24_07-22-00/1Bkg_1SignalPer2usFrame/Synrad_10GeV_Vac_10000Ahr_Runtime_50s_Egas_10GeV_Hgas_275GeV/DIS/NC` | — | — | — | — | — | — | main | craterlake |
| `Test/2025-11-24_15-22-00/1Bkg_1SignalPer2usFrame/Synrad_10GeV_Vac_10000Ahr_Runtime_50s_Egas_10GeV_Hgas_275GeV/DIS/NC` | — | — | — | — | — | — | main | craterlake |
| `Test/2025-11-25_15-22-00/1Bkg_1SignalPer2usFrame/Synrad_10GeV_Vac_10000Ahr_Runtime_50s_Egas_10GeV_Hgas_275GeV/DIS/NC` | — | — | — | — | — | — | main | craterlake |
| `Test/2025-11-25_22-22-00/1Bkg_1SignalPer2usFrame/Synrad_10GeV_Vac_10000Ahr_Runtime_50s_Egas_10GeV_Hgas_275GeV/DIS/NC` | — | — | — | — | — | — | main | craterlake |
| `Test/2025-11-25_22-43-00/1Bkg_1SignalPer2usFrame/Synrad_10GeV_Vac_10000Ahr_Runtime_50s_Egas_10GeV_Hgas_275GeV/DIS/NC` | — | — | — | — | — | — | main | craterlake |
| `Test/2025-11-27_23-43-00/Bkg_1SignalPer2usFrame/DIS/NC` | — | — | — | — | — | — | main | craterlake |
| `Test/2025-11-28_23-50-00/Bkg_1SignalPer2usFrame/DIS/NC` | — | — | — | — | — | — | main | craterlake |
| `Test/2025-11-28_23-55-00/Bkg_1SignalPer2usFrame/DIS/NC` | — | — | — | — | — | — | main | craterlake |

<!-- 35 background-mixed RECO directories at these energies were excluded -->

This is what makes 9 GeV workable: `FULL` has nothing at 9x (section 5.1a), but
`RECO` **26.07.1** covers essentially the whole 9x130 / 9x275 generator set, and
`RECO` 26.05.0 / 26.06.0 / 26.07.1 cover `DIS/pythia8.316-1.0/NC` at both.

**Staging caveat.** These files are largely tape-resident. The 9x `RECO`
directories on `/volatile` and `/cache` exist but are mostly **empty** —
`EXCLUSIVE/DVCS_ABCONV/EpIC_v1.1.8-1.4/{DVCS_BH,DVCS_ONLY,BH_ONLY}/{9x130,9x275}`
were the only 9x `RECO` branches with files on disk today. The XRootD door
`root://dtn2304.jlab.org:8443//jlab-osdf-ro/eic/EPIC/{volatile,cache,work}/…`
serves only the disk stores, so it cannot reach the purged files either —
anything else has to be staged from `/mss` with `jcache` first.

### 5.7 Recommendations and open requests

Framed as decided: **we add background ourselves**, so what we need from the
collaboration is background-free physics events plus the per-source background
inputs — not anybody's pre-mixed production.

**1. Work at 10x100, 10x130, 10x275 and 18x275 now.** These are the four
energies where all five background sources are on disk (section 5.1b), and
between them they carry the widest signal coverage in the catalogue. 18x275 has
the largest statistics by far (the `SIDIS/pythia6` 18x275 branches alone are
1.4 TiB + 506 GiB) and the lowest SynRad rate; 10x275 vacuum is the busiest
occupancy. Having both lets us train and test across an order of magnitude in
background rate rather than at a single point.

**2. 9 GeV is signal-ready and background-blocked.** 9x275 and 9x130 have
afterburned generator data for a broad set of processes; 9x100 is an eA point
with almost nothing in ep. What is missing is only the **rate table**: the
campaign already reuses the 10x275 SynRad / Coulomb / Touschek *files* for
10x100 and 10x130 with nothing changed but `freq`, so the same reuse at 9x
needs numbers, not new simulation. Worth asking for explicitly, since the
samples are already there.

**3. 5x41 and 5x100 are blocked by three files**, not by a missing recipe:
`BEAMGAS/electron/GETaLM1.0.0-1.1/5GeV/…`,
`SYNRAD/dataprod_rel_1.0.0/5x100/…preproc_10000repeats…`, and (5x41 only)
`BEAMGAS/proton/pythia8.306-1.0/41GeV/combined/…`. If a low-energy point matters,
asking for those three is a much smaller request than a new production.

**4. `edm2hepmc` is worth building — `RECO` keeps the generator record.**
`RECO` keeps `MCParticles` with the crossing angle already applied and the full
Pythia8 history intact (section 5.6, measured on two files). That makes `RECO`
a first-class source, not a fallback: it covers 9x where `FULL` has nothing, and
it is tape-backed where much of EVGEN is not. Selection rule is simply
`generatorStatus != 0`; the interaction-point offset has to be read per
production (beam particles for the EpIC-style chains, daughter vertices for
pythia8 NCDIS).

**5. Nothing is being staged.** Per instruction, no `jcache`. Everything above
was established from directory metadata plus files already resident on
`/volatile` / `/cache`.

**6. Durability — most of EVGEN is not archived.** Branches whose directory also
exists under `/mss`. Counted over the seven energies of the first pass only
(18x275, 5x100 and the eA points are not in this tally):

   | Energy | tape-backed branches | `/volatile`-only |
   |---|---:|---:|
   | 5x41 | 5 / 25 | 20 |
   | 9x100 | **0 / 8** | 8 |
   | 9x130 | 5 / 18 | 13 |
   | 9x275 | 8 / 21 | 13 |
   | 10x100 | 5 / 31 | 26 |
   | 10x130 | 4 / 15 | 11 |
   | 10x275 | 2 / 4 | 2 |

   `/volatile` is purgeable scratch. This is another argument for the
   `edm2hepmc` route: `RECO/26.07.1` is on tape and covers nearly the whole 9x
   set, so the generator record survives a purge even where the EVGEN copy does
   not.

**7. Corrections to carry forward.** Two things in Marco's table are wrong as a
guide to availability, and one of my own earlier readings was wrong:

- `rho` (23), `spectroscopy` (24) and `omega` (25) all **have** afterburned
  generator data — `EXCLUSIVE/RHO_ABCONV` (10x100), `SPECTROSCOPY_ABCONV`
  (10x100), `OMEGA_ABCONV` (18x275). They are invisible to a path-name search
  because the energy is in the **filename**, not a directory segment; I reported
  them as empty earlier in this survey and that was wrong.
- `tcs` is ambiguous in his table. `TCS_ABCONV` is the **TCS+BH interference**
  sample (files `tcs_bh_int_ab_hiAcc_*`); **pure TCS exists only head-on**, at
  5x41, 5x100, 10x100 and 18x275, 20 files / 20.8 GiB each. If the class means
  pure TCS, `abconv` has to be run; if it means the interference sample, it is
  ready at 5x41, 10x100 and 18x275.
- `cohrho` / `cohphi` are eAu-only by definition, and the bulk of them sit at
  **18x110**, an energy not in the original request.

## 6. Access verified 2026-10-15

| Item | Result |
|---|---|
| ifarm tunnel | `ssh -p 4333 romanov@localhost` → `ifarm2401.jlab.org`, user `romanov`. Works. |
| Rucio client | `apptainer exec /cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:nightly rucio …` → rucio **40.2.0** |
| Rucio identity | `rucio whoami` → account **`eicread`** (GROUP, ACTIVE) — read-only, which is what we want |
| Rucio scopes | `ying_test`, `test`, `eic`, `panta`, `rahmans`, **`epic`** |
| Rucio content | `epic:` indexes campaign output (`epic:/RECO/<ver>/…`, `epic:/FULL/…`) and generator datasets (`epic:/EVGEN/…`) — but **only partially**: 121 `EVGEN` DIDs and 197 `FULL` DIDs in total. Whole process trees that exist on disk are absent from Rucio (`EXCLUSIVE/TCS`, `OMEGA_ABCONV`, `SPECTROSCOPY_ABCONV`, `RHO_ABCONV`, `DEMPgen-1.2.4`, `DEMPgen-1.2.5`, …). **Rucio is not the inventory.** |
| Store hierarchy, measured | `/volatile` ⊇ tape ⊇ Rucio. 414 target-energy EVGEN directories on `/volatile` vs 105 on `/mss`, and **every** `/mss` target-energy EVGEN directory also exists on `/volatile` (`comm -23` empty). So: `/volatile` = the inventory, `/mss` = the durability check (a `/volatile`-only dataset is purgeable), Rucio = a partial index that adds replica/RSE information for the DIDs it does carry. |
| EVGEN on disk | `/volatile/eic/EPIC/EVGEN/{BACKGROUNDS,CI,DDIS,DIS,Djangoh,EW_BSM,EXCLUSIVE,SIDIS,SINGLE,Test}`; partial mirror in `/cache/eic/EPIC/EVGEN/{BACKGROUNDS,DIS,EXCLUSIVE,SIDIS,Test}` |
| Campaign config repo | `github.com/eic/simulation_campaign_datasets` cloned locally; has `config_data/*.json` (background rates per energy incl. 10x130, 10x100, 10x275, 5x41, 5x100, 18x275) and per-process `config.yml` + `*.csv` dataset listings |
| Local space | `/data` 951 GB free (bulk); scratchpad is tmpfs, 7.8 GB free (text only) |
| Farm write space | `/w/eic-scshelf2104/users/romanov/optim-out` exists and is writable — not needed for listing work |

---

## 7. Appendix: reproducing the sweep

All of it is read-only on the data. The only writes anywhere on the farm were
a handful of ~kB helper scripts in ifarm's `/tmp`, removed afterwards; nothing
was written under `/work`, `/volatile`, `/cache`, `/mss` or `/w/…`. Commands
go over the tunnel as `ssh -p 4333 -o BatchMode=yes romanov@localhost bash -s
<<'EOF' … EOF` (ifarm's login shell is tcsh, so the script must arrive on
stdin), and Rucio / ROOT run inside
`/cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:nightly`.

### 7.1 Inventory dumps

```bash
# Rucio (partial index): 121 EVGEN DIDs, 197 FULL DIDs, 105 background-mixed
apptainer exec /cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:nightly \
  rucio did list 'epic:/EVGEN/*'

# the real inventory
find /volatile/eic/EPIC/EVGEN -maxdepth 10 -type d
find /volatile/eic/EPIC/FULL  -maxdepth 9  -type d
find /mss/eic/EPIC/RECO/26.07.1 -maxdepth 8 -type d -name '9x*'

# per-leaf file count and size
find "$d" -maxdepth 1 -type f | wc -l; du -sb "$d"
```

### 7.2 Afterburner measurement

Needs `-B /volatile:/volatile:ro` (otherwise `TFile::Open` reports *does not
exist*) and a writable `TMPDIR`. Do **not** add `python3 -I` — isolated mode
hides ROOT from the interpreter.

```bash
apptainer exec -B /tmp:/tmp -B /volatile:/volatile:ro \
  /cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:nightly \
  env TMPDIR=/tmp HOME=/tmp python3 /tmp/measure_remote.py --root < list.tsv
```

`measure_remote.py` (reads `.hepmc3.tree.root` with `--root`, plain
`.hepmc` ASCII without it; input is TSV `file<TAB>dir<TAB>energy<TAB>nfiles<TAB>bytes`):

```python
import sys, math, statistics as st, os, gzip
def ascii_scan(path, nev=20):
    op = gzip.open if path.endswith(".gz") else open
    beams={}; pos=[]; nE=0
    with op(path, "rt", errors="replace") as fh:
        for line in fh:
            if line.startswith("E "):
                nE += 1
                if nE > nev: break
                f=line.split()
                if "@" in f:
                    i=f.index("@")
                    try: pos.append(tuple(float(x) for x in f[i+1:i+5]))
                    except Exception: pass
            elif line.startswith("P ") and nE>0:
                f=line.split()
                # P <id> <parent> <pid> px py pz e m status
                if len(f)>=10 and f[9]=="4":
                    pid=int(f[3]); px,py,pz=float(f[4]),float(f[5]),float(f[6])
                    beams.setdefault(pid,[]).append(math.atan2(math.hypot(px,py),abs(pz))*1000.0)
    return beams, pos, None
def root_scan(path, nev=20):
    import ROOT
    f=ROOT.TFile.Open(path)
    tname=next(k.GetName() for k in f.GetListOfKeys() if k.GetClassName()=="TTree")
    t=f.Get(tname); bn=t.GetListOfBranches()[0].GetName(); n=t.GetEntries()
    beams={}; pos=[]
    for i in range(min(nev,n)):
        t.GetEntry(i); ev=getattr(t,bn)
        for p in ev.particles:
            if p.status==4:
                m=p.momentum
                beams.setdefault(p.pid,[]).append(math.atan2(math.hypot(m.px(),m.py()),abs(m.pz()))*1000.0)
        got=False
        try:
            ep=ev.event_pos
            if any(abs(v)>1e-12 for v in (ep.x(),ep.y(),ep.z(),ep.t())):
                pos.append((ep.x(),ep.y(),ep.z(),ep.t())); got=True
        except Exception: pass
        if not got:
            try:
                v=ev.vertices[0].position
                pos.append((v.x(),v.y(),v.z(),v.t()))
            except Exception: pass
    f.Close()
    return beams, pos, n
def fmt(beams,pos,n):
    out=[]
    for pid in sorted(beams, key=lambda k: -abs(k)):
        a=beams[pid]
        out.append(f"{pid}:{st.mean(a):.3f}+-{(st.pstdev(a) if len(a)>1 else 0):.3f}")
    ang="|".join(out)
    if pos:
        zs=[p[2] for p in pos]; ts=[p[3] for p in pos]; xs=[p[0] for p in pos]
        vtx=f"x_rms={st.pstdev(xs) if len(xs)>1 else 0:.4f};z_rms={st.pstdev(zs) if len(zs)>1 else 0:.3f};t_rms={st.pstdev(ts) if len(ts)>1 else 0:.3f}"
    else:
        vtx="no_event_pos"
    return ang, vtx, (n if n is not None else "")
if __name__=="__main__":
    if len(sys.argv)>1 and sys.argv[1]=="--root":
        import ROOT; ROOT.gSystem.Load("libHepMC3rootIO"); ROOT.gErrorIgnoreLevel=ROOT.kFatal
    for line in sys.stdin:
        line=line.rstrip("\n")
        if not line: continue
        fp, d, e, nf, b = line.split("\t")
        isroot = fp.endswith(".root")
        want_root = (len(sys.argv)>1 and sys.argv[1]=="--root")
        if isroot != want_root: continue
        try:
            beams,pos,n = (root_scan if isroot else ascii_scan)(fp)
            ang,vtx,nn = fmt(beams,pos,n)
            print(f"{d}\t{e}\t{nf}\t{b}\t{os.path.basename(fp)}\t{nn}\t{ang}\t{vtx}", flush=True)
        except Exception as ex:
            print(f"{d}\t{e}\t{nf}\t{b}\t{os.path.basename(fp)}\tERR\t{type(ex).__name__}: {ex}\t", flush=True)
```

### 7.3 Reading `MCParticles` out of a RECO file

```python
import math, collections, ROOT
f = ROOT.TFile.Open(path)                  # …eicrecon.edm4eic.root
t = f.Get("events")
t.GetEntry(0)
mc = t.MCParticles
for p in mc:
    if p.generatorStatus == 4:             # the two beams
        m, v = p.momentum, p.vertex
        ang = math.atan2(math.hypot(m.x, m.y), abs(m.z)) * 1000   # mrad
        print(p.PDG, ang, (v.x, v.y, v.z), p.time)
print(collections.Counter(p.generatorStatus for p in mc))
# keep generatorStatus != 0 to rebuild the generator record; 0 = Geant4 secondary
```

No podio or edm4hep dictionary load is needed — ROOT 6.40 in `eic_xl` picks
them up from the rootmap.

---

## 8. Processes with crossing-angle HepMC3 data

The single table to pick datasets from. Every row has HepMC3 files with the
25 mrad crossing angle **measured** present on the beams, so each is ready for
`ddsim` with no `abconv` step. Head-on branches, non-HepMC formats and the one
unmeasured branch are deliberately absent — see sections 5.4 and 5.5 for those.

Energies in **bold** are the four where a complete background mixing recipe
also exists (section 5.1b), i.e. where a full signal+background dataset can be
built today. `format`: `root` = `.hepmc3.tree.root`, `ascii` = `.hepmc` /
`.hepmc3`, `ascii.gz` = gzipped. 167 branches, grouped into 47 rows.

### 8.1 Processes per beam energy

The same data rolled up by energy, ordered by how many processes each one
carries. This is the trade-off in one view: breadth of physics against whether
a background recipe exists.

> **`mixable`** means all five machine-background sources for that energy are
> present on disk, so we can add background ourselves there today — SynRad
> (status 2000), electron beam gas + brems (3000), Coulomb (4000), Touschek
> (5000) and proton beam gas (6000), as listed in the campaign's
> `config_data/…hgas_<E>_<pipe>….json`. It says nothing about the signal data;
> it is purely whether background can be mixed in. Full detail in section 5.1b.

| energy | processes with crossing-angle HepMC3 | mixable |
|---|---:|---|
| **10x100** | 27 | yes |
| **18x275** | 22 | yes |
| 5x41 | 18 | — |
| 9x275 | 15 | — |
| 9x130 | 12 | — |
| **10x130** | 10 | yes |
| 9x100 | 8 | — |
| 5x100 | 6 | — |
| 18x110 | 4 | — |
| **10x275** | 4 | yes |
| 18x108.41 | 2 | — |

**10x100 and 18x275 are the only energies that are both broad and mixable.**
10x275 is mixable but carries just 4 processes (the DIS and SIDIS lines), so its
value is as a *second occupancy point* — SynRad is 36.6 GHz there in vacuum
against 3.3 GHz at 18x275 — rather than as a second process set.

5x41 is third by breadth (18 processes) but its background recipe is blocked by
three missing files, and 9x275 / 9x130 are fourth and fifth with no rate table
at all. Both are worth asking for on the strength of the signal coverage already
sitting on disk.

### 8.2 Process catalogue, crossing-angle data only

| process | system | energies with crossing-angle HepMC3 | generator(s) | format | branches | files | size | Marco slug |
|---|---|---|---|---|---:|---:|---:|---|
| CC DIS, Q² threshold | ep | 5x41 5x100 **10x100** **10x275** **18x275** | Pythia8 (campaign) | ascii | 5 | 90 | 639.6 GiB | `ccdisq100/1000` |
| CC DIS, radiative, polarised | ep | 9x275 | DJANGOH 4.6.10 | root | 2 | 6 | 3.0 GiB | `ccdisq* (diff. generator)` |
| coherent J/ψ photoproduction | ep | **18x275** | eSTARlight | root | 1 | 2 | 679.2 MiB | `jpsiphoto` |
| coherent φ→K⁺K⁻, eA | eAu | 9x100 **10x100** 18x110 | Sartre | ascii, root | 4 | 14 | 61.1 GiB | `cohphi` |
| coherent/incoherent J/ψ, eA | eAu | 18x110 | Sartre | ascii | 2 | 8 | 32.4 GiB | `— (eA)` |
| coherent/incoherent ρ, eA | eAu | 9x100 **10x100** 18x110 | Sartre | ascii.gz, root | 4 | 2012 | 48.1 GiB | `cohrho` |
| DEMP π⁺ / K⁺Λ / K⁺Σ⁰ | ep | 5x41 5x100 9x130 9x275 **10x100** **10x130** **18x275** | DEMPgen | root | 13 | 840 | 375.1 GiB | `dempq3to10/10to20/20to35` |
| diffractive DIS | ep | 9x130 9x275 **10x100** | RAPGAP 3.310 | root | 5 | 5 | 14.2 GiB | `ddis` |
| diffractive J/ψ, ep | ep | 5x41 5x100 9x130 9x275 **10x100** **10x130** **18x275** | lAger | root | 7 | 7 | 437.7 MiB | `jpsi` |
| diffractive J/ψ, ePb | ePb | 18x108.41 | BeAGLE | ascii | 1 | 54 | 112.5 GiB | `— (ePb)` |
| diffractive φ, eA | eAu | 18x110 | eSTARlight | ascii | 1 | 1 | 54.0 MiB | `cohphi` |
| diffractive φ, ePb/eAu | eAu | 9x100 **10x100** | BeAGLE | root | 2 | 200 | 35.8 GiB | `cohphi` |
| diffractive φ, ePb/eAu | ePb | 18x108.41 | BeAGLE | ascii | 1 | 54 | 608.6 GiB | `cohphi` |
| double DVCS | ep | **10x130** **18x275** | EpIC | root | 2 | 6 | 2.3 GiB | `ddvcs` |
| DVCS | ep | 5x41 **10x100** **18x275** | DVCS gen (legacy) | ascii | 3 | 60 | 28.9 GiB | `dvcs` |
| DVCS + BH + INT | ep | 5x41 **10x100** **10x130** **18x275** | EpIC 1.1.6 | root | 6 | 10 | 3.5 GiB | `dvcs` |
| DVCS / BH / interference | ep | 9x130 9x275 | EpIC 1.1.8 | root | 6 | 24 | 11.3 GiB | `dvcs` |
| DVCS on deuteron | eD | 5x41 **10x100** | EpIC | ascii | 2 | 26 | 23.9 GiB | `— (eD)` |
| DVMP / Υ (lAger legacy) | ep | **10x100** | lAger | ascii | 1 | 8 | 1.7 GiB | `dvmp/upsilon` |
| DVMP J/ψ→μ⁺μ⁻ | ep | 9x130 9x275 **10x130** **18x275** | lAger | root | 4 | 4 | 3.2 GiB | `dvmp` |
| DVMP π⁰ | ep | 5x41 9x130 9x275 **10x100** **10x130** **18x275** | EpIC | root | 6 | 7 | 2.1 GiB | `dvmp` |
| exclusive ρ→π⁺π⁻ | ep | **10x100** | SLIGHT | ascii.gz | 1 | 52 | 719.0 MiB | `rho` |
| inclusive eA DIS | eAu | 5x41 9x100 **10x100** | BeAGLE | root | 5 | 815 | 94.3 GiB | `—` |
| inclusive eA DIS | eH2 | 9x130 **10x130** | BeAGLE | root | 5 | 221 | 73.3 GiB | `—` |
| inclusive eA DIS | eHe3 | 5x41 | BeAGLE | root | 1 | 3 | 3.2 GiB | `—` |
| meson structure function K⁺Λ | ep | 5x41 9x100 9x130 9x275 **10x100** **10x130** **18x275** | eicMesonSFGen | root | 7 | 3800 | 2.9 GiB | `mesonsf` |
| NC DIS, inclusive | ep | 5x41 5x100 9x130 9x275 **10x100** **10x130** **10x275** **18x275** | Pythia6.428, Pythia8.316 | root | 8 | 175 | 222.6 GiB | `ncdisq1/10/100/1000` |
| NC DIS, inclusive (EEEMCal cfg) | ep | 9x275 | Pythia8.315 | root | 1 | 100 | 1.8 GiB | `ncdisq*` |
| NC DIS, Q² threshold | ep | 5x41 5x100 **10x100** **10x275** **18x275** | Pythia8 (campaign) | ascii, root | 8 | 328 | 2.3 TiB | `ncdisq1/10/100/1000` |
| NC/CC DIS, radiative | ep | **18x275** | DJANGOH 4.6.21 | root | 2 | 8 | 6.5 GiB | `ncdisq*/ccdisq*` |
| SIDIS / min-bias photoprod. | en | 5x41 **10x100** **18x275** | Pythia6-eic | root | 3 | 715 | 576.5 GiB | `photoprod` |
| SIDIS / min-bias photoprod. | ep | 5x41 5x100 9x130 9x275 **10x100** **10x275** **18x275** | Pythia6-eic | root | 10 | 1141 | 1.1 TiB | `photoprod` |
| SIDIS D_s | ep | 9x275 | Pythia8 HFsim | root | 1 | 1200 | 3.1 GiB | `—` |
| SIDIS D_s (eA) | eAu | 9x100 | BeAGLE HFsim | root | 1 | 500 | 5.8 GiB | `—` |
| SIDIS dijet (PGF) | ep | **18x275** | Pythia6.428 dijet | root | 1 | 100 | 972.1 MiB | `—` |
| SIDIS open charm D⁰ | ep | 5x41 9x130 9x275 **10x100** **10x130** **18x275** | Pythia8, Pythia8 HFsim | root | 6 | 3728 | 22.7 GiB | `—` |
| SIDIS open charm D⁰ (eA) | eAu | 5x41 9x100 **10x100** | BeAGLE HFsim | root | 5 | 4900 | 15.1 GiB | `—` |
| SIDIS Λ | ep | **18x275** | Pythia8.306 | root | 1 | 8 | 10.5 GiB | `—` |
| SIDIS Λ_c | ep | 9x275 **10x100** | Pythia8 HFsim | root | 2 | 3500 | 3.7 GiB | `—` |
| SIDIS Λ_c (eA) | eAu | 9x100 **10x100** | BeAGLE HFsim | root | 3 | 1498 | 6.6 GiB | `—` |
| SIDIS, Q²-binned | ep | 5x41 **10x100** **18x275** | Pythia6 (IP6 era) | ascii, root | 5 | 5900 | 3.9 TiB | `photoprod (older prod.)` |
| spectroscopy ψ(2S)/X/Y | ep | **10x100** | dedicated | ascii | 1 | 24 | 2.2 GiB | `spectroscopy` |
| TCS + BH interference | ep | 5x41 **10x100** **18x275** | TCS gen | ascii | 3 | 800 | 59.6 GiB | `tcs` |
| u-channel π⁰ | ep | **18x275** | SLIGHT | root | 1 | 1 | 36.3 MiB | `upi0` |
| u-channel ρ | ep | **10x100** | SLIGHT/GENEX | root | 1 | 1 | 35.6 MiB | `urho` |
| Υ(1S/2S/3S) threshold | ep | 9x130 9x275 | eSTARlight 1.3.0 | root | 6 | 450 | 14.1 GiB | `upsilon` |
| ω photoproduction | ep | **18x275** | SLIGHT | ascii | 1 | 96 | 1.2 GiB | `omega` |

Rows are keyed on **(process, collision system)** — `ep`, `en`, `eD`, `eAu`,
`eH2`, `eHe3`, `ePb` are not interchangeable, and several processes exist in more
than one. Energies are the measured ones, so `SIDIS, Q²-binned` is listed at
18x275 for the branch whose directory is misnamed `ep_5x41` (section 5.5).

**Totals: 33,502 files, 10.3 TiB.**

Several processes exist in more than one collision system with different energy
coverage — `inclusive eA DIS` splits across eAu / eH2 / eHe3, `diffractive φ`
across eAu / ePb, and `SIDIS min-bias photoproduction` has an `en`
(electron–neutron) variant alongside `ep`. Those are not interchangeable, so
they stay as separate rows rather than being merged into one process line.
### 8.3 Coverage including degraded sources

Same rows as 8.2, but no longer restricted to ready-to-use data. Each energy
carries a marker for the **best source available at that energy**:

| marker | meaning | what it costs to use |
|---|---|---|
| *(none)* | crossing-angle HepMC3 on `/volatile` | nothing — feed to `ddsim` |
| `(R)` | only in `RECO`, as `MCParticles` | needs `edm2hepmc`; crossing angle already applied |
| `(h)` | only head-on HepMC3 | needs `abconv` run first |
| `(L)` | only in LUND / eic-smear / other non-HepMC form | needs a format conversion |
| `(?)` | present but beams not determined | needs inspection |

A marker describes the *best* option **for that branch family**, so a plain
energy may also have head-on or RECO copies. Note that a few `(h)` rows do have
an afterburned counterpart, but under a differently-named row because the
productions are distinct — `coherent ρ, eA` (head-on, `DIFFRACTIVE_RHO/Sartre`)
versus `coherent/incoherent ρ, eA` (afterburned,
`DIFFRACTIVE_RHO_ABCONV/Sartre/{Coherent,Incoherent}`). Section 5.5 pairs them
explicitly. Energies in **bold** have a complete background recipe.

This table has **57 rows against 8.2's 47**: the ten extra are processes that
exist only head-on, only in a non-HepMC format, or only in `RECO`.

| process | system | energies, by best available source | generator(s) | branches | files | size | Marco slug |
|---|---|---|---|---:|---:|---:|---|
| CC DIS, Q² threshold | ep | 5x41 5x100 **10x100** **10x275** **18x275** | Pythia8 (campaign) | 5 | 90 | 639.6 GiB | `ccdisq100/1000` |
| CC DIS, radiative (eRHIC fmt) | eD | 18x137 (h) | DJANGOH/eRHIC | 1 | 42 | 92.2 GiB | `ccdisq*` |
| CC DIS, radiative (eRHIC fmt) | ep | **18x275** (h) | DJANGOH/eRHIC | 2 | 36 | 102.4 GiB | `ccdisq*` |
| CC DIS, radiative, polarised | ep | 9x275 | DJANGOH 4.6.10 | 2 | 6 | 3.0 GiB | `ccdisq* (diff. generator)` |
| coherent J/ψ photoproduction | ep | **18x275** | eSTARlight | 1 | 2 | 679.2 MiB | `jpsiphoto` |
| coherent ρ, eA | eAu | 18x110 (h) | Sartre | 1 | 2 | 23.7 GiB | `cohrho` |
| coherent φ→K⁺K⁻, eA | eAu | 9x100 **10x100** 18x110 | Sartre | 4 | 14 | 61.1 GiB | `cohphi` |
| coherent/incoherent J/ψ, eA | eAu | 18x110 | Sartre | 2 | 8 | 32.4 GiB | `— (eA)` |
| coherent/incoherent ρ, eA | eAu | 9x100 **10x100** 18x110 | Sartre | 4 | 2012 | 48.1 GiB | `cohrho` |
| DEMP K⁺Λ / K⁺Σ (LUND fmt) | ep | 5x41 (L) **10x100** (L) | DEMPgen (legacy) | 5 | 46 | 11.1 GiB | `dempq*` |
| DEMP π⁺ / K⁺Λ / K⁺Σ⁰ | ep | 5x41 5x100 9x130 9x275 **10x100** **10x130** **18x275** | DEMPgen | 13 | 840 | 375.1 GiB | `dempq3to10/10to20/20to35` |
| diffractive DIS | ep | 9x130 9x275 **10x100** | RAPGAP 3.310 | 5 | 5 | 14.2 GiB | `ddis` |
| diffractive J/ψ, eA | eAu | 18x110 (h) | Sartre | 1 | 2 | 23.6 GiB | `— (eA)` |
| diffractive J/ψ, ep | ep | 5x41 5x100 9x130 9x275 **10x100** **10x130** **18x275** | lAger | 7 | 7 | 437.7 MiB | `jpsi` |
| diffractive J/ψ, ePb | ePb | 18x108.41 | BeAGLE | 1 | 54 | 112.5 GiB | `— (ePb)` |
| diffractive φ, eA | eA | 18x110 (h) | Sartre/BeAGLE | 1 | 200 | 72.0 GiB | `cohphi` |
| diffractive φ, eA | eAu | 18x110 | Sartre/BeAGLE, eSTARlight | 2 | 3 | 23.7 GiB | `cohphi` |
| diffractive φ, ePb/eAu | eAu | 9x100 **10x100** | BeAGLE | 2 | 200 | 35.8 GiB | `cohphi` |
| diffractive φ, ePb/eAu | ePb | 18x108.41 | BeAGLE | 1 | 54 | 608.6 GiB | `cohphi` |
| double DVCS | ep | **10x130** **18x275** | EpIC | 2 | 6 | 2.3 GiB | `ddvcs` |
| DVCS | ep | 5x41 **10x100** **18x275** | DVCS gen (legacy) | 6 | 65 | 32.9 GiB | `dvcs` |
| DVCS + BH + INT | ep | 5x41 **10x100** **10x130** **18x275** | EpIC 1.1.6 | 6 | 10 | 3.5 GiB | `dvcs` |
| DVCS + BH + INT, coherent | ep | **18x275** (L) | EpIC | 1 | 1 | 823.3 MiB | `dvcs` |
| DVCS / BH / interference | ep | 9x130 9x275 | EpIC 1.1.8 | 6 | 24 | 11.3 GiB | `dvcs` |
| DVCS on deuteron | eD | 5x41 **10x100** | EpIC | 2 | 26 | 23.9 GiB | `— (eD)` |
| DVMP / Υ (lAger legacy) | ep | **10x100** | lAger | 1 | 8 | 1.7 GiB | `dvmp/upsilon` |
| DVMP J/ψ→μ⁺μ⁻ | ep | 9x130 9x275 **10x130** **18x275** | lAger | 4 | 4 | 3.2 GiB | `dvmp` |
| DVMP π⁰ | ep | 5x41 9x130 9x275 **10x100** **10x130** **18x275** | EpIC | 7 | 8 | 2.2 GiB | `dvmp` |
| exclusive ρ→π⁺π⁻ | ep | **10x100** **18x275** (h) | SLIGHT | 3 | 56 | 1.5 GiB | `rho` |
| inclusive eA DIS | eAu | 5x41 9x100 **10x100** | BeAGLE | 5 | 815 | 94.3 GiB | `—` |
| inclusive eA DIS | eH2 | 9x130 **10x130** | BeAGLE | 5 | 221 | 73.3 GiB | `—` |
| inclusive eA DIS | eHe3 | 5x41 18x110 (R) | BeAGLE | 1 | 3 | 3.2 GiB | `—` |
| meson structure function K⁺Λ | ep | 5x41 9x100 9x130 9x275 **10x100** **10x130** **18x275** | eicMesonSFGen | 7 | 3800 | 2.9 GiB | `mesonsf` |
| NC DIS, inclusive | ep | 5x41 5x100 9x130 9x275 **10x100** **10x130** **10x275** **18x275** | Pythia6.428, Pythia8.316 | 8 | 175 | 222.6 GiB | `ncdisq1/10/100/1000` |
| NC DIS, inclusive (EEEMCal cfg) | ep | 9x275 | Pythia8.315 | 1 | 100 | 1.8 GiB | `ncdisq*` |
| NC DIS, Q² threshold | ep | 5x41 5x100 **10x100** **10x275** **18x275** | Pythia8 (campaign) | 8 | 328 | 2.3 TiB | `ncdisq1/10/100/1000` |
| NC/CC DIS, radiative | ep | **18x275** | DJANGOH 4.6.21 | 2 | 8 | 6.5 GiB | `ncdisq*/ccdisq*` |
| SIDIS / min-bias photoprod. | en | 5x41 **10x100** **18x275** | Pythia6-eic | 3 | 715 | 576.5 GiB | `photoprod` |
| SIDIS / min-bias photoprod. | ep | 5x41 5x100 9x130 9x275 **10x100** **10x275** **18x275** | Pythia6-eic | 10 | 1141 | 1.1 TiB | `photoprod` |
| SIDIS D_s | ep | 9x275 | Pythia8 HFsim | 1 | 1200 | 3.1 GiB | `—` |
| SIDIS D_s (eA) | eAu | 9x100 | BeAGLE HFsim | 1 | 500 | 5.8 GiB | `—` |
| SIDIS dijet (PGF) | ep | **18x275** | Pythia6.428 dijet | 1 | 100 | 972.1 MiB | `—` |
| SIDIS open charm D⁰ | ep | 5x41 9x130 9x275 **10x100** **10x130** **18x275** | Pythia8, Pythia8 HFsim | 6 | 3728 | 22.7 GiB | `—` |
| SIDIS open charm D⁰ (eA) | eAu | 5x41 9x100 **10x100** | BeAGLE HFsim | 5 | 4900 | 15.1 GiB | `—` |
| SIDIS Λ | ep | **18x275** | Pythia8.306 | 1 | 8 | 10.5 GiB | `—` |
| SIDIS Λ_c | ep | 9x275 **10x100** | Pythia8 HFsim | 2 | 3500 | 3.7 GiB | `—` |
| SIDIS Λ_c (eA) | eAu | 9x100 **10x100** | BeAGLE HFsim | 3 | 1498 | 6.6 GiB | `—` |
| SIDIS, Q²-binned | ep | 5x41 **10x100** 18x100 (L) **18x275** | Pythia6 (IP6 era) | 8 | 7320 | 4.0 TiB | `photoprod (older prod.)` |
| spectroscopy ψ(2S)/X/Y | ep | **10x100** | dedicated | 2 | 30 | 2.6 GiB | `spectroscopy` |
| TCS + BH interference | ep | 5x41 **10x100** **18x275** | TCS gen | 6 | 860 | 121.9 GiB | `tcs` |
| TCS, pure | ep | 5x41 (h) 5x100 (h) **10x100** (h) **18x275** (h) | TCS gen | 4 | 80 | 83.1 GiB | `tcs` |
| u-channel π⁰ | ep | **18x275** | SLIGHT | 1 | 1 | 36.3 MiB | `upi0` |
| u-channel ρ | ep | **10x100** | SLIGHT/GENEX | 1 | 1 | 35.6 MiB | `urho` |
| u-channel ω (neutral decay) | ep | **18x275** (h) | SLIGHT | 1 | 10 | 250.6 MiB | `— (not upi0/omega)` |
| Υ photoproduction (legacy) | ep | ? (h) | eSTARlight | 1 | 3 | 9.5 MiB | `upsilon` |
| Υ(1S/2S/3S) threshold | ep | 9x130 9x275 | eSTARlight 1.3.0 | 6 | 450 | 14.1 GiB | `upsilon` |
| ω photoproduction | ep | **18x275** | SLIGHT | 2 | 98 | 1.4 GiB | `omega` |

Cells by source: 128 ready, 1 RECO-only, 12 head-on-only, 4 needing format conversion, 0 undetermined.

**What the `RECO` route adds.** Exactly one (process, system, energy)
combination exists in a background-free `RECO` campaign with no crossing-angle
HepMC3 on `/volatile` — so `RECO`'s value is **durability and the 9x points**,
not extra process coverage:

| process | system | energy | RECO campaign(s) |
|---|---|---|---|
| inclusive eA DIS | eHe3 | 18x110 | 26.02.0, 26.03.1, 26.04.1, 26.07.1 |

### 8.4 Processes per beam energy, all sources

Section 8.1 counted only ready-to-use data. This counts a process at an energy
if it is reachable **at all** — ready, via `RECO`, via `abconv`, or via a format
conversion. Ordered by total, as in 8.1.

> **Legend:**
>
> **`mixable`** — all five machine-background sources for that energy are on
> disk, so we can add background ourselves there today: SynRad (status 2000),
> electron beam gas + brems (3000), Coulomb (4000), Touschek (5000), proton beam
> gas (6000). Only 10x100, 10x130, 10x275 and 18x275 qualify; 5x41 and 5x100 are
> short three files and the 9x points have no rate config at all (section 5.1b).
> This is about background only — it says nothing about the signal data.
>
> The other columns say what form the **signal** data takes, i.e. what it costs
> to use:
>
> | column | the data is | work needed |
> |---|---|---|
> | `ready` | crossing-angle HepMC3 on `/volatile` | none — feed straight to `ddsim` |
> | `(R)` | only in `RECO`, as `MCParticles` | needs the `edm2hepmc` tool; the crossing angle is already applied (section 5.6) |
> | `(h)` | only head-on HepMC3 | needs `abconv` first — head-on beams cannot go into `ddsim` (section 4) |
> | `(L)` | only in LUND or eic-smear format | needs a format conversion (section 5.5) |
>
> A process is counted once per energy, under its best available source.

| energy | processes, any source | ready | `(R)` RECO only | `(h)` head-on only | `(L)` convert | mixable |
|---|---:|---:|---:|---:|---:|---|
| **10x100** | 29 | 27 | — | 1 | 1 | yes |
| **18x275** | 27 | 22 | — | 4 | 1 | yes |
| 5x41 | 20 | 18 | — | 1 | 1 | — |
| 9x275 | 15 | 15 | — | — | — | — |
| 9x130 | 12 | 12 | — | — | — | — |
| **10x130** | 10 | 10 | — | — | — | yes |
| 9x100 | 8 | 8 | — | — | — | — |
| 18x110 | 8 | 4 | 1 | 3 | — | — |
| 5x100 | 7 | 6 | — | 1 | — | — |
| **10x275** | 4 | 4 | — | — | — | yes |
| 18x108.41 | 2 | 2 | — | — | — | — |
| 18x100 | 1 | — | — | — | 1 | — |
| 18x137 | 1 | — | — | 1 | — | — |
| ? | 1 | — | — | 1 | — | — |
| **total cells** | **145** | **128** | **1** | **12** | **4** | |

`?` is `EXCLUSIVE/UPSILON/v1` — a legacy Υ photoproduction sample whose only
recorded beam is a ~0.4 GeV virtual photon, so no configuration can be read off
it. `18x137` is eD (`erhic-cc-yrad-floff_eD_18_137_*`), `18x100` is the
eic-smear-format `SIDIS/pythia6/ep_18x100` set, and `18x108.41` is the BeAGLE
ePb production.

Against 8.1 the ordering barely moves: **10x100** and **18x275** stay first and
second and stay the only broad-and-mixable pair. What the extra sources buy is
small and concentrated — 18x110 nearly doubles (4 → 8) because the Sartre eA
head-on samples and the eHe3 RECO branch live there, and 18x275 gains 5 (pure
TCS, u-channel ω, eRHIC-format CC DIS, the coherent DVCS+BH+INT file). Neither
changes which energy to start at.

