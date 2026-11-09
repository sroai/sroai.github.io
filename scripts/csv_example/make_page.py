#!/usr/bin/env python3
"""make_page.py — writes ai-epic-background/csv-example.md, the CSV Example Event page.

Input: event.json (extract_event.py on one converted file) and ai-epic-background/csv-schema.yaml (what one row of
each file is). The page follows one real event through the files: a figure of its particles and of hit and cluster
rows pointing at them, the rows per event of every file, and the event's real rows. The figure is laid out by hand
for event 0 of event.json (node positions and card texts below); a different event needs those edited.

Run: python3 scripts/csv_example/make_page.py   (needs PyYAML)
"""
import html
import json
import os

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(HERE))
data = json.load(open(os.path.join(HERE, "event.json")))
counts, n_events, ex = data["counts"], data["events"], data["example"]
schema = yaml.safe_load(open(os.path.join(SITE, "ai-epic-background", "csv-schema.yaml")))


def esc(text):
    return html.escape(str(text), quote=True)


def per_event(role):
    value = counts[role]["rows"] / n_events
    return f"{value:,.0f}" if value >= 10 else f"{value:.1f}".rstrip("0").rstrip(".") if value else "0"


def elbow(points, cls):
    d = "M" + " L".join(f"{px:g},{py:g}" for px, py in points)
    end = ' marker-end="url(#csv-example-arrow)"' if cls == "ptr" else ""
    return f'<path class="{cls}" d="{d}" fill="none"{end}/>'


def label(x, y, text):
    return f'<text class="colhead" x="{x}" y="{y}">{esc(text)}</text>'


# ---------------------------------------------------------------- the figure: event 0
D = [16, 156, 296, 436, 576]          # x of the depth columns
NW, NH = 112, 40
TOP = 34
nodes = {   # MCParticles index (or "beams"): (depth, top y, title, line 2, kind)
    "beams": (0, 0, "p #0 · e #1", "gen 4 · the beams", "beam"),
    2: (1, 20, "e′ #2", "gen 1 · 17.0 GeV", "primary"),
    3: (1, 80, "K⁺ #3", "gen 1 · 28.4 GeV", "primary"),
    4: (1, 0, "Λ #4", "gen 1 · 80.0 GeV", "primary"),
    5: (2, 0, "π⁰ #5", "Geant4 · 14.9 GeV", "g4"),
    6: (2, 330, "n #6", "Geant4 · 65.0 GeV", "g4"),
    6383: (3, 140, "γ #6383", "Geant4 · 7.3 GeV", "g4"),
    6384: (3, 230, "γ #6384", "Geant4 · 7.6 GeV", "g4"),
    6385: (4, 196, "e⁻ #6385", "Geant4 · 2.1 GeV", "g4"),
    6386: (4, 264, "e⁺ #6386", "Geant4 · 5.5 GeV", "g4"),
    8: (3, 330, "p #8", "Geant4 · 1.0 GeV", "g4"),
}


def centre(key):
    return nodes[key][1] + NH / 2


def set_centre(key, cy):
    depth, _, a, b, kind = nodes[key]
    nodes[key] = (depth, cy - NH / 2, a, b, kind)


set_centre(5, (centre(6383) + centre(6384)) / 2)
set_centre(4, (centre(5) + centre(6)) / 2)
set_centre("beams", (centre(2) + centre(3) + centre(4)) / 3)
for key in nodes:
    depth, top, a, b, kind = nodes[key]
    nodes[key] = (depth, top + TOP, a, b, kind)

fig = []
for x, text in ((D[0], "beams"), (D[1], "generator"), (D[2], "made by Geant4 and saved")):
    fig.append(label(x, 18, text))
for parent, children in (("beams", [2, 3, 4]), (4, [5, 6]), (5, [6383, 6384]), (6384, [6385, 6386]), (6, [8])):
    px = D[nodes[parent][0]] + NW
    bus = px + 14
    for child in children:
        fig.append(elbow([(px, centre(parent)), (bus, centre(parent)), (bus, centre(child)), (D[nodes[child][0]], centre(child))], "tree"))
for key, (depth, top, a, b, kind) in nodes.items():
    x = D[depth]
    fig.append(f'<g class="node {kind}"><rect x="{x}" y="{top:g}" width="{NW}" height="{NH}" rx="5"/>'
               f'<text class="n-title" x="{x + 10}" y="{top + 17:g}">{esc(a)}</text>'
               f'<text class="n-sub" x="{x + 10}" y="{top + 32:g}">{esc(b)}</text></g>')

CX, CW = 716, 276
cards = [  # (top, file, place, values, target particle)
    (20, "cal_hits", "EcalBarrel2 · 2.46 GeV", "prt_index 2 · primary 2 · child −1", 2),
    (80, "trk_hits", "TrackerBarrel_2", "prt_index 3 · primary 3 · child −1", 3),
    (140, "cal_hits", "ZDC_Crystal · 1.14 GeV", "prt_index 6383 · primary 4 · child 5", 6383),
    (196, "trk_hits", "B0Tracker_Station_1", "prt_index 6385 · primary 4 · child 5", 6385),
    (330, "cal_hits", "B0ECal · 0.135 GeV", "prt_index 8 · primary 4 · child 6", 8),
]
for top, role, place, values, target in cards:
    top += TOP
    fig.append(f'<g class="card"><rect x="{CX}" y="{top}" width="{CW}" height="{NH}" rx="4"/>'
               f'<text class="c-role" x="{CX + 10}" y="{top + 16}">{esc(role)}</text>'
               f'<text class="c-place" x="{CX + 74}" y="{top + 16}">{esc(place)}</text>'
               f'<text class="c-vals" x="{CX + 10}" y="{top + 32}">{esc(values)}</text></g>')
    fig.append(elbow([(CX, top + NH / 2), (D[nodes[target][0]] + NW + 2, centre(target))], "ptr"))
ctop = 392 + TOP
fig.append(f'<g class="card"><rect x="{CX}" y="{ctop}" width="{CW}" height="80" rx="4"/>'
           f'<text class="c-role" x="{CX + 10}" y="{ctop + 16}">calo_clusters</text>'
           f'<text class="c-place" x="{CX + 112}" y="{ctop + 16}">B0ECal · 7.06 GeV</text>'
           f'<text class="c-place" x="{CX + 10}" y="{ctop + 32}">cluster: clu_index 0, two rows</text>'
           f'<text class="c-vals" x="{CX + 10}" y="{ctop + 52}">link 1 · prt_index 6384 · weight 0.95</text>'
           f'<text class="c-vals" x="{CX + 10}" y="{ctop + 70}">link 0 · prt_index 6 · weight 0.05</text></g>')
fig.append(elbow([(CX, ctop + 48), (CX - 18, ctop + 48), (CX - 18, centre(6384)), (D[nodes[6384][0]] + NW + 2, centre(6384))], "ptr"))
n6 = nodes[6]
fig.append(elbow([(CX, ctop + 66), (D[n6[0]] + NW / 2, ctop + 66), (D[n6[0]] + NW / 2, n6[1] + NH + 2)], "ptr"))
fig.append(label(CX, 18, "hit and cluster rows"))
height = ctop + 80 + 16
FIGURE = (f'<svg class="event-figure" viewBox="0 0 1000 {height}" role="img" aria-label="Event 0: the beams, the generator '
          f'particles e′, K⁺ and Λ, the Λ decay to π⁰ and n, the π⁰ photons, one photon converting to e⁻ e⁺, and the hit and '
          f'cluster rows that name these particles by prt_index.">'
          f'<defs><marker id="csv-example-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
          f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="arrowhead"/></marker></defs>'
          + "".join(fig) + "</svg>")


# ---------------------------------------------------------------- tables
def fmt(value):
    if isinstance(value, float):
        if value != value:
            return ""
        if value == int(value) and abs(value) < 1e6:
            return str(int(value))
        return f"{value:.4g}"
    return str(value)


def row_table(records, columns, highlight=()):
    head = "".join(f"<th>{esc(c)}</th>" for c in columns)
    body = "".join("<tr>" + "".join(f'<td class="{"hl" if c in highlight else ""}">{esc(fmt(r.get(c, "")))}</td>' for c in columns) + "</tr>"
                   for r in records)
    return f'<div class="rows-scroll"><table class="rows"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def details(summary, body, opened=False):
    return f'<details{" open" if opened else ""}><summary>{summary}</summary>{body}</details>'


file_rows = []
for lane in ("left", "center", "right", "bottom"):
    for role in schema["layout"][lane]:
        note = " (none in this sample)" if counts[role]["rows"] == 0 else ""
        file_rows.append(f"| [`{role}`](./csv-schema#{role}) | {schema['files'][role]['row']}{note} | "
                         f"{per_event(role)} | {counts[role]['columns']} |")

mcp_cols = ["evt", "prt_index", "prt_pdg", "prt_gen_status", "prt_energy", "prt_vtx_pos_z", "prt_end_pos_z", "prt_n_daughters", "prt_parent_index"]
records = {r["prt_index"]: r for r in ex["mc_generator"] + ex["mc_lambda_chain"]}
hit_cols = ["evt", "cal_hit_system_name", "cal_hit_energy", "sim_energy", "n_contrib", "prt_index", "prt_pdg", "prt_gen_status",
            "prt_primary_index", "prt_primary_pdg", "prt_primary_child_index", "prt_primary_child_pdg"]
trk_cols = ["evt", "hit_index", "trk_hit_system_name", "trk_hit_pos_z", "prt_index", "prt_pdg", "prt_gen_status",
            "prt_primary_index", "prt_primary_pdg", "prt_primary_child_index", "prt_primary_child_pdg"]
clu_cols = ["evt", "clu_collection", "clu_index", "clu_link_index", "clu_energy", "clu_nhits", "clu_assoc_weight", "prt_index", "prt_pdg",
            "prt_primary_pdg", "prt_primary_child_pdg"]
ancestry = ("prt_index", "prt_primary_index", "prt_primary_child_index")
ROWS = "\n".join([
    details("<code>mc_particles</code>: the beams, the generator particles, the Λ decay",
            row_table([records[i] for i in [0, 1, 2, 3, 4, 5, 6, 6383, 6384] if i in records], mcp_cols, ("prt_index", "prt_parent_index")), True),
    details("<code>cal_hits</code>: the e′ in the barrel, the photon in the ZDC, the proton in the B0ECal",
            row_table([ex["cal_hits_examples"][i] for i in (0, 1, 3)], hit_cols, ancestry)),
    details("<code>trk_hits</code>: the converted photon's e⁻ and e⁺, the K⁺", row_table(ex["trk_hits_examples"], trk_cols, ancestry)),
    details("<code>calo_clusters</code>: one B0ECal cluster, two rows",
            row_table(ex["calo_clusters_example"], clu_cols, ("clu_index", "clu_link_index", "prt_index"))),
    details("<code>mcpart_lambda</code>: the Λ with its daughters' row numbers",
            row_table(ex["mcpart_lambda"], ["evt", "lam_is_first", "lam_decay", "lam_index", "neut_index", "pizero_index", "gamone_index", "gamtwo_index"],
                      ("lam_index", "neut_index", "pizero_index", "gamone_index", "gamtwo_index"))),
    details("<code>reco_particles</code> and <code>reco_dis</code>: what was reconstructed",
            "<p><code>mc_elec_index</code> 2 and <code>mc_lam_index</code> 4 are rows of <code>mc_particles</code>. "
            "<code>elec_epz_index</code>, the E − pz electron, is a <code>rec_index</code> of <code>reco_particles</code>; "
            "<code>elec_index</code> indexes ReconstructedChargedParticles, which no CSV file holds.</p>"
            + row_table(ex["reco_particles"], ["evt", "rec_index", "rec_pdg", "rec_charge", "rec_energy", "rec_mom_z", "rec_n_clusters", "rec_n_tracks"], ("rec_index",))
            + row_table(ex["reco_dis"], ["evt", "mc_x", "mc_q2", "electron_x", "electron_q2", "da_x", "da_q2", "elec_index", "mc_elec_index",
                                         "mc_lam_index", "mc_lam_decay", "mc_true_t", "mc_lam_exp_t"], ("mc_elec_index", "mc_lam_index"))),
    details("<code>mc_dis</code>: the generator's own variables", row_table(ex["mc_dis"], ["evt", "xbj", "q2", "y_d", "w", "tprime"])),
])

g4 = ex["mc_particles_by_status"].get("0", 0)
by_pdg = ex["mc_geant4_by_pdg"]
g4_kinds = ", ".join(f"{by_pdg.get(pdg, 0):,} {name}" for pdg, name in (("22", "γ"), ("11", "e⁻"), ("-11", "e⁺"), ("2112", "n"), ("2212", "p")))

page = f'''---
aside: false
---

<!-- Generated by scripts/csv_example/make_page.py from scripts/csv_example/event.json; edit the script, not this file. -->

# CSV Example Event

One real event followed through the eic2ai CSV files: which rows it has, and how the row numbers in one file lead to
rows of another. The event is event 0 of a 2026-11 Sullivan-process file, e p → e′ K⁺ Λ at 9 × 100 GeV, simulated
and reconstructed with eic_xl 26.11. [CSV Schema](./csv-schema) lists every column.

## Rows per file

The first {n_events} events of that file. Every file has the column `evt`; the rows of one event share it.

| File | One row is | Rows per event | Columns |
| ---- | ---------- | -------------: | ------: |
{chr(10).join(file_rows)}

## Event 0 through the files

The Λ decays to n π⁰ at z = 4.75 m. One π⁰ photon reaches the ZDC; the other converts to e⁻ e⁺ at z = 5.80 m and
leaves hits in the B0 tracker. The neutron interacts at z = 7.11 m; a B0ECal cell names a proton made there.

<figure class="event">
<div class="figure-scroll">{FIGURE}</div>
<figcaption>Boxes on the left: rows of <code>mc_particles</code> (#n is <code>prt_index</code>); the lines between them are <code>prt_parent_index</code>. Highlighted boxes: generator particles (<code>prt_gen_status</code> 1), where every walk up the parents ends. Cards on the right: real rows of <code>cal_hits</code>, <code>trk_hits</code> and <code>calo_clusters</code>; the dashed arrow is the row's <code>prt_index</code>. The B0ECal cluster has two rows, one per particle that put energy into it.</figcaption>
</figure>

| Column of a hit row | What it holds | ZDC hit | B0 tracker hit |
| ------------------- | ------------- | ------- | -------------- |
| `prt_index` | the saved particle Geant4 credited with the energy | 6383 γ | 6385 e⁻ |
| `prt_primary_index` | the generator particle it comes from | 4 Λ | 4 Λ |
| `prt_primary_child_index` | the particle one step below that | 5 π⁰ | 5 π⁰ |

`prt_gen_status`: 4 beam, 1 generator particle (a primary), 2 decayed by the generator, 0 made by Geant4 (a
secondary). Event 0 has {ex["mc_particles_rows"]:,} rows in `mc_particles`: 5 from the generator, {g4:,} made by Geant4
({g4_kinds}, …). It has {ex["trk_hits_rows"]} tracker hits, {ex["cal_hits_rows"]:,} calorimeter cell hits and
{ex["calo_clusters_clusters"]} clusters in {ex["calo_clusters_rows"]} cluster rows.

## The rows

Event 0, selected columns; highlighted cells are row numbers that point into another file.

<div class="row-tables">
{ROWS}
</div>

<style scoped>
.figure-scroll {{ overflow-x: auto; }}
.event-figure {{ display: block; width: 100%; min-width: 760px; height: auto; }}
figure.event {{ margin: 24px 0; }}
figure.event figcaption {{ font-size: 13px; color: var(--vp-c-text-2); margin-top: 8px; }}
.event-figure .colhead {{ font: 600 10.5px var(--vp-font-family-base); fill: var(--vp-c-text-2); letter-spacing: .08em; text-transform: uppercase; }}
.event-figure .node rect {{ fill: var(--vp-c-bg-soft); stroke: var(--vp-c-divider); }}
.event-figure .node.primary rect {{ fill: var(--vp-c-brand-soft); stroke: var(--vp-c-brand-1); stroke-width: 1.8; }}
.event-figure .node.beam rect {{ stroke-dasharray: 4 3; }}
.event-figure .n-title {{ font: 600 13px var(--vp-font-family-base); fill: var(--vp-c-text-1); }}
.event-figure .n-sub {{ font: 11px var(--vp-font-family-base); fill: var(--vp-c-text-2); }}
.event-figure .tree {{ stroke: var(--vp-c-text-3); stroke-width: 1.2; }}
.event-figure .ptr {{ stroke: var(--vp-c-brand-1); stroke-width: 1.3; stroke-dasharray: 5 3; }}
.event-figure .arrowhead {{ fill: var(--vp-c-brand-1); }}
.event-figure .card rect {{ fill: var(--vp-c-bg-soft); stroke: var(--vp-c-divider); }}
.event-figure .c-role {{ font: 600 11.5px var(--vp-font-family-mono); fill: var(--vp-c-brand-1); }}
.event-figure .c-place {{ font: 11px var(--vp-font-family-base); fill: var(--vp-c-text-2); }}
.event-figure .c-vals {{ font: 11.5px var(--vp-font-family-mono); fill: var(--vp-c-text-1); }}
.row-tables details {{ margin: 10px 0; padding: 8px 12px; border: 1px solid var(--vp-c-divider); border-radius: 8px; background: var(--vp-c-bg-soft); }}
.row-tables summary {{ cursor: pointer; font-weight: 600; }}
.row-tables p {{ font-size: 13px; color: var(--vp-c-text-2); }}
.rows-scroll {{ overflow-x: auto; }}
.vp-doc table.rows {{ display: table; margin: 8px 0; font: 12px var(--vp-font-family-mono); }}
.vp-doc table.rows th, .vp-doc table.rows td {{ padding: 3px 8px; white-space: nowrap; }}
.vp-doc table.rows td.hl {{ color: var(--vp-c-brand-1); font-weight: 600; }}
</style>
'''
out = os.path.join(SITE, "ai-epic-background", "csv-example.md")
open(out, "w").write(page)
print("wrote", out, len(page), "bytes")
