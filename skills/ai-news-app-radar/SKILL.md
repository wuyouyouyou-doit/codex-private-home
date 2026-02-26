---
name: ai-news-app-radar
description: Build and operate a daily AI news plus AI applications intelligence pipeline (free/public sources only) with layered source strategy, ingestion/normalization/deduplication/clustering/ranking, Chinese digest generation with citations and multi-viewpoint comparison, and weekly trend tracking. Use when user asks to set up or improve AI news monitoring, application radar, source taxonomy, digest templates, or trend reports.
---

# AI News + AI Applications Radar

Follow this workflow to produce a high-signal daily brief in Chinese with traceable links.

## 1) Define daily outputs

Generate three outputs:

1. **Daily digest (exactly 30 selected items)**
2. **Application radar (5–10 items)**
3. **Weekly trend recap**
4. **Rejection log (all non-selected candidates with reasons)**

Daily operation target:

- Collect candidate pool first, then select exactly 30 items for daily digest.
- Keep transparent review trail: every non-selected candidate must be recorded with one clear rejection reason.
- If candidate pool < 30 after quality checks, explicitly report shortage and why.

For each digest item, always output:

- 标题（中文）
- 事实摘要（1–2 句，客观）
- 关键细节（3–5 条，优先包含时间、主体、数字）
- 影响解读（1 段）
- 观点对照（至少两个不同来源）
- 原文链接（按可信度排序）

For each rejected item, always output:

- 原始标题
- 来源
- 不入选理由（单行、可审计，例如“重复报道”“信源不足”“与主题弱相关”“缺少可核实链接”）

## 2) Use 3-layer source strategy

Use source layers with different confidence weights:

- **L1 Fact base (high trust)**: wire/newsroom sources for confirming event facts.
- **L2 Product & application discovery (high frequency)**: newsletters, product blogs, dev communities.
- **L3 Deep analysis (contextual understanding)**: research/industry long-form analysis.

Use only free/public content in MVP. Do not rely on paywalled full text.

## 3) Build pipeline modules

Implement these modules in order:

1. `source_registry`: manage source metadata (`type`, `frequency`, `weight`, `tags`, `language`, `access`).
2. `ingestion`: use resilient fetch chain for RSS (direct -> mirror/proxy -> extraction fallback) to tolerate 403/blocked feeds.
3. `normalize`: standardize title/time/author/summary/url/source.
4. `dedupe_cluster`: URL dedupe + title similarity + optional embedding clustering.
5. `rank_filter`: source weight + novelty + topic preference + multi-source coverage.
6. `selection_audit`: output selected=30 and rejected list with reasons.
7. `summarize_output`: generate Chinese digest with citation links and viewpoint comparison.

## 3.1) Enforce deterministic output folder structure

Write outputs only into one dated folder. Do not scatter files.

- Root folder: `outputs/`
- Daily folder: `outputs/YYYY-MM-DD/`
- Required files:
  1. `daily_digest.md` (30 selected items)
  2. `application_radar.md`
  3. `rejection_log.md` (all non-selected candidates + reasons)
  4. `run_summary.md` (counts, source stats, warnings)

If weekly recap is generated that day, save as `weekly_trends.md` in the same dated folder.

## 3.2) Handle RSS 403/blocked network (required)

When direct RSS fetch fails (e.g., `Tunnel connection failed: 403 Forbidden`), do not stop.

Run bundled script first:

```bash
python skills/ai-news-app-radar/scripts/resilient_feed_fetch.py \
  --registry skills/ai-news-app-radar/references/source_registry_free.yaml \
  --out outputs/YYYY-MM-DD/candidates.json \
  --cache-glob "outputs/*/candidates.json" \
  --bootstrap skills/ai-news-app-radar/references/bootstrap_candidates.json
```

The script automatically tries multiple methods per source:

1. direct URL
2. `r.jina.ai` mirror path
3. `r.jina.ai/{url}` mirror path
4. RSSHub conversion fallback

Then continue ranking/selection from `candidates.json`.

If some sources still fail, continue with partial candidates and record per-source failures in `run_summary.md` under “抓取失败来源列表”.
- If all network methods fail, fallback to latest local `outputs/*/candidates.json` cache and mark it in run summary as `cache_fallback_used`.
- If no network data and no local cache are available, load `references/bootstrap_candidates.json` to keep pipeline outputs deterministic, and mark items as `bootstrap` in run summary for manual replacement later.

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
- Keep strict formatting consistency: every markdown file must use headings + bullet lists + numbered sections where applicable.
- Keep titles explicit and human-readable; avoid ambiguous or duplicate headlines.

## 6) Use bundled references

- Load `references/source_registry_free.yaml` for starter free sources (30 entries).
- Load `references/output_templates.md` for digest and weekly report formatting.
- Load `references/scoring.md` for default ranking formula and thresholds.
- Use `scripts/resilient_feed_fetch.py` for anti-403 resilient ingestion before ranking.
- Use `references/bootstrap_candidates.json` only as last-resort continuity fallback when all remote fetching is blocked.
