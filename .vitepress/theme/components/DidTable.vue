<template>
  <div class="did-table">
    <div class="did-table-toolbar">
      <button
        class="did-btn did-btn-copy-all"
        :class="{ 'is-copied': copiedAll }"
        @click="copyAll"
        :title="`Copy all ${rows.length} DIDs (newline-separated)`"
      >
        <span v-if="copiedAll">✓ Copied {{ rows.length }} DID{{ rows.length === 1 ? '' : 's' }}</span>
        <span v-else>📋 Copy all ({{ rows.length }})</span>
      </button>
      <button
        v-if="hasMixedKinds"
        class="did-btn did-btn-secondary"
        :class="{ 'is-copied': copiedKind === 'FULL' }"
        @click="copyKind('FULL')"
        :title="`Copy ${countByKind.FULL} FULL DIDs`"
      >
        <span v-if="copiedKind === 'FULL'">✓</span>
        <span v-else>FULL only ({{ countByKind.FULL }})</span>
      </button>
      <button
        v-if="hasMixedKinds"
        class="did-btn did-btn-secondary"
        :class="{ 'is-copied': copiedKind === 'RECO' }"
        @click="copyKind('RECO')"
        :title="`Copy ${countByKind.RECO} RECO DIDs`"
      >
        <span v-if="copiedKind === 'RECO'">✓</span>
        <span v-else>RECO only ({{ countByKind.RECO }})</span>
      </button>
    </div>
    <table class="did-table-grid">
      <thead>
        <tr>
          <th class="col-copy"></th>
          <th class="col-kind">Kind</th>
          <th v-if="hasEnergy" class="col-energy">Beam</th>
          <th class="col-did">Rucio DID</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(row, i) in rows"
          :key="i"
          :class="['did-row', `did-row-${(row.kind || '').toLowerCase()}`]"
        >
          <td class="col-copy">
            <button
              class="did-btn did-btn-icon"
              :class="{ 'is-copied': copiedIndex === i }"
              :title="`Copy ${row.did}`"
              @click="copyOne(i, row.did)"
            >
              <span v-if="copiedIndex === i">✓</span>
              <span v-else>📋</span>
            </button>
          </td>
          <td class="col-kind">
            <span :class="['did-kind', `did-kind-${(row.kind || '').toLowerCase()}`]">
              {{ row.kind }}
            </span>
          </td>
          <td v-if="hasEnergy" class="col-energy">
            <code v-if="row.energy" class="did-energy">{{ row.energy }}</code>
          </td>
          <td class="col-did">
            <code class="did-code">{{ row.did }}</code>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  rows: {
    type: Array,
    required: true,
    // each row: { did: string, kind: 'FULL'|'RECO', energy?: string }
  }
});

const copiedIndex = ref(-1);
const copiedAll = ref(false);
const copiedKind = ref('');

const hasEnergy = computed(() => props.rows.some(r => r.energy));
const countByKind = computed(() => {
  const c = { FULL: 0, RECO: 0 };
  for (const r of props.rows) {
    if (r.kind === 'FULL' || r.kind === 'RECO') c[r.kind] += 1;
  }
  return c;
});
const hasMixedKinds = computed(() => countByKind.value.FULL > 0 && countByKind.value.RECO > 0);

async function writeClipboard(text) {
  // Prefer the async clipboard API; fall back to execCommand for old browsers / Safari.
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (_) {
    try {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      return true;
    } catch (_) {
      return false;
    }
  }
}

async function copyOne(i, did) {
  const ok = await writeClipboard(did);
  if (!ok) return;
  copiedIndex.value = i;
  setTimeout(() => {
    if (copiedIndex.value === i) copiedIndex.value = -1;
  }, 1600);
}

async function copyAll() {
  const text = props.rows.map(r => r.did).join('\n');
  const ok = await writeClipboard(text);
  if (!ok) return;
  copiedAll.value = true;
  setTimeout(() => { copiedAll.value = false; }, 1600);
}

async function copyKind(kind) {
  const text = props.rows.filter(r => r.kind === kind).map(r => r.did).join('\n');
  const ok = await writeClipboard(text);
  if (!ok) return;
  copiedKind.value = kind;
  setTimeout(() => {
    if (copiedKind.value === kind) copiedKind.value = '';
  }, 1600);
}
</script>

<style scoped>
.did-table {
  margin: 0.75em 0 1.5em;
}

.did-table-toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4em;
  margin-bottom: 0.4em;
}

.did-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.25em;
  font-family: var(--vp-font-family-base);
  font-size: 0.8em;
  font-weight: 500;
  line-height: 1;
  padding: 4px 10px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 4px;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;
}
.did-btn:hover {
  background: var(--vp-c-bg-mute);
  border-color: var(--vp-c-brand);
}
.did-btn.is-copied {
  background: #16a34a;
  border-color: #16a34a;
  color: #fff;
}

.did-btn-copy-all {
  font-weight: 600;
}
.did-btn-secondary {
  font-weight: 400;
}

.did-btn-icon {
  padding: 2px 6px;
  font-size: 0.9em;
}

.did-table-grid {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85em;
  table-layout: auto;
}

.did-table-grid thead th {
  text-align: left;
  font-weight: 600;
  padding: 6px 8px;
  border-bottom: 2px solid var(--vp-c-divider);
  background: var(--vp-c-bg-soft);
  font-size: 0.85em;
  color: var(--vp-c-text-2);
}

.did-table-grid tbody td {
  padding: 4px 8px;
  border-bottom: 1px solid var(--vp-c-divider);
  vertical-align: middle;
}

.did-row-full {
  background: var(--vp-c-bg);
}
.did-row-reco {
  background: var(--vp-c-bg-soft);
}

.col-copy { width: 36px; text-align: center; }
.col-kind { width: 64px; }
.col-energy { width: 80px; white-space: nowrap; }
.col-did { word-break: break-all; }

.did-kind {
  display: inline-block;
  padding: 1px 6px;
  border-radius: 3px;
  font-size: 0.75em;
  font-weight: 700;
  letter-spacing: 0.02em;
}
.did-kind-full {
  background: #3f51b5;
  color: #fff;
}
.did-kind-reco {
  background: #16a34a;
  color: #fff;
}

.did-code {
  font-family: var(--vp-font-family-mono);
  font-size: 0.85em;
  background: transparent;
  padding: 0;
  word-break: break-all;
}

.did-energy {
  font-family: var(--vp-font-family-mono);
  font-size: 0.85em;
  background: var(--vp-c-bg-mute);
  padding: 1px 5px;
  border-radius: 3px;
}
</style>
