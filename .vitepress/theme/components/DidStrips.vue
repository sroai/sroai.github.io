<script>
/*
 * DidStrips.vue — declarative, hand-authored dataset strips for VitePress.
 *
 * Nothing is parsed. Every tag (label, colour, tooltip) is set by hand in
 * Markdown. `didpath` is shown verbatim as the copyable prefix line; <Dids>
 * is the literal list rendered in the expandable table. FULL/RECO counts are
 * a simple substring count of the <Dids> lines (not tag inference).
 *
 * Authoring (Option B — grouped by colour):
 *
 *   <DidStrips didpath="epic:/{FULL|RECO}/26.04.1/.../DIS/NC/"
 *              version="26.04.1" name="Bkg_Exact1S_2us">
 *     <Tags color="violet" desc="Physics process">
 *       <Tag desc="Deep Inelastic Scattering">DIS</Tag>
 *       <Tag desc="Neutral current">NC</Tag>
 *     </Tags>
 *     <Tags color="sky" desc="Beam energy">
 *       <Tag>10x100</Tag><Tag>10x275</Tag>
 *     </Tags>
 *     <Tags color="amber" desc="Minimum Q2">
 *       <Tag>minQ2=1</Tag><Tag>minQ2=10</Tag><Tag>minQ2=100</Tag><Tag>minQ2=1000</Tag>
 *     </Tags>
 *     <More color="slate">
 *       <Tag desc="Generator: MadGraph5 v3.7.0">madgraph5-3.7.0-1.0</Tag>
 *     </More>
 *     <Dids>
 *   epic:/FULL/26.04.1/.../10x100/minQ2=1
 *   epic:/RECO/26.04.1/.../10x100/minQ2=1
 *     </Dids>
 *   </DidStrips>
 *
 * Register all five in .vitepress/theme/index.ts (see README).
 */
import { defineComponent, ref, computed, useSlots, Comment } from 'vue';

// ---- child markers: identifiable, render nothing (parent never mounts them) ----
const marker = (name, kind) =>
  defineComponent({ name, __ds: kind, render: () => null });

export const Tags = marker('Tags', 'group'); // colour group of <Tag> chips (main row)
export const Tag  = marker('Tag',  'tag');   // one chip: text = label, props: desc, color/bg
export const More = marker('More',  'more');  // colour group shown under "Additional info"
export const Dids = marker('Dids',  'dids');  // literal DID list (one per line)

// ---- named colours -> hex (or pass a raw #hex / any CSS colour) ----
const PALETTE = {
  violet: '#7c3aed', sky: '#0369a1', amber: '#b45309', slate: '#475569',
  green: '#15803d', indigo: '#4f46e5', teal: '#0f766e', rose: '#be123c',
  fuchsia: '#a21caf', gray: '#78716c', grey: '#78716c', blue: '#2563eb',
  red: '#dc2626', orange: '#ea580c',
};
const hueOf = (c) => (c ? (PALETTE[c] || c) : '#78716c');

export default defineComponent({
  name: 'DidStrips',
  props: {
    didpath: { type: String, default: '' },
    csvpath: { type: String, default: '' }, // XRootD path to the converted CSVs (optional)
    version: { type: String, default: '' },
    name:    { type: String, default: '' },
    open:    { type: Boolean, default: false }, // start expanded
  },
  setup(props) {
    const slots  = useSlots();
    const isOpen = ref(props.open);
    const copied = ref('');
    const tip    = ref({ show: false, text: '', x: 0, y: 0 });

    // ---- vnode helpers -------------------------------------------------
    const dsKind = (v) => (v && v.type && v.type.__ds) || null;

    function childrenOf(vnode) {
      const c = vnode && vnode.children;
      if (c == null) return [];
      if (Array.isArray(c)) return c;
      if (typeof c === 'string') return [c];
      if (typeof c === 'object' && typeof c.default === 'function') return c.default();
      return [];
    }
    // flat array of all text leaves under a vnode
    function leaves(vnode, out = []) {
      if (vnode == null) return out;
      if (typeof vnode === 'string') { out.push(vnode); return out; }
      if (Array.isArray(vnode)) { vnode.forEach((n) => leaves(n, out)); return out; }
      if (typeof vnode !== 'object' || vnode.type === Comment) return out;
      if (typeof vnode.children === 'string') { out.push(vnode.children); return out; }
      childrenOf(vnode).forEach((n) => leaves(n, out));
      return out;
    }
    const textOf = (vnode) => leaves(vnode).join('').replace(/\s+/g, ' ').trim();

    // collect marker vnodes of given kinds, descending through wrappers (<p>, fragments)
    function collect(nodes, kinds, acc = []) {
      for (const n of nodes || []) {
        if (!n || typeof n !== 'object') continue;
        if (kinds.includes(dsKind(n))) { acc.push(n); continue; }
        const kids = childrenOf(n);
        if (kids.length) collect(kids, kinds, acc);
      }
      return acc;
    }

    // ---- authored model (fully explicit) -------------------------------
    const model = computed(() => {
      const top = collect(slots.default ? slots.default() : [], ['group', 'more', 'dids']);
      const main = [];   // main-row chips
      const more = [];   // additional-info chips
      let dids = [];

      for (const node of top) {
        const kind = dsKind(node);
        if (kind === 'group' || kind === 'more') {
          const gp = node.props || {};
          const gColor = gp.color || gp.bg;
          const gDesc  = gp.desc;
          const bucket = kind === 'group' ? main : more;
          for (const t of collect(childrenOf(node), ['tag'])) {
            const p = t.props || {};
            const label = textOf(t);
            if (!label) continue;
            bucket.push({
              label,
              desc: p.desc || gDesc || '',
              hue: hueOf(p.color || p.bg || gColor),
            });
          }
        } else if (kind === 'dids') {
          // a DID never contains whitespace, so split on any whitespace —
          // robust whether newlines survive markdown / template compilation or not.
          dids = leaves(node).join(' ').split(/\s+/).map((s) => s.trim()).filter(Boolean);
        }
      }

      const full = dids.filter((d) => d.includes('/FULL/')).length;
      const reco = dids.filter((d) => d.includes('/RECO/')).length;
      return { main, more, dids, full, reco };
    });

    // ---- styling -------------------------------------------------------
    function chip(hue, mono = true) {
      return {
        color: hue,
        background: `color-mix(in srgb, ${hue} 11%, var(--vp-c-bg))`,
        borderColor: `color-mix(in srgb, ${hue} 32%, var(--vp-c-bg))`,
        fontFamily: mono ? 'var(--vp-font-family-mono)' : 'var(--vp-font-family-base)',
      };
    }
    const kindHue = (k) => (k === 'FULL' ? '#4f46e5' : '#15803d');

    // ---- clipboard -----------------------------------------------------
    async function writeClip(text) {
      try { await navigator.clipboard.writeText(text); return true; }
      catch (_) {
        try {
          const ta = document.createElement('textarea');
          ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
          document.body.appendChild(ta); ta.select();
          document.execCommand('copy'); document.body.removeChild(ta);
          return true;
        } catch (_) { return false; }
      }
    }
    let flashTimer;
    function flash(key) {
      copied.value = key;
      clearTimeout(flashTimer);
      flashTimer = setTimeout(() => { if (copied.value === key) copied.value = ''; }, 1500);
    }
    const copyAll    = () => { writeClip(model.value.dids.join('\n')); flash('all'); };
    const copyRow    = (i) => { writeClip(model.value.dids[i]); flash('row' + i); };
    const copyPrefix = () => { writeClip(props.didpath); flash('prefix'); };
    const copyCsv    = () => { writeClip(props.csvpath); flash('csv'); };

    // ---- tooltip -------------------------------------------------------
    function showTip(e, text) { if (!text) return; tip.value = { show: true, text, x: e.clientX, y: e.clientY }; }
    function hideTip() { tip.value = { ...tip.value, show: false }; }

    const toggle = () => { isOpen.value = !isOpen.value; };

    return {
      props, isOpen, copied, tip, model,
      chip, kindHue, hueOf,
      copyAll, copyRow, copyPrefix, copyCsv, showTip, hideTip, toggle,
    };
  },
});
</script>

<template>
  <div class="did-strips">
    <div class="ds-strip">
      <!-- header -->
      <div class="ds-head" @click="toggle">
        <span class="ds-chev" :class="{ open: isOpen }">&#9656;</span>

        <div class="ds-head-main">
          <div class="ds-row">
            <span v-if="props.version" class="ds-chip ds-version">{{ props.version }}</span>
            <span
              v-if="props.name"
              class="ds-chip"
              :style="chip('#0f766e')"
            >{{ props.name }}</span>
            <span
              v-if="model.full"
              class="ds-chip ds-kind"
              :style="chip(kindHue('FULL'), false)"
              @mouseenter="showTip($event, 'FULL — DD4hep full Geant4 simulation (sim-level)')"
              @mouseleave="hideTip"
            >FULL&nbsp;&middot;{{ model.full }}</span>
            <span
              v-if="model.reco"
              class="ds-chip ds-kind"
              :style="chip(kindHue('RECO'), false)"
              @mouseenter="showTip($event, 'RECO — EICrecon reconstruction output (reco-level)')"
              @mouseleave="hideTip"
            >RECO&nbsp;&middot;{{ model.reco }}</span>
          </div>

          <div class="ds-row" v-if="model.main.length">
            <span
              v-for="(t, i) in model.main"
              :key="'m' + i"
              class="ds-chip ds-hoverable"
              :style="chip(t.hue)"
              @mouseenter="showTip($event, t.desc)"
              @mouseleave="hideTip"
            >{{ t.label }}</span>
          </div>

          <div
            v-if="props.didpath"
            class="ds-prefix"
            :class="{ copied: copied === 'prefix' }"
            @click.stop="copyPrefix"
            title="Click to copy the DID prefix"
          >
            <span class="ds-prefix-ico">{{ copied === 'prefix' ? '&#10003;' : '&#128203;' }}</span>
            <code class="ds-prefix-txt">{{ props.didpath }}</code>
            <span class="ds-prefix-hint">{{ copied === 'prefix' ? 'Copied' : 'Copy prefix' }}</span>
          </div>

          <div
            v-if="props.csvpath"
            class="ds-prefix ds-csv"
            :class="{ copied: copied === 'csv' }"
            @click.stop="copyCsv"
            title="Click to copy the XRootD path to the converted CSVs"
          >
            <span class="ds-prefix-ico">{{ copied === 'csv' ? '&#10003;' : '&#128203;' }}</span>
            <span class="ds-csv-badge">CSV</span>
            <code class="ds-prefix-txt">{{ props.csvpath }}</code>
            <span class="ds-prefix-hint">{{ copied === 'csv' ? 'Copied' : 'Copy CSV path' }}</span>
          </div>
        </div>

        <div class="ds-actions" v-if="model.dids.length">
          <button class="ds-btn ds-btn-copy" :class="{ ok: copied === 'all' }" @click.stop="copyAll">
            <span v-if="copied === 'all'">&#10003; Copied {{ model.dids.length }}</span>
            <span v-else>&#128203; Copy all ({{ model.dids.length }})</span>
          </button>
          <button class="ds-btn ds-btn-toggle" :class="{ open: isOpen }" @click.stop="toggle">
            <span v-if="isOpen">Hide DIDs &#8963;</span>
            <span v-else>Show {{ model.dids.length }} DIDs &#8964;</span>
          </button>
        </div>
      </div>

      <!-- expanded -->
      <div class="ds-body" v-if="isOpen">
        <div class="ds-more" v-if="model.more.length">
          <div class="ds-more-label">Additional info</div>
          <div class="ds-row">
            <span
              v-for="(t, i) in model.more"
              :key="'a' + i"
              class="ds-chip ds-hoverable"
              :style="chip(t.hue)"
              @mouseenter="showTip($event, t.desc)"
              @mouseleave="hideTip"
            >{{ t.label }}</span>
          </div>
        </div>

        <div class="ds-table" v-if="model.dids.length">
          <div class="ds-tr" v-for="(did, i) in model.dids" :key="'d' + i">
            <button class="ds-copy" :class="{ ok: copied === 'row' + i }" @click="copyRow(i)" :title="'Copy ' + did">
              <span v-if="copied === 'row' + i">&#10003;</span>
              <span v-else>&#128203;</span>
            </button>
            <code class="ds-did">{{ did }}</code>
          </div>
        </div>
      </div>
    </div>

    <!-- floating tooltip -->
    <div
      v-if="tip.show"
      class="ds-tip"
      :style="{ left: Math.min(tip.x + 14, (typeof window !== 'undefined' ? window.innerWidth : 1200) - 312) + 'px', top: (tip.y + 16) + 'px' }"
    >{{ tip.text }}</div>
  </div>
</template>

<style scoped>
.did-strips { margin: 0.75em 0 1.5em; }

.ds-strip {
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
  overflow: hidden;
}

.ds-head {
  display: flex;
  align-items: flex-start;
  gap: 13px;
  padding: 16px 18px;
  cursor: pointer;
}
.ds-head:hover { background: var(--vp-c-bg-soft); }

.ds-chev {
  flex: none;
  font-size: 12px;
  color: var(--vp-c-text-3);
  margin-top: 5px;
  transition: transform 0.18s ease;
}
.ds-chev.open { transform: rotate(90deg); }

.ds-head-main { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 9px; }
.ds-row { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }

.ds-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.3em;
  padding: 2px 9px;
  border-radius: 6px;
  border: 1px solid transparent;
  font-size: 12.5px;
  font-weight: 600;
  line-height: 1.5;
  white-space: nowrap;
}
.ds-hoverable, .ds-kind { cursor: help; }
.ds-version {
  background: #334155 !important;
  color: #fff;
  border-color: #334155;
  font-family: var(--vp-font-family-mono);
}

.ds-prefix {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  align-self: flex-start;
  max-width: 100%;
  padding: 4px 9px;
  border-radius: 6px;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  cursor: pointer;
}
.ds-prefix:hover { background: var(--vp-c-bg-mute); }
.ds-prefix.copied { border-color: #16a34a; }
.ds-prefix-ico { font-size: 10px; color: var(--vp-c-text-3); flex: none; }
.ds-prefix-txt {
  font-family: var(--vp-font-family-mono);
  font-size: 10px;
  color: var(--vp-c-text-2);
  line-height: 1.45;
  word-break: break-all;
  background: transparent;
  padding: 0;
}
.ds-prefix-hint {
  flex: none;
  font-family: var(--vp-font-family-mono);
  font-size: 9px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--vp-c-text-3);
}

/* converted-CSV path line: same layout as the DID prefix, with a CSV badge */
.ds-csv-badge {
  flex: none;
  font-family: var(--vp-font-family-mono);
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #ea580c;
  background: color-mix(in srgb, #ea580c 11%, var(--vp-c-bg));
  border: 1px solid color-mix(in srgb, #ea580c 32%, var(--vp-c-bg));
  border-radius: 4px;
  padding: 1px 5px;
}
.ds-csv.copied { border-color: #16a34a; }

.ds-actions { display: flex; flex-direction: column; gap: 8px; flex: none; }
.ds-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.3em;
  font-family: var(--vp-font-family-base);
  font-size: 12.5px;
  font-weight: 600;
  line-height: 1;
  padding: 7px 13px;
  border-radius: 8px;
  border: 1px solid var(--vp-c-divider);
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;
}
.ds-btn-copy { background: var(--vp-c-bg-soft); color: var(--vp-c-text-1); border-radius: 7px; }
.ds-btn-copy:hover { border-color: var(--vp-c-brand-1); }
.ds-btn-toggle { background: var(--vp-c-bg); color: var(--vp-c-text-1); }
.ds-btn-toggle:hover { border-color: var(--vp-c-brand-1); }
.ds-btn-toggle.open { background: #334155; color: #fff; border-color: #334155; }
.ds-btn.ok { background: #16a34a !important; border-color: #16a34a; color: #fff; }

.ds-body {
  border-top: 1px solid var(--vp-c-divider);
  padding: 15px 18px 18px;
  background: var(--vp-c-bg-soft);
}
.ds-more { margin-bottom: 15px; }
.ds-more-label {
  font-family: var(--vp-font-family-mono);
  font-size: 10.5px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  color: var(--vp-c-text-3);
  margin-bottom: 9px;
}

.ds-table {
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  overflow: hidden;
  background: var(--vp-c-bg);
}
.ds-tr {
  display: grid;
  grid-template-columns: 34px minmax(0, 1fr);
  gap: 11px;
  align-items: center;
  padding: 6px 10px;
}
.ds-tr + .ds-tr { border-top: 1px solid var(--vp-c-divider); }
.ds-copy {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 24px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  color: var(--vp-c-text-2);
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  padding: 0;
}
.ds-copy:hover { border-color: var(--vp-c-brand-1); }
.ds-copy.ok { background: #16a34a; border-color: #16a34a; color: #fff; }
.ds-did {
  font-family: var(--vp-font-family-mono);
  font-size: 11.5px;
  color: var(--vp-c-text-2);
  word-break: break-all;
  line-height: 1.45;
  background: transparent;
  padding: 0;
}

.ds-tip {
  position: fixed;
  z-index: 100;
  pointer-events: none;
  max-width: 300px;
  background: #1f2430;
  color: #fff;
  padding: 8px 11px;
  border-radius: 8px;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.28);
  font-size: 12.5px;
  line-height: 1.4;
}
</style>
