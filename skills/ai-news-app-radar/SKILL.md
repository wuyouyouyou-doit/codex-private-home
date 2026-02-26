---
name: ai-news-app-radar
description: Build and operate a daily AI news plus AI applications intelligence pipeline (free/public sources only) with layered source strategy, ingestion/normalization/deduplication/clustering/ranking, Chinese digest generation with citations and multi-viewpoint comparison, and weekly trend tracking. Use when user asks to set up or improve AI news monitoring, application radar, source taxonomy, digest templates, or trend reports.
---

# AI News + AI Applications Radar

Follow this workflow to produce a high-signal daily brief in Chinese with traceable links.

## 1) Define daily outputs

Generate three outputs:

1. **Daily digest (10–20 items)**
2. **Application radar (5–10 items)**
3. **Weekly trend recap**

For each digest item, always output:

- 标题（中文）
- 事实摘要（1–2 句，客观）
- 关键细节（3–5 条，优先包含时间、主体、数字）
- 影响解读（1 段）
- 观点对照（至少两个不同来源）
- 原文链接（按可信度排序）

## 2) Use 3-layer source strategy

Use source layers with different confidence weights:

- **L1 Fact base (high trust)**: wire/newsroom sources for confirming event facts.
- **L2 Product & application discovery (high frequency)**: newsletters, product blogs, dev communities.
- **L3 Deep analysis (contextual understanding)**: research/industry long-form analysis.

Use only free/public content in MVP. Do not rely on paywalled full text.

## 3) Build pipeline modules

Implement these modules in order:

1. `source_registry`: manage source metadata (`type`, `frequency`, `weight`, `tags`, `language`, `access`).
2. `ingestion`: prioritize RSS; use lightweight web extraction only when RSS is unavailable.
3. `normalize`: standardize title/time/author/summary/url/source.
4. `dedupe_cluster`: URL dedupe + title similarity + optional embedding clustering.
5. `rank_filter`: source weight + novelty + topic preference + multi-source coverage.
6. `summarize_output`: generate Chinese digest with citation links and viewpoint comparison.

## 4) Apply taxonomy tags

Tag each item with multi-label taxonomy.

### News taxonomy

- Model / Research
- Product / Platform
- Company / People
- Funding / M&A
- Policy / Regulation
- Safety / Security
- Infra / Chips / Cloud

### Applications taxonomy

- Industry (医疗/教育/金融/制造/零售/内容/法律/政务/能源/汽车…)
- Use-case (客服/营销/代码/数据分析/知识库/流程自动化/研发助理/质检…)
- Maturity (概念验证/试点/规模化)
- ROI signal (节省人力/提升转化/降低错误率/缩短周期)

## 5) Enforce quality and compliance rules

- Attach links for every factual claim and numeric datapoint.
- Mark uncertain claims as “据…报道/尚未证实”.
- Keep viewpoint diversity for policy/safety topics.
- Respect copyright and paywalls; summarize only accessible content.

## 6) Use bundled references

- Load `references/source_registry_free.yaml` for starter free sources (30 entries).
- Load `references/output_templates.md` for digest and weekly report formatting.
- Load `references/scoring.md` for default ranking formula and thresholds.
