# EntropyGate Crawler Worker

GitHub Actions 上的**境外抓取出口**。解决 Studio（部署在中国机房）无法直连
Google / DeepMind / HuggingFace / OpenAI / Anthropic 等海外源的问题。

## 原理

- GitHub Actions runner 出口在境外（美/欧），不受 GFW 限制，且 IP 段通常被海外
  站点接受 → 在这些 runner 上抓取全文。
- 抓到的文章通过 `POST {STUDIO_BASE_URL}/api/v1/articles` 推送给 Studio。
  Studio **原样存储**传入的 `content`，不会从中国重抓，只做评分 + LLM 改写。
- 每 30 分钟跑一次（`cron: "*/30 * * * *"`），也可在 Actions 页面手动 `Run workflow`。

## 去重

`seen_urls.json` 每次运行后提交回仓库，避免同一篇文章在每轮重复入库。

## 配置（仓库 Secrets）

| Secret | 说明 |
| --- | --- |
| `STUDIO_BASE_URL` | Studio 地址，如 `https://dl5201010-ai-news-platform.ms.show` |
| `STUDIO_ADMIN_PASSWORD` | 管理员密码（用于登录拿 `X-Access-Token`） |
| `PAT` | 本仓库的 Personal Access Token，用于把 `seen_urls.json` 提交回仓 |

## 增加来源

编辑 `sources.json`：

```json
{
  "name": "显示名",
  "parser_type": "rss",          // 或 "html"
  "feed_url": "https://.../rss.xml",
  "language": "en"
}
```

HTML 列表页用 `"parser_type": "html"` + `"list_url"` + `"selectors": {"article_list":"a","title":"h2","summary":"p"}`。

## 注意事项

- 本方案**不需要代理**，靠 Actions 境外出口即可。
- `PAT` 是明文凭据，建议用最小权限、定期轮换；不要 commit 到仓库。
- 若某源被 Azure IP 段限流，可加 Cloudflare Worker 抓取代理作为兜底（见评估文档）。
