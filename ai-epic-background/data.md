# Data

Available **background-mixed** datasets in Rucio. Source of truth:

```bash
rucio did list --filter 'is_background_mixed=true' 'epic:*'
```

The campaign strips below are authored by hand with the `<DidStrips>`
component — see `.vitepress/theme/components/DidStrips.vue`. To refresh them
after a new Rucio campaign, run the `update-data-md` skill: it queries Rucio,
digests the DIDs with `scripts/summarize_rucio_dids.py`, and guides authoring
the strips (labels, colours, and tooltips are set by hand).

_Last updated: **2026-09-29**_

## Conventions

- **FULL** — DD4hep simulation output (sim-level, full Geant4 hits).
- **RECO** — EICrecon reconstruction output (reco-level).
- Each strip covers one `(campaign, data_name)` pair. Click a strip to reveal
  the exact Rucio DIDs with copy buttons; hover any tag for a description.
- `main/` branch / CI / Test entries are filtered out — only versioned
  campaigns are shown.
- `epic_craterlake` is the only detector configuration.
- Use the per-row 📋 to copy a single DID, the **Copy all** button to copy
  every DID in a strip (newline-separated), or click the prefix line to copy
  the shared DID prefix.

<!-- BEGIN STRIPS -->


## Campaign 26.07.1

<DidStrips
  didpath="epic:/{FULL|RECO}/26.07.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/"
  version="26.07.1"
  name="Bkg_Exact1S_2us"
>
  <Tags color="violet" desc="Physics process">
    <Tag desc="Deep Inelastic Scattering (pythia8), neutral current">DIS</Tag>
    <Tag desc="Neutral-current exchange">NC</Tag>
    <Tag desc="Semi-Inclusive DIS (pythia6-eic 1.0.0)">SIDIS</Tag>
  </Tags>
  <Tags color="sky" desc="Beam energy">
    <Tag desc="Beam energy 10x100 GeV (e 10 x p 100) — both DIS/NC and SIDIS">10x100</Tag>
    <Tag desc="Beam energy 10x275 GeV (e 10 x p 275) — both DIS/NC and SIDIS">10x275</Tag>
  </Tags>
  <Tags color="amber" desc="Momentum transfer">
    <Tag desc="DIS/NC: minimum Q2 >= 1 GeV2">minQ2=1</Tag>
    <Tag desc="DIS/NC: minimum Q2 >= 10 GeV2">minQ2=10</Tag>
    <Tag desc="DIS/NC: minimum Q2 >= 100 GeV2">minQ2=100</Tag>
    <Tag desc="DIS/NC: minimum Q2 >= 1000 GeV2">minQ2=1000</Tag>
    <Tag desc="SIDIS branch only: Q2 range 0-1 GeV2">q2_0to1</Tag>
  </Tags>
  <More color="slate">
    <Tag desc="Detector: ePIC craterlake">epic_craterlake</Tag>
    <Tag desc="Beam-pipe gold coating">GoldCt</Tag>
    <Tag desc="Coating thickness 10 um">10um</Tag>
    <Tag desc="Generator for the SIDIS branch: pythia6-eic v1.0.0">pythia6-eic/1.0.0</Tag>
  </More>
  <Dids>
epic:/FULL/26.07.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=1
epic:/RECO/26.07.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=1
epic:/FULL/26.07.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=10
epic:/RECO/26.07.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=10
epic:/FULL/26.07.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=100
epic:/RECO/26.07.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=100
epic:/FULL/26.07.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=1000
epic:/RECO/26.07.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=1000
epic:/FULL/26.07.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=1
epic:/RECO/26.07.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=1
epic:/FULL/26.07.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=10
epic:/RECO/26.07.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=10
epic:/FULL/26.07.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=100
epic:/RECO/26.07.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=100
epic:/FULL/26.07.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=1000
epic:/RECO/26.07.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=1000
epic:/FULL/26.07.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/SIDIS/pythia6-eic/1.0.0/10x100/q2_0to1
epic:/RECO/26.07.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/SIDIS/pythia6-eic/1.0.0/10x100/q2_0to1
epic:/FULL/26.07.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/SIDIS/pythia6-eic/1.0.0/10x275/q2_0to1
epic:/RECO/26.07.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/SIDIS/pythia6-eic/1.0.0/10x275/q2_0to1
  </Dids>
</DidStrips>

Adds a **SIDIS** branch (pythia6-eic 1.0.0, `q2_0to1`) alongside the DIS/NC
grid, and every dataset now has both a **FULL** (sim) and a **RECO** partition.


## Campaign 26.07.0

<DidStrips
  didpath="epic:/{FULL|RECO}/26.07.0/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/"
  version="26.07.0"
  name="Bkg_Exact1S_2us"
>
  <Tags color="violet" desc="Physics process">
    <Tag desc="Deep Inelastic Scattering">DIS</Tag>
    <Tag desc="Neutral-current exchange">NC</Tag>
  </Tags>
  <Tags color="sky" desc="Beam energy">
    <Tag desc="Beam energy 10x100 GeV (e 10 x p 100)">10x100</Tag>
    <Tag desc="Beam energy 10x275 GeV (e 10 x p 275)">10x275</Tag>
  </Tags>
  <Tags color="amber" desc="Minimum momentum transfer">
    <Tag desc="Minimum Q2 >= 1 GeV2">minQ2=1</Tag>
    <Tag desc="Minimum Q2 >= 10 GeV2">minQ2=10</Tag>
    <Tag desc="Minimum Q2 >= 100 GeV2">minQ2=100</Tag>
    <Tag desc="Minimum Q2 >= 1000 GeV2">minQ2=1000</Tag>
  </Tags>
  <More color="slate">
    <Tag desc="Detector: ePIC craterlake">epic_craterlake</Tag>
    <Tag desc="Beam-pipe gold coating">GoldCt</Tag>
    <Tag desc="Coating thickness 10 um">10um</Tag>
  </More>
  <Dids>
epic:/FULL/26.07.0/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=1
epic:/RECO/26.07.0/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=1
epic:/FULL/26.07.0/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=10
epic:/RECO/26.07.0/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=10
epic:/FULL/26.07.0/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=100
epic:/RECO/26.07.0/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=100
epic:/FULL/26.07.0/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=1000
epic:/RECO/26.07.0/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=1000
epic:/FULL/26.07.0/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=1
epic:/RECO/26.07.0/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=1
epic:/FULL/26.07.0/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=10
epic:/RECO/26.07.0/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=10
epic:/FULL/26.07.0/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=100
epic:/RECO/26.07.0/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=100
epic:/FULL/26.07.0/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=1000
epic:/RECO/26.07.0/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=1000
  </Dids>
</DidStrips>


## Campaign 2026-06

**Meson-structure k-Λ background**

<DidStrips
  didpath="/work/eic3/users/romanov/meson-structure-2026-06/reco-background/"
  version="2026-06"
  name="reco-background"
>
  <Tags color="violet" desc="Signal physics process">
    <Tag desc="Meson structure function, exclusive K⁺Λ (eic_mesonsf_generator)">k-Λ</Tag>
  </Tags>
  <Tags color="sky" desc="Beam energy (e × p, GeV)">
    <Tag desc="e 10 × p 100 GeV — 68 files × 5000 evt">10x100</Tag>
    <Tag desc="e 10 × p 130 GeV — 43 files × 5000 evt">10x130</Tag>
    <Tag desc="e 18 × p 275 GeV — 107 files × 5000 evt">18x275</Tag>
  </Tags>
  <Tags color="orange" desc="Background">
    <Tag desc="Background mixed in (has_background=true) with beam effects / afterburner applied">background + beam-effects</Tag>
  </Tags>
  <More color="slate">
    <Tag desc="Detector: ePIC craterlake">epic_craterlake</Tag>
    <Tag desc="Reconstructed (EICrecon) edm4eic output">RECO</Tag>
    <Tag desc="Generator: eic_mesonsf_generator">eic_mesonsf_generator</Tag>
    <Tag desc="Software release: eicdev-eic-full-2026-06-01.sif">eicdev 2026-06-01</Tag>
    <Tag desc="5000 events per file">5000 evt/file</Tag>
  </More>
  <Dids>
/work/eic3/users/romanov/meson-structure-2026-06/reco-background/10x100
/work/eic3/users/romanov/meson-structure-2026-06/reco-background/10x130
/work/eic3/users/romanov/meson-structure-2026-06/reco-background/18x275
  </Dids>
</DidStrips>

k-Λ signal reconstructed with background + beam effects — not on Rucio, on the
JLab work disk (XRootD via `root://dtn-eic.jlab.org`). One leaf per beam energy
of `k_lambda_<beam>_5000evt_*.edm4eic.root`; file counts are in the beam-energy
tooltips above.


## Campaign 26.05.0

<DidStrips
  didpath="epic:/RECO/26.05.0/epic_craterlake/Bkg_Exact1S_2us_e_only/GoldCt/10um/EW_BSM/ALP/madgraph5-3.7.0-1.0/"
  csvpath="root://sci-xrootd.jlab.org//work/eic/users/romanov/epic-background-2026-05/csv_eicrecon/"
  version="26.05.0"
  name="Bkg_Exact1S_2us_e_only"
>
  <Tags color="violet" desc="Physics process">
    <Tag desc="Electroweak / Beyond-Standard-Model">EW_BSM</Tag>
    <Tag desc="Axion-like particle signal">ALP</Tag>
  </Tags>
  <Tags color="fuchsia" desc="Final state / decay channel">
    <Tag desc="Final state a -> e, mu+ mu-">aem-ax-emmupmum</Tag>
    <Tag desc="Final state a -> e e">aem-axem</Tag>
  </Tags>
  <Tags color="sky" desc="Beam energy">
    <Tag desc="Beam energy 10x110 GeV (e 10 x p 110)">10x110</Tag>
  </Tags>
  <Tags color="rose" desc="ALP signal mass">
    <Tag desc="ALP mass = 0.1 GeV">ma_0.1</Tag>
    <Tag desc="ALP mass = 0.2 GeV">ma_0.2</Tag>
    <Tag desc="ALP mass = 0.5 GeV">ma_0.5</Tag>
    <Tag desc="ALP mass = 1.0 GeV">ma_1.0</Tag>
    <Tag desc="ALP mass = 2.0 GeV">ma_2.0</Tag>
    <Tag desc="ALP mass = 5.0 GeV">ma_5.0</Tag>
    <Tag desc="ALP mass = 10.0 GeV">ma_10.0</Tag>
    <Tag desc="ALP mass = 20.0 GeV">ma_20.0</Tag>
  </Tags>
  <More color="slate">
    <Tag desc="Detector: ePIC craterlake">epic_craterlake</Tag>
    <Tag desc="Generator: MadGraph5 v3.7.0">madgraph5-3.7.0-1.0</Tag>
    <Tag desc="Beam-pipe gold coating">GoldCt</Tag>
    <Tag desc="Coating thickness 10 um">10um</Tag>
  </More>
  <Dids>
epic:/RECO/26.05.0/epic_craterlake/Bkg_Exact1S_2us_e_only/GoldCt/10um/EW_BSM/ALP/madgraph5-3.7.0-1.0/aem-ax-emmupmum/10x110/ma_0.1
epic:/RECO/26.05.0/epic_craterlake/Bkg_Exact1S_2us_e_only/GoldCt/10um/EW_BSM/ALP/madgraph5-3.7.0-1.0/aem-ax-emmupmum/10x110/ma_0.2
epic:/RECO/26.05.0/epic_craterlake/Bkg_Exact1S_2us_e_only/GoldCt/10um/EW_BSM/ALP/madgraph5-3.7.0-1.0/aem-ax-emmupmum/10x110/ma_0.5
epic:/RECO/26.05.0/epic_craterlake/Bkg_Exact1S_2us_e_only/GoldCt/10um/EW_BSM/ALP/madgraph5-3.7.0-1.0/aem-ax-emmupmum/10x110/ma_1.0
epic:/RECO/26.05.0/epic_craterlake/Bkg_Exact1S_2us_e_only/GoldCt/10um/EW_BSM/ALP/madgraph5-3.7.0-1.0/aem-ax-emmupmum/10x110/ma_2.0
epic:/RECO/26.05.0/epic_craterlake/Bkg_Exact1S_2us_e_only/GoldCt/10um/EW_BSM/ALP/madgraph5-3.7.0-1.0/aem-ax-emmupmum/10x110/ma_5.0
epic:/RECO/26.05.0/epic_craterlake/Bkg_Exact1S_2us_e_only/GoldCt/10um/EW_BSM/ALP/madgraph5-3.7.0-1.0/aem-ax-emmupmum/10x110/ma_10.0
epic:/RECO/26.05.0/epic_craterlake/Bkg_Exact1S_2us_e_only/GoldCt/10um/EW_BSM/ALP/madgraph5-3.7.0-1.0/aem-ax-emmupmum/10x110/ma_20.0
epic:/RECO/26.05.0/epic_craterlake/Bkg_Exact1S_2us_e_only/GoldCt/10um/EW_BSM/ALP/madgraph5-3.7.0-1.0/aem-axem/10x110/ma_0.1
epic:/RECO/26.05.0/epic_craterlake/Bkg_Exact1S_2us_e_only/GoldCt/10um/EW_BSM/ALP/madgraph5-3.7.0-1.0/aem-axem/10x110/ma_0.2
epic:/RECO/26.05.0/epic_craterlake/Bkg_Exact1S_2us_e_only/GoldCt/10um/EW_BSM/ALP/madgraph5-3.7.0-1.0/aem-axem/10x110/ma_0.5
epic:/RECO/26.05.0/epic_craterlake/Bkg_Exact1S_2us_e_only/GoldCt/10um/EW_BSM/ALP/madgraph5-3.7.0-1.0/aem-axem/10x110/ma_1.0
epic:/RECO/26.05.0/epic_craterlake/Bkg_Exact1S_2us_e_only/GoldCt/10um/EW_BSM/ALP/madgraph5-3.7.0-1.0/aem-axem/10x110/ma_2.0
epic:/RECO/26.05.0/epic_craterlake/Bkg_Exact1S_2us_e_only/GoldCt/10um/EW_BSM/ALP/madgraph5-3.7.0-1.0/aem-axem/10x110/ma_5.0
epic:/RECO/26.05.0/epic_craterlake/Bkg_Exact1S_2us_e_only/GoldCt/10um/EW_BSM/ALP/madgraph5-3.7.0-1.0/aem-axem/10x110/ma_10.0
epic:/RECO/26.05.0/epic_craterlake/Bkg_Exact1S_2us_e_only/GoldCt/10um/EW_BSM/ALP/madgraph5-3.7.0-1.0/aem-axem/10x110/ma_20.0
  </Dids>
</DidStrips>


## Campaign 26.04.1

<DidStrips
  didpath="epic:/{FULL|RECO}/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/"
  version="26.04.1"
  name="Bkg_Exact1S_2us"
>
  <Tags color="violet" desc="Physics process">
    <Tag desc="Deep Inelastic Scattering">DIS</Tag>
    <Tag desc="Neutral-current exchange">NC</Tag>
  </Tags>
  <Tags color="sky" desc="Beam energy">
    <Tag desc="Beam energy 10x100 GeV (e 10 x p 100)">10x100</Tag>
    <Tag desc="Beam energy 10x275 GeV (e 10 x p 275)">10x275</Tag>
  </Tags>
  <Tags color="amber" desc="Minimum momentum transfer">
    <Tag desc="Minimum Q2 >= 1 GeV2">minQ2=1</Tag>
    <Tag desc="Minimum Q2 >= 10 GeV2">minQ2=10</Tag>
    <Tag desc="Minimum Q2 >= 100 GeV2">minQ2=100</Tag>
    <Tag desc="Minimum Q2 >= 1000 GeV2">minQ2=1000</Tag>
  </Tags>
  <More color="slate">
    <Tag desc="Detector: ePIC craterlake">epic_craterlake</Tag>
    <Tag desc="Beam-pipe gold coating">GoldCt</Tag>
    <Tag desc="Coating thickness 10 um">10um</Tag>
  </More>
  <Dids>
epic:/FULL/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=1
epic:/RECO/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=1
epic:/FULL/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=10
epic:/RECO/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=10
epic:/FULL/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=100
epic:/RECO/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=100
epic:/FULL/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=1000
epic:/RECO/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=1000
epic:/FULL/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=1
epic:/RECO/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=1
epic:/FULL/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=10
epic:/RECO/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=10
epic:/FULL/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=100
epic:/RECO/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=100
epic:/FULL/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=1000
epic:/RECO/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=1000
  </Dids>
</DidStrips>


## Campaign 26.03.0

<DidStrips
  didpath="epic:/RECO/26.03.0/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/"
  version="26.03.0"
  name="Bkg_Exact1S_2us"
>
  <Tags color="violet" desc="Physics process">
    <Tag desc="Deep Inelastic Scattering">DIS</Tag>
    <Tag desc="Neutral-current exchange">NC</Tag>
    <Tag desc="Semi-Inclusive DIS">SIDIS</Tag>
    <Tag desc="D0 (afterburner conversion)">D0_ABCONV</Tag>
  </Tags>
  <Tags color="sky" desc="Beam energy">
    <Tag desc="Beam energy 10x100 GeV">10x100</Tag>
    <Tag desc="Beam energy 10x275 GeV">10x275</Tag>
  </Tags>
  <Tags color="amber" desc="Momentum transfer">
    <Tag desc="Minimum Q2 >= 1 GeV2">minQ2=1</Tag>
    <Tag desc="Q2 = 100 GeV2">q2_100</Tag>
  </Tags>
  <More color="slate">
    <Tag desc="Detector: ePIC craterlake">epic_craterlake</Tag>
    <Tag desc="Generator: PYTHIA 8.306">pythia8.306-1.1</Tag>
    <Tag desc="High beam divergence">hiDiv</Tag>
  </More>
  <Dids>
epic:/RECO/26.03.0/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=1
epic:/RECO/26.03.0/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/SIDIS/D0_ABCONV/pythia8.306-1.1/10x100/q2_100/hiDiv
epic:/RECO/26.03.0/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x275/minQ2=1
  </Dids>
</DidStrips>

<!-- END STRIPS -->


## Campaign 25.10

Not available on Rucio, but can be downloaded from JLab xrootd
(`root://dtn-eic.jlab.org//volatile/eic/...`). These strips list the
**directory paths** under each background configuration rather than leaf DIDs.

<DidStrips
  didpath="/volatile/eic/EPIC/RECO/25.10.0/epic_craterlake/Bkg_1SignalPer2usFrame/"
  csvpath="root://sci-xrootd.jlab.org//work/eic/users/romanov/epic-background-2025-10/csv_reco/"
  version="25.10.0"
  name="Bkg_1SignalPer2usFrame"
>
  <Tags color="orange" desc="Background type">
    <Tag desc="Synchrotron radiation background (10 GeV, vacuum)">Synrad</Tag>
  </Tags>
  <More color="slate">
    <Tag desc="Detector: ePIC craterlake">epic_craterlake</Tag>
  </More>
  <Dids>
/volatile/eic/EPIC/RECO/25.10.0/epic_craterlake/Bkg_1SignalPer2usFrame/Synrad_10GeV_Vac_10000Ahr_Runtime_50s_Egas_10GeV_Hgas_275GeV
  </Dids>
</DidStrips>

<DidStrips
  didpath="/volatile/eic/EPIC/RECO/25.10.4/epic_craterlake/Bkg_1SignalPer2usFrame/"
  csvpath="root://sci-xrootd.jlab.org//work/eic/users/romanov/epic-background-2025-10/csv_reco/"
  version="25.10.4"
  name="Bkg_1SignalPer2usFrame"
>
  <Tags color="violet" desc="Signal physics process">
    <Tag desc="Deep Inelastic Scattering, neutral current (pythia8), 10x100 & 10x275">DIS/NC</Tag>
    <Tag desc="Double DVCS, afterburner + γ→ee conversion (EpIC 1.1.6-1.0), 18x275">DDVCS_ABCONV</Tag>
    <Tag desc="Deeply Virtual Meson Production, π⁰ (EpIC 1.1.6-1.1), 18x275">DVMP</Tag>
    <Tag desc="Semi-Inclusive DIS (pythia6-eic), 18x275 — only 1 reco file present so far">SIDIS</Tag>
    <Tag desc="DVCS, afterburner + conversion (18x275) — exists only inside the Synrad subtree">DVCS_ABCONV</Tag>
  </Tags>
  <Tags color="sky" desc="Beam energy (e × p, GeV)">
    <Tag desc="e 10 × p 100 GeV (DIS/NC)">10x100</Tag>
    <Tag desc="e 10 × p 275 GeV (DIS/NC)">10x275</Tag>
    <Tag desc="e 18 × p 275 GeV (DDVCS, DVMP, SIDIS, Synrad)">18x275</Tag>
  </Tags>
  <Tags color="orange" desc="Background mixed into each 2 µs frame">
    <Tag desc="Full cocktail: synrad + ebrems + ecoulomb + etouschek + p-beam-gas (all top-level channels)">cocktail</Tag>
    <Tag desc="Synchrotron radiation only — 18 GeV, vacuum, 10000 Ah·r (the Synrad_18GeV_… subtree)">synrad-only</Tag>
  </Tags>
  <Tags color="amber" desc="Q² range (GeV²)">
    <Tag desc="minQ2 = 1 (DIS/NC)">gt-1</Tag>
    <Tag desc="0–10 (DDVCS)">0to10</Tag>
    <Tag desc="1–1000 (DVMP)">1to1000</Tag>
    <Tag desc="~0–1 (SIDIS)">0to1</Tag>
  </Tags>
  <More color="slate">
    <Tag desc="Detector: ePIC craterlake">epic_craterlake</Tag>
    <Tag desc="Signal-mixing scheme: exactly 1 signal event per 2 µs timeframe">1 signal / 2 µs</Tag>
    <Tag desc="Generator: pythia8 (DIS/NC)">pythia8</Tag>
    <Tag desc="Generator: EpIC 1.1.6 (DDVCS, DVMP)">EpIC1.1.6</Tag>
    <Tag desc="Generator: pythia6-eic 1.0.0 (SIDIS)">pythia6-eic</Tag>
    <Tag desc="DDVCS electron-decay channel, negative/positive scattered hadron">edecay hminus/hplus</Tag>
  </More>
  <Dids>
/volatile/eic/EPIC/RECO/25.10.4/epic_craterlake/Bkg_1SignalPer2usFrame/DIS/NC/10x100/minQ2=1
/volatile/eic/EPIC/RECO/25.10.4/epic_craterlake/Bkg_1SignalPer2usFrame/DIS/NC/10x275/minQ2=1
/volatile/eic/EPIC/RECO/25.10.4/epic_craterlake/Bkg_1SignalPer2usFrame/EXCLUSIVE/DDVCS_ABCONV/EpIC1.1.6-1.0/18x275/q2_0_10/edecay/hminus
/volatile/eic/EPIC/RECO/25.10.4/epic_craterlake/Bkg_1SignalPer2usFrame/EXCLUSIVE/DDVCS_ABCONV/EpIC1.1.6-1.0/18x275/q2_0_10/edecay/hplus
/volatile/eic/EPIC/RECO/25.10.4/epic_craterlake/Bkg_1SignalPer2usFrame/EXCLUSIVE/DVMP/EpIC1.1.6-1.1/unpolarised/18x275/q2_1_1000
/volatile/eic/EPIC/RECO/25.10.4/epic_craterlake/Bkg_1SignalPer2usFrame/SIDIS/pythia6-eic/1.0.0/18x275/q2_0to1
/volatile/eic/EPIC/RECO/25.10.4/epic_craterlake/Bkg_1SignalPer2usFrame/Synrad_18GeV_Vac_10000Ahr_Runtime_50s_Egas_18GeV_Hgas_275GeV/DIS/NC/18x275/minQ2=1
/volatile/eic/EPIC/RECO/25.10.4/epic_craterlake/Bkg_1SignalPer2usFrame/Synrad_18GeV_Vac_10000Ahr_Runtime_50s_Egas_18GeV_Hgas_275GeV/EXCLUSIVE/DVCS_ABCONV/18x275
  </Dids>
</DidStrips>

The six signal channels above resolve to **eight leaf datasets** (the
directories that actually hold the RECO `.edm4eic.root` files). The
`DDVCS_ABCONV` channel splits into `hminus`/`hplus`, and the `Synrad_18GeV_…`
folder is a self-contained subtree (DIS/NC + DVCS_ABCONV) mixed with
**synchrotron radiation only** rather than the full cocktail:

| Leaf dataset | Beam | Background | Files |
| --- | --- | --- | --- |
| `DIS/NC/10x100/minQ2=1` | 10x100 | cocktail | 4 978 |
| `DIS/NC/10x275/minQ2=1` | 10x275 | cocktail | 5 922 |
| `EXCLUSIVE/DDVCS_ABCONV/…/q2_0_10/edecay/hminus` | 18x275 | cocktail | 7 517 |
| `EXCLUSIVE/DDVCS_ABCONV/…/q2_0_10/edecay/hplus` | 18x275 | cocktail | 7 517 |
| `EXCLUSIVE/DVMP/…/unpolarised/18x275/q2_1_1000` | 18x275 | cocktail | 6 803 |
| `SIDIS/pythia6-eic/1.0.0/18x275/q2_0to1` | 18x275 | cocktail | **1** ⚠️ |
| `Synrad_18GeV_…/DIS/NC/18x275/minQ2=1` | 18x275 | synrad-only | 46 696 |
| `Synrad_18GeV_…/EXCLUSIVE/DVCS_ABCONV/18x275` | 18x275 | synrad-only | 20 103 |

> ⚠️ **SIDIS** currently has a single reconstructed file
> (`…run10.ab.0173…`) — the rest of that dataset is not (yet) reconstructed on
> XRootD. Treat it as a placeholder until the campaign completes.

<DidStrips
  didpath="/volatile/eic/EPIC/RECO/25.10.4/epic_craterlake/Bkg_Exactly1SignalPer2usFrame/"
  csvpath="root://sci-xrootd.jlab.org//work/eic/users/romanov/epic-background-2025-10/csv_reco/"
  version="25.10.4"
  name="Bkg_Exactly1SignalPer2usFrame"
>
  <Tags color="violet" desc="Physics process">
    <Tag desc="Exclusive processes">EXCLUSIVE</Tag>
    <Tag desc="Semi-Inclusive DIS">SIDIS</Tag>
  </Tags>
  <Dids>
/volatile/eic/EPIC/RECO/25.10.4/epic_craterlake/Bkg_Exactly1SignalPer2usFrame/EXCLUSIVE
/volatile/eic/EPIC/RECO/25.10.4/epic_craterlake/Bkg_Exactly1SignalPer2usFrame/SIDIS
  </Dids>
</DidStrips>

<DidStrips
  didpath="/volatile/eic/EPIC/RECO/25.10.4/epic_craterlake/Bkg_OnlyPer2usFrame/"
  csvpath="root://sci-xrootd.jlab.org//work/eic/users/romanov/epic-background-2025-10/csv_reco/"
  version="25.10.4"
  name="Bkg_OnlyPer2usFrame"
>
  <Tags color="teal" desc="Background composition">
    <Tag desc="Only proton beam-gas background">proton-beamgas</Tag>
  </Tags>
  <Dids>
/volatile/eic/EPIC/RECO/25.10.4/epic_craterlake/Bkg_OnlyPer2usFrame/
  </Dids>
</DidStrips>

<DidStrips
  didpath="/volatile/eic/EPIC/RECO/25.10.4/epic_craterlake/Bkg_RealisticSignalPer2usFrame/"
  csvpath="root://sci-xrootd.jlab.org//work/eic/users/romanov/epic-background-2025-10/csv_reco/"
  version="25.10.4"
  name="Bkg_RealisticSignalPer2usFrame"
>
  <Tags color="violet" desc="Physics process">
    <Tag desc="Semi-Inclusive DIS (realistic signal only)">SIDIS</Tag>
  </Tags>
  <Dids>
/volatile/eic/EPIC/RECO/25.10.4/epic_craterlake/Bkg_RealisticSignalPer2usFrame/SIDIS
  </Dids>
</DidStrips>


## Using these DIDs

A DID is just a pointer — it resolves to a set of files (PFNs) on Rucio
Storage Elements. Two upstream pages cover this in full; this section is
the bare minimum to get you started.

- 📚 [Rucio usage tutorial](https://eic.github.io/tutorial-file-access/02-rucio_usage/index.html) — setup, auth, full command reference.
- 📚 [Use-cases tutorial](https://eic.github.io/tutorial-file-access/03-use_cases/index.html) — download vs. stream, batch workflows, common patterns.

### 1. One-time setup (inside `eic-shell`)

```bash
# Voms / OIDC auth — pick what matches your account (see Rucio tutorial).
rucio whoami
```

If `rucio whoami` returns your identity, you're done. If not, follow the
auth steps on the [Rucio usage tutorial](https://eic.github.io/tutorial-file-access/02-rucio_usage/index.html).

### 2. See what's inside a dataset

```bash
rucio did content list 'epic:/RECO/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=1'
```

Get list of files to 

```bash
rucio replica list file --protocols root --pfns --rses isopenaccess 'epic:/RECO/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=1'
```

### 3. Download files locally

```bash
rucio download 'epic:/RECO/26.04.1/epic_craterlake/Bkg_Exact1S_2us/GoldCt/10um/DIS/NC/10x100/minQ2=1'
```

> (!) You probably don't want to download the full dataset!

Downloads land in a directory tree mirroring the DID. Add `--nrandom N`
to pull only a sample, or `--rse <RSE>` to pin a storage element.

### 4. Stream over XRootD (no local copy)

Most analyses can read directly from XRootD — faster on the JLab farm and
saves disk:

```bash
# List replica URLs for a DID
rucio list-file-replicas --pfns 'epic:/RECO/26.04.1/.../minQ2=1' | head

# Then open them directly, e.g. in ROOT / uproot / EICrecon:
root -l 'root://dtn-eic.jlab.org//volatile/eic/EPIC/RECO/.../file.edm4eic.root'
```

See [use-cases](https://eic.github.io/tutorial-file-access/03-use_cases/index.html) for the recommended patterns when running many jobs over a dataset.
