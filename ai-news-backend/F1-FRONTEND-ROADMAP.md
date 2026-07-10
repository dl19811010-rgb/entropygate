# F1 Frontend Product Integration

## 目标

让目前所有 Projection 真正成为网站页面。

## 架构原则

- Frontend 只消费 Snapshot，不做复杂数据库聚合
- API baseURL: `/api/v1`
- 所有页面直接读取 Projection 输出的 snapshot
- Architecture Budget: 0（不修改 Runtime/Platform/Governance）

## API 映射

| 页面 | API Endpoint | 数据来源 |
|------|-------------|---------|
| 首页 | `GET /api/v1/homepage/feed` | feed_daily.json |
| Entity | `GET /api/v1/entity/{type}/{slug}` | entity snapshot |
| 搜索 | `GET /api/v1/search?q=` | search_index.json |
| 搜索建议 | `GET /api/v1/search/suggest?q=` | search_index.json |
| 时间线 | `GET /api/v1/timeline?period=` | feed + entity snapshots |
| 实体时间线 | `GET /api/v1/timeline/entity/{type}/{slug}` | entity snapshot |
| Product Health | `GET /api/v1/product-dashboard/product` | feed + registry |
| Runtime Health | `GET /api/v1/product-dashboard/runtime` | golden + evidence |

## 实施阶段

### F1-1 首页 (Home.vue)
- 接入 `GET /api/v1/homepage/feed`
- 渲染：Today's Headline, Major Events, Capability Changes, Important Releases, Industry Trends, Research Highlights, Latest Benchmarks
- 完全来自 feed snapshot，不调用 articles API

### F1-2 Entity 页面 (EntityDetail.vue)
- 路由：`/entity/:type/:slug`
- 接入 `GET /api/v1/entity/{type}/{slug}`
- 展示：Overview, Timeline, Latest Events, Capabilities, Knowledge, Relations
- 支持类型：company, model, capability, research

### F1-3 搜索 (Search.vue)
- 接入 `GET /api/v1/search?q=`
- 接入 `GET /api/v1/search/suggest?q=`
- 实现：Autocomplete, Recent Search, Search Result
- 搜索结果点击跳转到 Entity 页面

### F1-4 时间线 (Timeline.vue)
- 路由：`/timeline` 和 `/timeline/:type/:slug`
- 接入 `GET /api/v1/timeline?period=` (today/week/month/all)
- 接入 `GET /api/v1/timeline/entity/{type}/{slug}`

### F1-5 Dashboard (ai-news-admin)
- 接入 `GET /api/v1/product-dashboard/product`
- 接入 `GET /api/v1/product-dashboard/runtime`
- 展示：Signals Today, Facts Today, Events Today, Knowledge, Success Rate, Review Queue, Replay, Conformance, Spec Age

## Definition of Done

```
[F1 Frontend Product Integration]

Homepage:
PASS

Entity Pages:
PASS

Search:
PASS

Timeline:
PASS

Dashboard:
PASS

Snapshot-only Rendering:
PASS

No Runtime Logic in Frontend:
PASS

End-to-End Navigation:
PASS

Performance:
PASS

Architecture Budget:
0

Overall:
🟢 READY
```
