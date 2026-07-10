# P2 — Entity Experience Roadmap

> **从信息流 → 知识门户**

---

## 目标

把网站从"新闻流"升级为"知识入口"。

用户不只是看新闻，而是进入一个实体（Company / Model / Capability / Research）后，看到该实体的完整 Intelligence。

---

## 架构原则

### 统一数据流

```
Entity (数据库)
    ↓
Entity Projection (纯函数)
    ↓
Entity Snapshot (JSON 文件)
    ↓
Entity API (只读快照)
    ↓
Vue Entity Page
```

**禁止页面直接拼 SQL。所有页面都消费 Projection。**

### Entity Types

第一批（P2 必须完成）：
- Company
- Model
- Capability
- Research

后续（P3+）：
- Person
- Organization
- Dataset
- Benchmark
- Policy

---

## Entity Output Contract

每个 Entity Projection 输出统一结构：

```json
{
  "entity": {
    "slug": "openai",
    "name": "OpenAI",
    "type": "company",
    "description": "...",
    "website": "https://openai.com",
    "founded": "2015",
    "logo_url": "..."
  },
  "summary": {
    "headline": "OpenAI: Leading AI Research Lab",
    "overview": "...",
    "total_events": 42,
    "total_capabilities": 12,
    "maturity": "mature"
  },
  "timeline": [
    {"date": "2026-03-15", "event": "GPT-5 Released", "type": "model_release"},
    {"date": "2026-01-20", "event": "Deep Research announced", "type": "feature_added"}
  ],
  "latest_events": [
    {"id": "...", "title": "...", "type": "...", "score": 85}
  ],
  "capabilities": [
    {"name": "Reasoning", "status": "mature", "maturity_score": 90},
    {"name": "Memory", "status": "active", "maturity_score": 75}
  ],
  "knowledge": [
    {"predicate": "released", "object": "GPT-5"},
    {"predicate": "partnership", "object": "Microsoft"}
  ],
  "relations": [
    {"type": "model", "slug": "gpt-5", "name": "GPT-5"},
    {"type": "partner", "slug": "microsoft", "name": "Microsoft"}
  ],
  "generated_at": "2026-07-08T08:00:00Z"
}
```

---

## Snapshot Storage

```
evidence/snapshots/
    company/
        openai.json
        anthropic.json
        google.json
        meta.json
        ...
    model/
        gpt-5.json
        claude-3.json
        gemini.json
        ...
    capability/
        reasoning.json
        memory.json
        agent.json
        ...
    research/
        transformers.json
        diffusion.json
        llm-alignment.json
        ...
```

---

## API Endpoints

| Endpoint | 用途 |
|----------|------|
| `GET /entity/company/{slug}` | Company 详情页 |
| `GET /entity/model/{slug}` | Model 详情页 |
| `GET /entity/capability/{slug}` | Capability 详情页 |
| `GET /entity/research/{slug}` | Research 详情页 |
| `GET /entity/list/{type}` | Entity 列表（可选） |

所有 API 直接读取 Snapshot，**禁止请求阶段复杂 SQL 聚合**。

---

## Tasks

### P2-1: Entity Projection Framework

创建统一 EntityProjection 基类和 4 个具体实现：
- `CompanyProjection`
- `ModelProjection`
- `CapabilityProjection`
- `ResearchProjection`

### P2-2: Entity Snapshot Output

创建 `snapshots/` 目录结构和输出逻辑。

### P2-3: Entity API

创建 `entity.py` router，4 个 endpoint。

### P2-4: EntityPipeline

创建调度器，自动刷新所有 Entity Snapshot。

### P2-5: Homepage → Entity Link

Homepage 卡片增加 `entity_slug` 字段，前端点击跳转 Entity 页。

### P2-6: Timeline & Relations

确保每个 Entity 都有 `timeline` 和 `relations` 字段。

---

## Definition of Done

| 项 | DoD |
|----|-----|
| Company Projection | ✅ |
| Model Projection | ✅ |
| Capability Projection | ✅ |
| Research Projection | ✅ |
| Entity Snapshot 自动生成 | ✅ |
| Entity API 全部读取 Snapshot | ✅ |
| Timeline Projection | ✅ |
| Relations Projection | ✅ |
| Homepage 卡片跳转 Entity | ✅ |
| Runtime / Platform / Governance 修改 | **0** |

---

## P2 完成后的产品形态

产品将从：
```
Feed Website
```
升级为：
```
Intelligence Knowledge Portal
```

用户拥有两种浏览方式：
- **纵向浏览**：首页 Feed → Intelligence 流。
- **横向探索**：Entity → Timeline → Relations → Knowledge。

这是产品从"新闻聚合"迈向"AI Intelligence 平台"的关键一步。