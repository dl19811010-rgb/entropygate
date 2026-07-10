<template>
  <div class="skeleton-card" :class="{ compact }">
    <!-- 封面区域 -->
    <div class="skeleton-cover">
      <div class="skeleton-shine"></div>
    </div>
    <!-- 内容区域 -->
    <div class="skeleton-body">
      <div class="skeleton-line title"></div>
      <div class="skeleton-line subtitle"></div>
      <div class="skeleton-line meta short"></div>
      <div v-if="!compact" class="skeleton-line tag"></div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  compact: { type: Boolean, default: false }
})
</script>

<style scoped>
.skeleton-card {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: #fff;
  border-radius: 12px;
  border: 1px solid #f1f5f9;
}
.skeleton-card.compact {
  flex-direction: column;
  gap: 12px;
  padding: 12px;
}
.skeleton-cover {
  flex-shrink: 0;
  width: 160px;
  height: 90px;
  border-radius: 8px;
  background: linear-gradient(110deg, #e2e8f0 8%, #f1f5f9 18%, #e2e8f0 33%);
  background-size: 200% 100%;
  overflow: hidden;
  position: relative;
}
.compact .skeleton-cover {
  width: 100%;
  height: 140px;
}
.skeleton-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 4px 0;
}
.skeleton-line {
  height: 14px;
  background: linear-gradient(110deg, #e2e8f0 8%, #f1f5f9 18%, #e2e8f0 33%);
  background-size: 200% 100%;
  border-radius: 6px;
  animation: skeleton-shimmer 1.5s infinite;
}
.skeleton-line.title {
  width: 85%;
  height: 18px;
}
.skeleton-line.subtitle {
  width: 100%;
  height: 14px;
}
.skeleton-line.meta {
  width: 50%;
  height: 12px;
  align-self: flex-start;
}
.skeleton-line.tag {
  width: 30%;
  height: 22px;
  margin-top: auto;
  align-self: flex-start;
}
@keyframes skeleton-shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
/* 懒加载完成后的过渡 */
.lazy-img, .lazy-bg {
  transition: opacity 0.3s ease;
}
.lazy-loaded {
  opacity: 1;
}
</style>
