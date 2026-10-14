---
name: update-data-md
description: Use this skill when the user asks to update, refresh, regenerate, or rebuild `ai-epic-background/data.md` — the catalog of available ePIC background-mixed datasets in Rucio. The skill queries Rucio for all DIDs with `is_background_mixed=true`, drops the CI/`main` branch entries, groups the remaining real-campaign DIDs by campaign → data name, and helps you hand-author one `<DidStrips>` block per data name (with per-row and per-strip copy buttons and hover-tooltip tags). Trigger phrases: "update data.md", "refresh the data catalog", "regenerate data page", "pull the new datasets from rucio", "what backgrounds are on rucio", "list available DIDs".
---

# Update `ai-epic-background/data.md`

`ai-epic-background/data.md` is the project's human-readable catalog of background-mixed
datasets available in Rucio. Its source of truth is the output of
`rucio did list --filter 'is_background_mixed=true' 'epic:*'`.

**This is a hand-authoring task, not an automated parse.** The page uses the
**`<DidStrips>` Vue component**, whose tags — the coloured chips with hover
tooltips — carry meaning (physics process, beam energy, `minQ2`, signal mass,
…) that *you* assign. The DID path has **no fixed schema**: data names and
segment layouts change from campaign to campaign, and the same position can
mean different things in different datasets. There is nothing reliable to
parse into tags, so don't try. There is also not much data (a handful of
strips), so authoring by hand is quick.

Your job: query Rucio, digest the result with the helper script, then **edit
`ai-epic-background/data.md` directly** — add/update one `<DidStrips>` block per
`(campaign, data_name)`, choosing sensible tag groups, colours, and tooltips.

> Prior versions of this page used an auto-generated `<DidTable>`. That is
> retired. Do not emit `<DidTable>`; author `<DidStrips>` (see step 3).

---

## 1. Query Rucio inside the `eic_xl` container

Rucio lives inside the `eicweb/eic_xl:nightly` image. The command can be
slow (tens of seconds to a couple of minutes).

**Docker (most portable):**

```bash
docker run --rm eicweb/eic_xl:nightly \
  rucio did list --filter 'is_background_mixed=true' 'epic:*' > /tmp/rucio.txt
```

**Apptainer / Singularity (JLab farm, CVMFS):**

```bash
apptainer exec /cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:nightly \
  rucio did list --filter 'is_background_mixed=true' 'epic:*' > /tmp/rucio.txt
```

**Authentication:** the container ships with a working Rucio config for the
EIC instance, but the user may need an active X.509 proxy / OIDC token. If
the command fails with a 401/403, surface that — auth is the user's
responsibility, not the skill's.

---

## 2. Digest the DIDs with the helper

`scripts/summarize_rucio_dids.py` is **read-only** — it never writes
`ai-epic-background/data.md`. It parses the Rucio table, drops `main/` and non-`FULL`/`RECO`
and non-`epic_craterlake` entries, groups by `(campaign, data_name)`, and for
each group prints exactly the material you need to author a strip:

- **`didpath`** — the shared DID prefix (with `{FULL|RECO}` when both
  partitions are present) to paste into the `didpath=` attribute;
- **`version`** (campaign) and **`name`** (data name);
- **FULL / RECO** counts;
- **varying segments by position** — the segments that differ within the
  group. These are your candidate **tag groups** (`<Tags>`);
- **constant segments** — the same across every DID. These usually belong in
  the collapsed **`<More>`** section, not the main row;
- the full, sorted **DID list** to paste verbatim into `<Dids>`.

```bash
python scripts/summarize_rucio_dids.py /tmp/rucio.txt
# or:  cat /tmp/rucio.txt | python scripts/summarize_rucio_dids.py
# add --json for a machine-readable version of the same grouping
```

Read this output; it tells you what varies (→ tag groups) and what is fixed
(→ `<More>`). You still decide the labels, colours, and tooltips.

---

## 3. Author `<DidStrips>` blocks in `ai-epic-background/data.md`

Edit `ai-epic-background/data.md` by hand. The generated strips live between the
`<!-- BEGIN STRIPS -->` and `<!-- END STRIPS -->` markers (Rucio campaigns);
the JLab-xrootd `25.10` strips and all surrounding prose (intro, conventions,
"Using these DIDs") are hand-edited and stay as they are unless the data
changed. Add a `## Campaign <version>` heading per campaign (newest first) and
one `<DidStrips>` per `(campaign, data_name)`.

### Anatomy of a strip

```md
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
  </Dids>
</DidStrips>
```

### Prop / child reference

- **`<DidStrips didpath version name open>`** — `didpath` is shown verbatim
  as the copyable prefix line (use the helper's `didpath`; `{FULL|RECO}` is
  just display text, not interpreted). `version` → dark campaign pill, `name`
  → teal dataset chip. `open` starts the strip expanded.
- **`<Tags color="..." desc="...">`** — a colour group on the main row.
  `color` applies to every child chip; `desc` is the group's default tooltip.
- **`<More color="...">`** — same, but renders under *Additional info* when the
  strip is expanded. Put constant/context segments here.
- **`<Tag desc="..." color="...">label</Tag>`** — one chip. Element text is the
  label; `desc` sets the hover tooltip (falls back to the group's `desc`);
  `color`/`bg` overrides the group colour for a single chip.
- **`<Dids>`** — one full DID per line, pasted verbatim. Rendered as the
  expandable table with a per-row 📋 and *Copy all*. The `FULL·n` / `RECO·n`
  counts come from a substring check of `/FULL/` and `/RECO/` in these lines.

**Colours** — named: `violet sky amber slate green indigo teal rose fuchsia
gray blue red orange`, or any CSS colour / `#hex`. Chip bg/border derive from
the hue and adapt to light/dark automatically. Reuse a consistent colour per
concept across strips (e.g. `violet` = physics process, `sky` = beam energy,
`amber` = `minQ2`) so the page reads coherently.

### Authoring guidance

- One `<DidStrips>` per `(campaign, data_name)`; group `## Campaign` headings
  newest-first so the sidebar/TOC order matches.
- Map each **varying-segment position** from the helper to a `<Tags>` group.
  You don't have to surface every distinct value — pick the ones a user would
  filter on. Constant segments → `<More>`.
- Write real tooltips (`desc`): expand acronyms, give units. This is the whole
  point of the redesign over a flat table.
- Paste the DID list into `<Dids>` **verbatim and complete** — the strip's copy
  buttons and FULL/RECO counts come straight from those lines, so this is the
  authoritative list even though only a few tags are surfaced.
- Update the `_Last updated: **YYYY-MM-DD**_` line near the top.

---

## 4. Wire `data.md` into the docs

Already done in `.vitepress/config.mts` (top nav `Data` → `/data`;
sidebar `Data` → `Available Datasets`). If those entries went missing after a
config rewrite, add them back.

`<DidStrips>` and its child markers `Tags` / `Tag` / `More` / `Dids` are
globally registered in `.vitepress/theme/index.ts`, so no per-page
imports are needed.

---

## 5. Commit

`ai-epic-background/data.md` is the only artefact to commit. Do **not** commit the raw
Rucio output (`/tmp/rucio.txt`). Typical message:

```
docs: refresh data.md from rucio (N DIDs across M campaigns)
```

---

## 6. Verify

- `cd docs && npm run build` succeeds with no "page not found" and no Vue
  warnings about unknown components (`DidStrips`/`Tags`/`Tag`/`More`/`Dids`).
- Every `## Campaign` heading is a version tag (e.g. `26.04.1`), never `main`.
- Each strip's `<Dids>` list is complete; FULL has its RECO twin where Rucio
  has one.
- Spot-check a strip in `npm run dev`: chips show tooltips on hover, *Copy all*
  and per-row 📋 work, the prefix line copies.

Then report to the user: number of campaigns, number of DIDs, the path written
(`ai-epic-background/data.md`), and how many `main/` entries were skipped.

---

## Notes

- The Rucio output table widens to fit the longest DID; the helper uses
  `split("|", 2)[1]` and only reads the first column, so column widths don't
  matter.
- Some DIDs have unusual tails (e.g. SIDIS:
  `.../SIDIS/D0_ABCONV/pythia8.306-1.1/10x100/q2_100/hiDiv`). Their extra
  segments show up as their own varying positions in the helper output —
  decide per case whether each becomes a tag or goes in `<More>`.
- The component lives at `.vitepress/theme/components/DidStrips.vue`;
  its header comment and
  `.vitepress/theme/components/DidStrips.README.md` document it in more
  depth.
