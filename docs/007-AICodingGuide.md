# AI Intelligence Coding Guide（AICodingGuide）

> 版本：v1.0 | 创建日期：2026-07-06 | 更新频率：每季度 Review

> 参考：[002-AIS.md](002-AIS.md)

---

## 设计原则（Design Principles）

参考 [001-Vision.md](001-Vision.md) 中的设计原则章节。

---

## 核心规则

### 禁止事项（Must Not）

| # | 禁止行为 | 原因 |
|---|---------|------|
| 1 | **不得新增 Dictionary** | Dictionary 必须通过 AIS Review 流程 |
| 2 | **不得修改 Naming** | 命名规范是 AIS 的一部分，修改需 Review |
| 3 | **不得删除 Capability** | Capability 是核心资产，只能 deprecate |
| 4 | **不得新增 Event Type** | Event Type 必须通过 AIS Review 流程 |
| 5 | **不得直接修改 AIS** | AIS 是宪法，修改需走正式流程 |
| 6 | **不得创建与现有 Capability 含义重叠的标签** | 用 aliases 解决，不新增标签 |
| 7 | **不得跳过 AI Review** | 所有 AI 输出必须经过 Review |
| 8 | **不得在数据库中存储非标准化的数据** | 必须遵循 AIS 规范 |

### 必须事项（Must）

| # | 必须行为 | 原因 |
|---|---------|------|
| 1 | **所有 AI 输出必须遵循 AIS 规范** | 统一语言，避免混乱 |
| 2 | **所有 Capability 标签必须来自 Dictionary** | 不允许 AI 自创标签 |
| 3 | **所有 Event Type 必须来自 Dictionary** | 不允许 AI 自创事件类型 |
| 4 | **所有 Entity 必须来自 Dictionary** | 不允许 AI 自创实体 |
| 5 | **所有数据必须有证据来源** | 可追溯，可验证 |
| 6 | **所有事实必须拆分为 Fact** | Fact 是原子单位 |
| 7 | **所有 Event 必须包含多个 Fact** | 事件由事实组成 |
| 8 | **所有回答必须遵循 AAS 规范** | 统一回答格式 |

---

## Review Checklist

### 开发前检查

| # | 检查项 | 说明 |
|---|--------|------|
| 1 | 需求是否对应 AIQL 中的问题？ | 确保开发有明确目标 |
| 2 | 需要的 Capability 是否在 Dictionary 中？ | 不允许使用未定义的标签 |
| 3 | 需要的 Entity 是否在 Dictionary 中？ | 不允许使用未定义的实体 |
| 4 | 需要的 Event Type 是否在 Dictionary 中？ | 不允许使用未定义的类型 |
| 5 | 数据模型是否符合 AKG 规范？ | 确保图谱结构正确 |

### 开发中检查

| # | 检查项 | 说明 |
|---|--------|------|
| 1 | AI 是否使用了未定义的 Capability 标签？ | 必须从 Dictionary 中选择 |
| 2 | AI 是否使用了未定义的 Event Type？ | 必须从 Dictionary 中选择 |
| 3 | AI 是否使用了未定义的 Entity？ | 必须从 Dictionary 中选择 |
| 4 | 所有数据是否有证据来源？ | 必须可追溯 |
| 5 | 是否跳过了 Fact 提取直接生成 Event？ | 必须先拆 Fact |

### 开发后检查

| # | 检查项 | 说明 |
|---|--------|------|
| 1 | 是否能够回答目标问题？ | 验证开发成果 |
| 2 | 回答是否遵循 AAS 规范？ | 验证回答格式 |
| 3 | 数据是否正确入库？ | 验证数据完整性 |
| 4 | 是否有未处理的异常情况？ | 验证健壮性 |
| 5 | 是否通过了所有测试？ | 验证正确性 |

---

## AI Coding Prompt 规范

### 通用 Prompt 结构

```
你是本项目的 AI 助手，必须严格遵循 AIS 规范。

规则：
1. 所有 Capability 标签必须从 Dictionary 中选择，不允许自创
2. 所有 Event Type 必须从 Dictionary 中选择，不允许自创
3. 所有 Entity 必须从 Dictionary 中选择，不允许自创
4. 必须先拆 Fact，再组成 Event
5. 所有输出必须可追溯到证据来源
6. 回答必须遵循 AAS 规范

输入：
{输入内容}

输出格式：
{指定输出格式}
```

### Capability 提取 Prompt

```
你是本项目的 AI 助手，必须严格遵循 AIS 规范。

任务：从以下文本中提取 AI 能力标签。

规则：
1. 能力标签必须从 Dictionary 中选择（见附录）
2. 不允许自创标签
3. 每个标签必须给出置信度（0-1）
4. 对于不确定的内容，使用 "uncertain" 字段列出

输入文本：
{text}

输出格式（JSON）：
{
  "capabilities": [
    {"code": "memory.long-term.user", "confidence": 0.95},
    {"code": "tool-use.mcp.client", "confidence": 0.85}
  ],
  "uncertain": [
    {"text": "some capability", "suggested_code": "reasoning.code.generation"}
  ]
}

附录：可用的 Capability 标签（部分）
{capability_list}
```

### Fact 提取 Prompt

```
你是本项目的 AI 助手，必须严格遵循 AIS 规范。

任务：从以下新闻中提取事实（Fact）。

规则：
1. 一条新闻可能包含多个 Fact
2. Fact 必须是原子单位（不可再拆分）
3. 每个 Fact 必须有类型、主体、能力（如适用）、值
4. 能力标签必须从 Dictionary 中选择

新闻内容：
{news_content}

输出格式（JSON）：
{
  "facts": [
    {
      "type": "capability-added",
      "subject": "model-claude-4-1",
      "capability": "memory.long-term.user",
      "value": "cross-session memory up to 100 conversations",
      "evidence": "Claude 4.1 now supports long-term memory",
      "confidence": 0.95
    }
  ]
}
```

### Event 构建 Prompt

```
你是本项目的 AI 助手，必须严格遵循 AIS 规范。

任务：将以下 Fact 组成 Event。

规则：
1. 一个 Event 由多个 Fact 组成
2. Event Type 必须从 Dictionary 中选择
3. Event 必须有标题、摘要、评分

Fact 列表：
{facts}

输出格式（JSON）：
{
  "event": {
    "type": "model-update",
    "title": "Claude 4.1 Released",
    "summary": "Claude 4.1 新增了长期记忆和项目记忆能力",
    "facts": [...],
    "capabilities": ["memory.long-term.user", "memory.project.workspace"],
    "score": 85,
    "confidence": 95
  }
}
```

---

## 开发规范

### 代码风格

| 规则 | 说明 |
|------|------|
| 语言 | Python 3.10+ |
| 框架 | FastAPI |
| 数据库 | SQLite（开发）/ PostgreSQL（生产） |
| ORM | SQLAlchemy |
| 命名 | 遵循 AIS 的 Naming Convention |

### 目录结构

```
ai-news-backend/
├── app/
│   ├── crawler/           # 采集模块
│   ├── services/          # 业务服务
│   ├── models/            # 数据模型
│   ├── api/               # API 接口
│   ├── ai/                # AI 服务
│   ├── utils/             # 工具函数
│   └── config/            # 配置文件
├── tests/                 # 测试
├── docs/                  # 文档
├── alembic/               # 数据库迁移
└── celery/                # 定时任务
```

### 数据模型规范

所有数据模型必须符合 AKG 规范：

| 规则 | 说明 |
|------|------|
| 表名 | 复数形式，蛇形命名 |
| 字段名 | 蛇形命名，无缩写 |
| 外键 | 必须建立正确的关系 |
| 时间戳 | 使用 `_at` 后缀 |
| 布尔值 | 使用 `is_` 前缀 |

### API 规范

| 规则 | 说明 |
|------|------|
| 风格 | RESTful |
| 路径 | 复数形式 |
| 参数 | 查询参数用 snake_case |
| 响应 | JSON 格式 |
| 错误 | 统一错误格式 |

### 测试规范

| 规则 | 说明 |
|------|------|
| 框架 | pytest |
| 覆盖率 | ≥ 80% |
| 测试数据 | 使用 fixtures |
| 测试命名 | `test_{功能}_{场景}` |

---

## 新增 Dictionary 流程

### 步骤

1. **提案**：在 AIS 文档中新增提案，包含：
   - code（遵循命名规范）
   - name_en / name_zh
   - definition
   - 为什么现有标签无法覆盖

2. **Review**：每周 Review 会议讨论：
   - 是否真的是新概念（不是别名）
   - 应该放在哪个 Domain/Category
   - 是否与现有标签有重叠

3. **批准**：添加到 Dictionary，版本号 +1

4. **回刷**：对过去 30 天的 Event 重新打标签（如有必要）

### 提案格式

```yaml
proposal_id: cap-001
type: capability
code: {proposed_code}
name_en: {proposed_name_en}
name_zh: {proposed_name_zh}
domain: {proposed_domain}
category: {proposed_category}
definition: >
  {详细定义}
reason_for_new: >
  为什么现有标签无法覆盖？
related_capabilities:
  - {相关标签1}
  - {相关标签2}
examples:
  - {示例1}
  - {示例2}
author: {提案人}
date: {日期}
status: pending
```

---

## 版本管理

### 代码版本

```
{major}.{minor}.{patch}
```

- 新增功能：minor +1
- 修复 bug：patch +1
- 破坏兼容：major +1

### 数据版本

所有数据库表都有版本号：
```
table_version: Integer
```

迁移时版本号 +1。

---

## 错误处理

### 常见错误

| 错误 | 原因 | 处理方式 |
|------|------|---------|
| AI 生成未定义的 Capability | Prompt 未包含完整 Dictionary | 增加 Dictionary 到 Prompt |
| AI 生成未定义的 Event Type | Prompt 未包含完整 Dictionary | 增加 Dictionary 到 Prompt |
| Fact 提取不完整 | 新闻内容太长 | 分段处理 |
| Event 合并错误 | 相似度阈值不合适 | 调整阈值 |
| 证据缺失 | 来源不可访问 | 标记为 pending |

### 错误日志

| 字段 | 说明 |
|------|------|
| error_type | 错误类型 |
| error_message | 错误信息 |
| source | 来源 |
| timestamp | 时间戳 |
| context | 上下文数据 |

---

*文档版本：v1.0*
*创建日期：2026-07-06*
*下次 Review：2026-10-06*
