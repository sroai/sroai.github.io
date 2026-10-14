# DidStrips — VitePress handoff

Declarative, **hand-authored** replacement for `DidTable`. Nothing is parsed:
every tag's label, colour and hover description is set explicitly in Markdown.
Authoring style **B** (grouped by colour).

## 1. Install

Copy `DidStrips.vue` into your theme components folder:

```
docs/.vitepress/theme/components/DidStrips.vue
```

## 2. Register (globally, like DidTable)

In `docs/.vitepress/theme/index.ts` — import the **default** export plus the
four child markers, and register all five:

```ts
import DidStrips, { Tags, Tag, More, Dids } from "./components/DidStrips.vue";

// inside enhanceApp({ app }) { ... }
app.component("DidStrips", DidStrips);
app.component("Tags", Tags);
app.component("Tag", Tag);
app.component("More", More);
app.component("Dids", Dids);
```

> **Name collisions:** `Tags` / `Tag` / `More` / `Dids` are generic global
> names. If anything else in your docs uses those tags, rename them at
> registration (e.g. `app.component("DidTag", Tag)`) — the component matches
> children by an internal marker, not by tag name, so any names work.

## 3. Author in `data.md`

```md
### Bkg_Exact1S_2us

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
    <Tag desc="Detector configuration: ePIC craterlake">epic_craterlake</Tag>
    <Tag desc="Event generator: MadGraph5 v3.7.0">madgraph5-3.7.0-1.0</Tag>
    <Tag desc="Beam-pipe: gold coating, 10 um">GoldCt / 10um</Tag>
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
```

## Reference

**`<DidStrips>` props**
- `didpath` — string shown verbatim as the copyable prefix line (use
  `{FULL|RECO}` or any placeholder text you like; it is **not** interpreted).
- `version` — dark identity pill (e.g. campaign `26.04.1`).
- `name` — teal dataset-name chip.
- `open` — boolean; start expanded.

**`<Tags color="..." desc="...">`** — a colour group on the main row.
`color` applies to every child chip; `desc` is the group's default tooltip.

**`<More color="...">`** — same, but its chips render under *Additional info*
when the strip is expanded.

**`<Tag desc="..." color="...">label</Tag>`** — one chip. The element text is
the label. `desc` sets the hover tooltip (falls back to the group's `desc`);
`color`/`bg` overrides the group colour for just this chip.

**`<Dids>`** — one full DID per line. Rendered as the expandable table with a
copy button per row and *Copy all*. `FULL·n` / `RECO·n` counts come from a
simple substring check (`/FULL/`, `/RECO/`) of these lines.

**Colours** — named: `violet sky amber slate green indigo teal rose fuchsia
gray blue red orange`, or pass any CSS colour / `#hex`. Chip background/border
are derived from the hue and adapt to light/dark via `--vp-c-bg`.

## Migrating from DidTable

`DidTable` took a single `:rows='[...]'` JSON blob. With `DidStrips` you split
that into (a) the DIDs — paste them verbatim into `<Dids>` — and (b) the
handful of tags you want surfaced, authored once per colour group. One
`<DidStrips>` per `(campaign, data_name)` pair, same as one `<DidTable>` today.
