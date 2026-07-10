<template>
  <div class="tool-compare">
    <!-- 工具选择区 -->
    <div class="compare-header">
      <h3 class="compare-title">🔍 工具对比</h3>
      <p class="compare-desc">选择多个工具进行横向对比，找到最适合你的AI助手</p>
      
      <div class="tool-selector">
        <n-select
          v-model:value="selectedIds"
          multiple
          :options="toolOptions"
          placeholder="选择要对比的工具（最多5个）"
          :max-tag-count="5"
          @update:value="onSelectionChange"
        />
      </div>
    </div>

    <!-- 对比表格 -->
    <div v-if="selectedTools.length >= 2" class="compare-table-wrap">
      <table class="compare-table">
        <thead>
          <tr>
            <th class="dim-col">对比维度</th>
            <th v-for="tool in selectedTools" :key="tool.id" class="tool-col">
              <div class="tool-header">
                <div class="tool-logo">{{ tool.name.charAt(0) }}</div>
                <div class="tool-name">{{ tool.name }}</div>
                <n-badge 
                  :type="availabilityType(tool.availability?.status)" 
                  size="small" 
                  style="margin-top:4px"
                >
                  {{ availabilityLabel(tool.availability?.status) }}
                </n-badge>
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <!-- 定价行 -->
          <tr>
            <td class="dim-cell">💰 定价</td>
            <td v-for="tool in selectedTools" :key="'price-'+tool.id" class="val-cell">
              <span class="price-text">{{ tool.pricing?.price_from || '免费' }}</span>
              <span class="price-type">{{ pricingLabel(tool.pricing?.type) }}</span>
            </td>
          </tr>
          <!-- 可用性行 -->
          <tr>
            <td class="dim-cell">🌏 国内可用性</td>
            <td v-for="tool in selectedTools" :key="'avail-'+tool.id" class="val-cell">
              <span 
                class="avail-badge" 
                :class="tool.availability?.status || 'uncertain'"
              >
                {{ availabilityLabel(tool.availability?.status) }}
              </span>
              <div v-if="tool.availability?.access_method" class="access-method">
                {{ tool.availability.access_method }}
              </div>
            </td>
          </tr>
          <!-- 使用难度 -->
          <tr>
            <td class="dim-cell">📚 使用难度</td>
            <td v-for="tool in selectedTools" :key="'diff-'+tool.id" class="val-cell">
              <span class="diff-badge" :class="tool.difficulty || 'beginner'">
                {{ difficultyLabel(tool.difficulty) }}
              </span>
            </td>
          </tr>
          <!-- 平台支持 -->
          <tr>
            <td class="dim-cell">📱 支持平台</td>
            <td v-for="tool in selectedTools" :key="'plat-'+tool.id" class="val-cell">
              <div class="platform-tags">
                <span v-if="tool.platforms?.includes('web')" class="plat-tag">Web</span>
                <span v-if="tool.platforms?.includes('ios')" class="plat-tag">iOS</span>
                <span v-if="tool.platforms?.includes('android')" class="plat-tag">Android</span>
                <span v-if="tool.platforms?.includes('api')" class="plat-tag">API</span>
                <span v-if="tool.platforms?.includes('desktop')" class="plat-tag">桌面端</span>
                <span v-if="!tool.platforms?.length" class="plat-tag dim">-</span>
              </div>
            </td>
          </tr>
          <!-- API支持 -->
          <tr>
            <td class="dim-cell">🔌 API接口</td>
            <td v-for="tool in selectedTools" :key="'api-'+tool.id" class="val-cell">
              <span v-if="tool.api_available" class="api-yes">✅ 提供API</span>
              <span v-else class="api-no">❌ 无API</span>
            </td>
          </tr>
          <!-- 免费层 -->
          <tr>
            <td class="dim-cell">🆓 免费层</td>
            <td v-for="tool in selectedTools" :key="'free-'+tool.id" class="val-cell">
              <template v-if="tool.pricing?.has_free_tier">
                <span class="free-yes">✅ 有免费额度</span>
                <div v-if="tool.free_tier_limits" class="free-limit">{{ tool.free_tier_limits }}</div>
              </template>
              <span v-else class="free-no">❌ 无免费层</span>
            </td>
          </tr>
          <!-- 评分 -->
          <tr>
            <td class="dim-cell">⭐ 用户评分</td>
            <td v-for="tool in selectedTools" :key="'rate-'+tool.id" class="val-cell">
              <div class="rating-wrap">
                <span class="rating-num">{{ tool.rating || '-' }}</span>
                <span class="rating-count">({{ tool.rating_count || 0 }}评)</span>
              </div>
            </td>
          </tr>
          <!-- 最适合场景 -->
          <tr>
            <td class="dim-cell">🎯 最适合</td>
            <td v-for="tool in selectedTools" :key="'best-'+tool.id" class="val-cell best-for">
              {{ tool.best_for || '-' }}
            </td>
          </tr>
          <!-- 核心功能对比（动态） -->
          <tr v-for="(feat, fi) in allFeatures" :key="'feat-'+fi">
            <td class="dim-cell feat-cell">
              <span v-if="isFeatureSupported(feat)" class="feat-supported">✅</span>
              <span v-else class="feat-unsupported">⬜</span>
              {{ feat }}
            </td>
            <td v-for="tool in selectedTools" :key="'fval-'+tool.id+'-'+fi" class="val-cell">
              <span v-if="hasFeature(tool, feat)" class="feat-yes">✅</span>
              <span v-else class="feat-no">—</span>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 操作栏 -->
      <div class="compare-actions">
        <n-button type="primary" @click="$router.push(`/tools/${firstToolSlug}`)">
          查看第一个工具详情
        </n-button>
        <n-button @click="clearSelection">清空对比</n-button>
      </div>
    </div>

    <!-- 未选够提示 -->
    <div v-else class="compare-empty">
      <div class="empty-icon">📊</div>
      <p>请至少选择 2 个工具开始对比</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { NSelect, NBadge, NButton } from 'naive-ui'

const props = defineProps({
  tools: { type: Array, default: () => [] }
})

const emit = defineEmits(['compare'])

const selectedIds = ref([])

const toolOptions = computed(() => props.tools.map(t => ({
  label: t.name,
  value: t.id,
  disabled: selectedIds.value.length >= 5 && !selectedIds.value.includes(t.id)
})))

const selectedTools = computed(() =>
  props.tools.filter(t => selectedIds.value.includes(t.id))
)

const firstToolSlug = computed(() =>
  selectedTools.value[0]?.slug || ''
)

// 收集所有功能并集
const allFeatures = computed(() => {
  const feats = new Set()
  props.tools
    .filter(t => selectedIds.value.includes(t.id))
    .forEach(t => (t.features || []).forEach(f => feats.add(f)))
  return [...feats]
})

function isFeatureSupported(feat) {
  return selectedTools.value.some(t => (t.features || []).includes(feat))
}

function hasFeature(tool, feat) {
  return (tool.features || []).includes(feat)
}

function onSelectionChange(ids) {
  if (ids.length > 5) {
    ids = ids.slice(0, 5)
  }
  selectedIds.value = ids
}

function clearSelection() {
  selectedIds.value = []
}

// --- 标签映射函数 ---

function availabilityType(status) {
  const map = { available: 'success', restricted: 'warning', blocked: 'error',
               needs_vpn: 'warning', uncertain: 'default', enterprise_only: 'info' }
  return map[status] || 'default'
}

function availabilityLabel(status) {
  const map = { available: '国内可用', restricted: '部分受限', blocked: '已被封禁',
               needs_vpn: '需VPN', uncertain: '待核实', enterprise_only: '仅企业版' }
  return map[status] || status || '未知'
}

function pricingLabel(type) {
  const map = { freemium: '免费增值', free_tier: '有免费额', paid: '付费',
               open_source: '开源可部署', custom: '企业定制' }
  return map[type] || type || ''
}

function difficultyLevel(d) {
  const map = { beginner: 1, intermediate: 2, advanced: 3 }
  return map[d] || 1
}

function difficultyLabel(d) {
  const map = { beginner: '新手友好 ⭐', intermediate: '需基础 ⭐⭐', advanced: '专业级 ⭐⭐⭐' }
  return map[d] || d || ''
}
</script>

<style scoped>
.tool-compare { background: var(--bg-card); border-radius: 16px; padding: 24px; border: 1px solid #e2e8f0; }
.compare-header { margin-bottom: 24px; }
.compare-title { font-size: 1.25rem; font-weight: 700; margin-bottom: 4px; color: var(--text-primary); }
.compare-desc { font-size: 0.9rem; color: var(--text-tertiary); margin-bottom: 16px; }
.tool-selector { max-width: 500px; }

.compare-table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; }
.compare-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; min-width: 600px; }
.compare-table th { background: #f8fafc; padding: 14px 12px; text-align: left; font-weight: 600; border-bottom: 2px solid #e2e8f0; position: sticky; top: 0; z-index: 1; }
.compare-table td { padding: 12px; border-bottom: 1px solid #f1f5f9; vertical-align: top; }
.compare-table tr:hover td { background: #fafbfc; }

.dim-col { width: 140px; min-width: 140px; }
.dim-cell { font-weight: 600; color: var(--text-secondary); white-space: nowrap; }
.feat-cell { font-weight: 400; }
.feat-supported { color: #10b981; margin-right: 4px; }
.feat-unsupported { color: #d1d5db; margin-right: 4px; }

.tool-col { min-width: 160px; text-align: center; }
.tool-header { display: flex; flex-direction: column; align-items: center; gap: 6px; }
.tool-logo { width: 40px; height: 40px; border-radius: 10px; background: linear-gradient(135deg, #6366f1, #8b5cf6); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1.1rem; }
.tool-name { font-weight: 700; font-size: 0.95rem; color: var(--text-primary); }

.val-cell { text-align: center; font-size: 0.85rem; }

/* 可用性 */
.avail-badge { display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 600; }
.avail-badge.available { background: #dcfce7; color: #166534; }
.avail-badge.restricted { background: #fef3c7; color: #92400e; }
.avail-badge.blocked { background: #fee2e2; color: #991b1b; }
.avail-badge.needs_vpn { background: #e0e7ff; color: #3730a3; }
.avail-badge.uncertain { background: #f1f5f9; color: #64748b; }
.avail-badge.enterprise_only { background: #ede9fe; color: #6b21a8; }
.access-method { font-size: 0.75rem; color: #94a3b8; margin-top: 2px; }

/* 难度 */
.diff-badge { display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 0.8rem; }
.diff-badge.beginner { background: #dcfce7; color: #166534; }
.diff-badge.intermediate { background: #fef3c7; color: #92400e; }
.diff-badge.advanced { background: #fee2e2; color: #991b1b; }

/* 平台 */
.platform-tags { display: flex; gap: 4px; flex-wrap: wrap; justify-content: center; }
.plat-tag { padding: 2px 8px; border-radius: 6px; background: #f1f5f9; font-size: 0.75rem; color: #475569; }
.plat-tag.dim { opacity: 0.4; }

/* API */
.api-yes { color: #10b981; font-weight: 600; }
.api-no { color: #94a3b8; }

/* 免费 */
.free-yes { color: #10b981; font-weight: 600; }
.free-no { color: #94a3b8; }
.free-limit { font-size: 0.75rem; color: #94a3b8; margin-top: 2px; }

/* 评分 */
.rating-wrap { display: flex; flex-direction: column; align-items: center; gap: 2px; }
.rating-num { font-size: 1.25rem; font-weight: 700; color: #f59e0b; }
.rating-count { font-size: 0.75rem; color: #94a3b8; }

/* 最适合 */
.best-for { font-size: 0.82rem; color: var(--text-secondary); line-height: 1.4; }

/* 功能对比 */
.feat-yes { color: #10b981; font-weight: 700; font-size: 0.95rem; }
.feat-no { color: #d1d5db; }

/* 操作栏 */
.compare-actions { display: flex; gap: 12px; margin-top: 20px; justify-content: center; padding-top: 16px; border-top: 1px solid #f1f5f9; }

/* 空状态 */
.compare-empty { text-align: center; padding: 48px 24px; color: #94a3b8; }
.empty-icon { font-size: 3rem; margin-bottom: 12px; }

@media (max-width: 767px) {
  .tool-compare { padding: 16px; }
  .compare-table { font-size: 0.82rem; }
  .compare-table th, .compare-table td { padding: 10px 8px; }
  .dim-col { width: 100px; min-width: 100px; }
}
</style>
