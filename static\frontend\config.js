// 运行时配置：前端分离部署(EdgeOne/Cloudflare Pages)时，
// 由部署脚本把本文件覆盖为真实 API 基地址，例如：
//   window.API_BASE = "https://entropygate.cc.cd/api/v1";
// （API 直接走后端稳定地址 entropygate.cc.cd，避免 CNAME 跨域证书问题；
//   公众端/后台的品牌域名 aientropygate.com 仅用于静态资源 Geo 分流）
// 同源部署(ModelScope)留空，app.js 自动回退到 /api/v1。
// 注意：本文件须在 app.js 之前加载。
window.API_BASE = "";
