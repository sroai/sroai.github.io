---
layout: home
title: SRO AI
titleTemplate: AI for Streaming Readout

hero:
  name: SRO AI
  text: AI for Streaming Readout
  tagline: Real-time signal and background separation in continuous nuclear physics data streams
  actions:
    - theme: brand
      text: EIC AI Background
      link: /ai-epic-background/
    - theme: alt
      text: GitHub
      link: https://github.com/sroai

features:
  - icon: 🌊
    title: Streaming data frames
    details: Continuous detector readout as time-ordered frames that keep timing, pileup and detector response — no event boundaries required.
  - icon: ⚡
    title: Streaming AI core
    details: Selective state-space models with linear-time inference and self-supervised predictive learning, built for real-time throughput.
  - icon: 🧩
    title: SLERM
    details: Streaming Latent Event Representation Modeling — relational structure across detector signals without explicit graph construction.
  - icon: ⚖️
    title: Physics constraints
    details: Energy-momentum conservation, kinematics and detector response priors built into the training objective.
---

## Mission

The Electron-Ion Collider will read out its detectors continuously at rates near
100 Gb/s. Rare physics signals have to be found in real time, inside unsegmented
data with heavy background and pileup. Trigger and reconstruction frameworks
built for discrete, low-rate events do not scale to this regime, and offline
machine learning pipelines add latency that limits sensitivity to rare processes.

SRO AI develops stream-native, physics-integrated AI that runs at the data
acquisition layer: continuous signal–background discrimination, event
prioritization and anomaly detection as the data are produced.

## Research thrusts

- **Data layer** — a unified streaming representation for Geant4 simulation and
  Jefferson Lab pseudo-streaming data: synchronized detector channels, normalization
  across run conditions, sliding temporal windows.
- **AI layer** — a state-space backbone, JEPA-style self-supervised learning and
  SLERM, with physics constraints in the loss.
- **Benchmarking** — signal efficiency, background rejection, reconstructed
  kinematics, latency and throughput, measured against event-based pipelines as
  data rate and pileup grow.
- **Integration** — real-time inference inside the JANA2 framework, with model
  compression and quantization for streaming deployment.

The physics benchmark is the **Sullivan process** — scattering off the pion cloud of
the nucleon, a key channel for meson structure at the EIC — studied against inclusive
DIS and meson production backgrounds at high luminosity.

## Projects

| Project | What it provides |
| ------- | ---------------- |
| [EIC AI Background](/ai-epic-background/) | Full-simulation pipeline, background mixing and CSV datasets for the ePIC detector |
| [eic2ai](https://github.com/sroai/eic2ai) | Single-pass converter from ePIC ROOT (podio) files to AI-ready CSV |
| [Meson Structure](https://jeffersonlab.github.io/meson-structure/) | EIC meson structure simulation campaigns, data access and analysis |

## Institutions

- [The Catholic University of America](https://www.catholic.edu/)
- [Thomas Jefferson National Accelerator Facility](https://www.jlab.org/)
