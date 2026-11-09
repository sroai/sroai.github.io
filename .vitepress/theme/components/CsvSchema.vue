<script setup lang="ts">
// CsvSchema.vue: the eic2ai CSV files drawn as tables with arrows from the columns that hold a row number of
// another file. Click a box to open its full column list. The content comes from
// ai-epic-background/csv-schema.yaml through csv-schema.data.ts; nothing about the files is written here.
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from "vue";

const props = defineProps<{ schema: any }>();

const LANES = ["left", "center", "right"];
const files = computed<Record<string, any>>(() => props.schema.files);
const layout = computed<Record<string, string[]>>(() => props.schema.layout);
const titles = computed<Record<string, string>>(() => props.schema.laneTitles ?? {});
const lanes = computed(() => LANES.filter((lane) => layout.value[lane]?.length));
const band = computed<string[]>(() => layout.value.bottom ?? []);

const open = reactive<Record<string, boolean>>({});
const hovered = ref("");
const query = ref("");
const needle = computed(() => query.value.trim().toLowerCase());

function matches(column: any) {
    return column.name.toLowerCase().includes(needle.value) || column.text.toLowerCase().includes(needle.value);
}

/** The rows a box shows: every column when open, the matches while filtering, else the key and link columns. */
function rows(file: any) {
    if (needle.value) return file.columns.filter(matches);
    if (open[file.name]) return file.columns;
    return file.columns.filter((column: any) => column.key || column.linkFile);
}

/** Whether a group heading (the prefix legend) goes above row i. */
function startsGroup(file: any, list: any[], i: number) {
    const group = list[i].group;
    return open[file.name] && !needle.value && group && (i === 0 || list[i - 1].group !== group);
}

function laneWidths() {
    return lanes.value
        .map((lane) => (layout.value[lane].some((name) => open[name]) ? "minmax(0, 3fr)" : "minmax(210px, 0.8fr)"))
        .join(" ");
}

function toggle(name: string) {
    open[name] = !open[name];
}

function show(name: string) {
    open[name] = true;
    if (typeof history !== "undefined") history.replaceState(null, "", "#" + name);
    nextTick(() => document.getElementById(name)?.scrollIntoView({ block: "start", behavior: "smooth" }));
}

function setAll(value: boolean) {
    for (const name of Object.keys(files.value)) open[name] = value;
}

// ---- arrows: measured from the rendered boxes, redrawn whenever the layout moves
const diagram = ref<HTMLElement | null>(null);
const lanesBox = ref<HTMLElement | null>(null);
const bandBox = ref<HTMLElement | null>(null);
const arrows = ref<{ d: string; files: string[] }[]>([]);
const size = ref({ width: 0, height: 0 });

function box(element: Element, base: DOMRect) {
    const r = element.getBoundingClientRect();
    return { left: r.left - base.left, right: r.right - base.left, top: r.top - base.top, bottom: r.bottom - base.top };
}

function anchorY(fileBox: Element, column: string, base: DOMRect) {
    const cell = fileBox.querySelector(`[data-column="${column}"]`);
    if (cell) {
        const r = box(cell, base);
        return (r.top + r.bottom) / 2;
    }
    return box(fileBox, base).top + 16;
}

function drawArrows() {
    const root = diagram.value;
    if (!root || !lanesBox.value) return;
    size.value = { width: root.clientWidth, height: root.clientHeight };
    const stacked = getComputedStyle(lanesBox.value).gridTemplateColumns.trim().split(/\s+/).length < 2;
    if (stacked) {
        arrows.value = [];
        return;
    }
    const base = root.getBoundingClientRect();
    const drawn: { d: string; files: string[] }[] = [];
    const fromBand = new Map<string, string[]>();   // target file → band files pointing at it

    for (const file of Object.values(files.value)) {
        const targets = new Map<string, any[]>();
        for (const column of file.columns) {
            if (!column.linkFile) continue;
            if (!targets.has(column.linkFile)) targets.set(column.linkFile, []);
            targets.get(column.linkFile)!.push(column);
        }
        for (const [target, columns] of targets) {
            if (band.value.includes(file.name) && !band.value.includes(target)) {
                fromBand.set(target, [...(fromBand.get(target) ?? []), file.name]);
                continue;
            }
            const source = root.querySelector(`[data-file="${file.name}"]`);
            const destination = root.querySelector(`[data-file="${target}"]`);
            if (!source || !destination) continue;
            const s = box(source, base);
            const t = box(destination, base);
            const visible = columns.find((column) => source.querySelector(`[data-column="${column.name}"]`));
            const sy = anchorY(source, (visible ?? columns[0]).name, base);
            const ty = anchorY(destination, columns[0].linkColumn, base);
            let d: string;
            if (s.right < t.left) {
                const dx = Math.max(24, (t.left - s.right) / 2);
                d = `M${s.right},${sy} C${s.right + dx},${sy} ${t.left - dx},${ty} ${t.left - 2},${ty}`;
            } else if (s.left > t.right) {
                const dx = Math.max(24, (s.left - t.right) / 2);
                d = `M${s.left},${sy} C${s.left - dx},${sy} ${t.right + dx},${ty} ${t.right + 2},${ty}`;
            } else {
                // same column of the diagram (or the same box): a loop on the right side
                const x = Math.max(s.right, t.right);
                d = `M${s.right},${sy} C${x + 34},${sy} ${x + 34},${ty} ${t.right + 2},${ty}`;
            }
            drawn.push({ d, files: [file.name, target] });
        }
    }
    // the band below the columns: one arrow per target, from the band's top edge up into the target's bottom
    if (bandBox.value) {
        const b = box(bandBox.value, base);
        for (const [target, sources] of fromBand) {
            const destination = root.querySelector(`[data-file="${target}"]`);
            if (!destination) continue;
            const t = box(destination, base);
            const x = (t.left + t.right) / 2;
            drawn.push({ d: `M${x},${b.top} L${x},${t.bottom + 2}`, files: [target, ...sources] });
        }
    }
    arrows.value = drawn;
}

const active = computed(() => {
    const names = new Set(Object.keys(open).filter((name) => open[name]));
    if (hovered.value) names.add(hovered.value);
    return names;
});

let observer: ResizeObserver | null = null;
let frame = 0;
function scheduleDraw() {
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(drawArrows);
}

function openFromHash() {
    const name = decodeURIComponent(location.hash.slice(1));
    if (files.value[name]) show(name);
}

onMounted(() => {
    observer = new ResizeObserver(scheduleDraw);
    if (diagram.value) observer.observe(diagram.value);
    window.addEventListener("hashchange", openFromHash);
    openFromHash();
    scheduleDraw();
});
onBeforeUnmount(() => {
    observer?.disconnect();
    window.removeEventListener("hashchange", openFromHash);
    cancelAnimationFrame(frame);
});
watch([open, needle], () => nextTick(scheduleDraw));
</script>

<template>
  <div class="csv-schema">
    <div class="cs-toolbar">
      <input v-model="query" class="cs-find" type="search" placeholder="Find a column" aria-label="Find a column" />
      <button type="button" class="cs-button" @click="setAll(true)">Open all</button>
      <button type="button" class="cs-button" @click="setAll(false)">Close all</button>
      <span class="cs-legend"><span class="cs-key">◆</span> identifies a row · <span class="cs-link">→</span> row number in another file</span>
    </div>

    <div ref="diagram" class="cs-diagram">
      <svg class="cs-arrows" :width="size.width" :height="size.height" aria-hidden="true">
        <defs>
          <marker id="cs-head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" class="cs-head" />
          </marker>
        </defs>
        <path v-for="(arrow, i) in arrows" :key="i" :d="arrow.d" marker-end="url(#cs-head)"
              :class="['cs-arrow', { on: arrow.files.some((f) => active.has(f)) }]" />
      </svg>

      <div ref="lanesBox" class="cs-lanes" :style="{ gridTemplateColumns: laneWidths() }">
        <div v-for="lane in lanes" :key="lane" class="cs-lane">
          <div v-if="titles[lane]" class="cs-lane-title">{{ titles[lane] }}</div>
          <template v-for="name in layout[lane]" :key="name">
            <section :id="name" :data-file="name"
                     :class="['cs-box', { open: open[name], dim: needle && !rows(files[name]).length }]"
                     @mouseenter="hovered = name" @mouseleave="hovered = ''">
              <button type="button" class="cs-head-row" :aria-expanded="!!open[name]" @click="toggle(name)">
                <span class="cs-file">{{ name }}</span>
                <span class="cs-count">{{ files[name].columns.length }} columns <span class="cs-chevron">{{ open[name] ? "▾" : "▸" }}</span></span>
              </button>
              <p class="cs-row-text">
                {{ files[name].row }}<template v-if="open[name]"> · <code>&lt;stem&gt;.{{ name }}.csv.zip</code> · needs {{ files[name].needs }}</template>
              </p>
              <div v-if="rows(files[name]).length" :class="['cs-table', { full: open[name] || needle }]">
                <template v-for="(column, i) in rows(files[name])" :key="column.name">
                  <div v-if="startsGroup(files[name], rows(files[name]), i)" class="cs-group">
                    <code>{{ column.group }}_*</code> {{ files[name].prefixes[column.group] }}
                  </div>
                  <span :class="['cs-mark', column.key ? 'cs-key' : 'cs-link']">{{ column.key ? "◆" : column.linkFile ? "→" : "" }}</span>
                  <code class="cs-name" :data-column="column.name">{{ column.name }}</code>
                  <span class="cs-text">
                    <template v-if="open[name] || needle">{{ column.text }}<span v-if="column.unit" class="cs-unit-inline"> · {{ column.unit }}</span></template>
                    <a v-if="column.linkFile" class="cs-target" :href="'#' + column.linkFile"
                       @click.prevent="show(column.linkFile)">→ {{ column.linkFile }}</a>
                  </span>
                  <span class="cs-unit">{{ open[name] || needle ? column.unit : "" }}</span>
                </template>
              </div>
              <button v-if="!open[name] && !needle" type="button" class="cs-more" @click="toggle(name)">
                show all {{ files[name].columns.length }} columns
              </button>
            </section>
          </template>
        </div>
      </div>

      <div v-if="band.length" ref="bandBox" class="cs-band">
        <div v-if="titles.bottom" class="cs-lane-title">{{ titles.bottom }}</div>
        <div class="cs-band-grid">
          <section v-for="name in band" :id="name" :key="name" :data-file="name"
                   :class="['cs-box', { open: open[name], dim: needle && !rows(files[name]).length }]"
                   @mouseenter="hovered = name" @mouseleave="hovered = ''">
            <button type="button" class="cs-head-row" :aria-expanded="!!open[name]" @click="toggle(name)">
              <span class="cs-file">{{ name }}</span>
              <span class="cs-count">{{ files[name].columns.length }} columns <span class="cs-chevron">{{ open[name] ? "▾" : "▸" }}</span></span>
            </button>
            <p class="cs-row-text">
              {{ files[name].row }}<template v-if="open[name]"> · <code>&lt;stem&gt;.{{ name }}.csv.zip</code> · needs {{ files[name].needs }}</template>
            </p>
            <div v-if="rows(files[name]).length" :class="['cs-table', { full: open[name] || needle }]">
              <template v-for="(column, i) in rows(files[name])" :key="column.name">
                <div v-if="startsGroup(files[name], rows(files[name]), i)" class="cs-group">
                  <code>{{ column.group }}_*</code> {{ files[name].prefixes[column.group] }}
                </div>
                <span :class="['cs-mark', column.key ? 'cs-key' : 'cs-link']">{{ column.key ? "◆" : column.linkFile ? "→" : "" }}</span>
                <code class="cs-name" :data-column="column.name">{{ column.name }}</code>
                <span class="cs-text">
                  <template v-if="open[name] || needle">{{ column.text }}<span v-if="column.unit" class="cs-unit-inline"> · {{ column.unit }}</span></template>
                  <a v-if="column.linkFile" class="cs-target" :href="'#' + column.linkFile"
                     @click.prevent="show(column.linkFile)">→ {{ column.linkFile }}</a>
                </span>
                <span class="cs-unit">{{ open[name] || needle ? column.unit : "" }}</span>
              </template>
            </div>
            <button v-if="!open[name] && !needle" type="button" class="cs-more" @click="toggle(name)">
              show all {{ files[name].columns.length }} columns
            </button>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.csv-schema {
  margin: 24px 0;
  font-size: 13px;
  line-height: 1.45;
}

.cs-toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px 10px;
  margin-bottom: 16px;
}

.cs-find {
  flex: 0 1 240px;
  min-width: 160px;
  padding: 5px 10px;
  border: 1px solid var(--vp-c-border);
  border-radius: 6px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 13px;
}

.cs-button {
  padding: 4px 10px;
  border: 1px solid var(--vp-c-border);
  border-radius: 6px;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
  font-size: 12px;
}

.cs-button:hover {
  border-color: var(--vp-c-brand-1);
}

.cs-legend {
  color: var(--vp-c-text-2);
  font-size: 12px;
}

.cs-key {
  color: var(--vp-c-brand-1);
}

.cs-link {
  color: var(--vp-c-text-2);
}

.cs-diagram {
  position: relative;
  container: diagram / inline-size;
}

.cs-arrows {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: visible;
}

.cs-arrow {
  fill: none;
  stroke: var(--vp-c-text-3);
  stroke-width: 1.3;
  opacity: 0.55;
  transition: opacity 0.15s, stroke 0.15s;
}

.cs-arrow.on {
  stroke: var(--vp-c-brand-1);
  stroke-width: 1.8;
  opacity: 1;
}

.cs-head {
  fill: var(--vp-c-text-3);
  fill: context-stroke;
}

.cs-lanes {
  position: relative;
  display: grid;
  column-gap: 52px;
  align-items: start;
}

.cs-lane {
  display: flex;
  flex-direction: column;
  gap: 18px;
  min-width: 0;
}

.cs-lane-title {
  color: var(--vp-c-text-2);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.cs-band {
  position: relative;
  margin-top: 56px;
  padding-top: 14px;
  border-top: 1px dashed var(--vp-c-divider);
}

.cs-band-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 18px;
  margin-top: 10px;
  align-items: start;
}

.cs-band-grid .cs-box.open {
  grid-column: 1 / -1;
}

.cs-box {
  position: relative;
  container: box / inline-size;
  min-width: 0;
  border: 1px solid var(--vp-c-border);
  border-radius: 8px;
  background: var(--vp-c-bg);
  scroll-margin-top: calc(var(--vp-nav-height) + 16px);
  transition: opacity 0.15s, border-color 0.15s;
}

.cs-box:hover,
.cs-box.open {
  border-color: var(--vp-c-brand-1);
}

.cs-box.dim {
  opacity: 0.35;
}

.cs-head-row {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 8px;
  width: 100%;
  padding: 7px 10px 3px;
  text-align: left;
  cursor: pointer;
}

.cs-file {
  font-family: var(--vp-font-family-mono);
  font-size: 13px;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.cs-count {
  margin-left: auto;
  color: var(--vp-c-text-3);
  font-size: 11px;
  white-space: nowrap;
}

.cs-count .cs-chevron {
  margin-left: 4px;
  font-size: 13px;
}

.cs-chevron {
  color: var(--vp-c-text-2);
}

.cs-row-text {
  margin: 0;
  padding: 0 10px 6px;
  color: var(--vp-c-text-2);
  font-size: 12px;
}

.cs-row-text code {
  font-size: 11px;
}

.cs-table {
  display: grid;
  grid-template-columns: 14px max-content minmax(0, 1fr) max-content;
  column-gap: 8px;
  padding: 6px 10px 8px;
  border-top: 1px solid var(--vp-c-divider);
}

.cs-table > * {
  padding: 2px 0;
}

.cs-table.full > .cs-name,
.cs-table.full > .cs-text,
.cs-table.full > .cs-unit,
.cs-table.full > .cs-mark {
  border-bottom: 1px solid var(--vp-c-divider);
}

.cs-mark {
  font-size: 11px;
}

.cs-name {
  font-family: var(--vp-font-family-mono);
  font-size: 12px;
  color: var(--vp-c-text-1);
  background: none;
  padding: 2px 0;
}

.cs-text {
  color: var(--vp-c-text-2);
  font-size: 12px;
  min-width: 0;
}

.cs-target {
  margin-left: 4px;
  font-family: var(--vp-font-family-mono);
  font-size: 11.5px;
  white-space: nowrap;
}

.cs-table:not(.full) .cs-target {
  margin-left: 0;
}

.cs-unit {
  color: var(--vp-c-text-3);
  font-size: 11.5px;
  white-space: nowrap;
}

.cs-unit-inline {
  display: none;
  color: var(--vp-c-text-3);
}

.cs-group {
  grid-column: 1 / -1;
  margin-top: 8px;
  padding: 3px 0;
  color: var(--vp-c-text-1);
  font-size: 12px;
  font-weight: 600;
}

.cs-group code {
  font-size: 11.5px;
}

.cs-more {
  display: block;
  width: 100%;
  padding: 4px 10px 7px;
  text-align: left;
  color: var(--vp-c-brand-1);
  font-size: 12px;
  cursor: pointer;
}

.cs-more:hover {
  text-decoration: underline;
}

/* narrow content: one column, no arrows (the → links stay clickable) */
@container diagram (max-width: 760px) {
  .cs-lanes {
    grid-template-columns: minmax(0, 1fr) !important;
    row-gap: 18px;
  }

  .cs-arrows {
    display: none;
  }

  .cs-band {
    margin-top: 28px;
  }
}

/* a narrow open box: the name on its own line, description and unit below it */
@container box (max-width: 440px) {
  .cs-table.full {
    grid-template-columns: 14px minmax(0, 1fr);
  }

  .cs-table.full > .cs-name {
    overflow-wrap: anywhere;
    border-bottom: none;
    padding-top: 6px;
  }

  .cs-table.full > .cs-mark {
    border-bottom: none;
    padding-top: 6px;
  }

  .cs-table.full > .cs-text {
    grid-column: 2;
    padding: 0 0 5px;
  }

  .cs-table.full > .cs-unit {
    display: none;
  }

  .cs-unit-inline {
    display: inline;
  }
}
</style>
