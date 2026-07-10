<script setup>
const currentYear = new Date().getFullYear()
</script>

<template>
  <footer class="app-footer">
    <div class="footer-inner">
      <div class="footer-content">
        <div class="footer-brand">
          <div class="logo-text">EntropyGate AI</div>
          <p class="footer-desc">探索 AI 领域的无限可能，汇聚全球前沿人工智能资讯</p>
        </div>
        <div class="footer-links">
          <div class="link-group">
            <h4>内容栏目</h4>
            <a href="/news">AI新动态</a>
            <a href="/tools">AI工具库</a>
          </div>
          <div class="link-group">
            <h4>关于我们</h4>
            <a href="#">关于本站</a>
            <a href="#">联系方式</a>
            <a href="#">投稿建议</a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>© {{ currentYear }} EntropyGate AI. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.app-footer {
  background: var(--bg-secondary);
  color: var(--text-tertiary);
  margin-top: 60px;
}

.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 48px 24px 24px;
}

.footer-content {
  display: grid;
  grid-template-columns: 2fr 3fr;
  gap: 48px;
  padding-bottom: 32px;
  border-bottom: 1px solid var(--border-color);
}

.footer-brand .logo-text {
  font-size: 22px;
  font-weight: 700;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 12px;
}

.footer-desc {
  font-size: 14px;
  line-height: 1.6;
}

.footer-links {
  display: flex;
  gap: 64px;
}

.link-group h4 {
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 16px;
}

.link-group a {
  display: block;
  font-size: 13px;
  color: var(--text-tertiary);
  margin-bottom: 10px;
  transition: color 0.2s;
}

.link-group a:hover {
  color: var(--brand-primary);
}

.footer-bottom {
  padding-top: 24px;
  text-align: center;
  font-size: 13px;
  color: var(--text-tertiary);
}
</style>
