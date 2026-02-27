# Output Templates

## 0) 文件落盘规范（统一目录，禁止散落）

```text
outputs/
  YYYY-MM-DD/
    daily_digest.md
    application_radar.md
    rejection_log.md
    run_summary.md
    weekly_trends.md   # 可选，仅在周报日生成
```

All generated files must be written into the same `outputs/YYYY-MM-DD/` folder.

## A) 每日简报条目模板

```markdown
### {{中文标题}}
- 事实摘要：{{1-2句客观事实}}
- 关键细节：
  - {{细节1：主体 + 动作 + 时间}}
  - {{细节2：关键数字/里程碑}}
  - {{细节3：范围/对象/限制条件}}
- 影响解读：{{对产业链、应用落地或竞争格局的影响}}
- 观点对照：
  - 来源A（{{媒体名}}）：{{观点A}}
  - 来源B（{{媒体名}}）：{{观点B}}
- Links：
  - {{URL1}}
  - {{URL2}}
```

## B) 应用雷达模板

```markdown
### {{案例名/公司名}}
- 行业：{{industry}}
- 场景：{{use-case}}
- 成熟度：{{概念验证/试点/规模化}}
- ROI信号：{{效率/转化/错误率/周期}}
- 可复用做法：{{工具链/流程/组织协作}}
- Links：{{公开链接}}
```

## C) 每周趋势报告模板

```markdown
## 本周AI趋势
- 热词Top10：{{词 + 周环比}}
- 升温赛道：{{赛道 + 证据链接}}
- 公司/产品动向：{{里程碑列表}}
- 政策与安全变化：{{重点政策/事件}}
- 下周观察点：{{3-5条}}
```

## D) 不入选清单模板（rejection_log.md）

```markdown
# 不入选清单（{{YYYY-MM-DD}}）

## 统计
- 候选总数：{{N}}
- 入选数：30
- 不入选数：{{N-30}}

## 不入选条目
1. **{{标题}}**
   - 来源：{{source}}
   - 链接：{{url}}
   - 不入选理由：{{单行原因}}

2. **{{标题}}**
   - 来源：{{source}}
   - 链接：{{url}}
   - 不入选理由：{{单行原因}}
```

## E) 运行摘要模板（run_summary.md）

```markdown
# 运行摘要（{{YYYY-MM-DD}}）

## 输出文件
- daily_digest.md
- application_radar.md
- rejection_log.md
- run_summary.md
- weekly_trends.md（可选）

## 指标
- 候选总数：{{N}}
- 入选数：30
- 不入选数：{{N-30}}
- 来源覆盖数：{{distinct_sources}}

## 告警与说明
- {{若候选不足30，说明原因}}
- {{抓取失败来源列表（如有）}}

- {{cache_fallback_used: 路径（如使用）}}
- {{bootstrap_fallback_used: 路径（如使用）}}
```


## F) 抓取失败来源模板（写入 run_summary.md）

```markdown
## 抓取失败来源列表
1. {{source_name}}
   - 原始URL：{{feed_url}}
   - 失败阶段：{{direct/jina/rsshub}}
   - 错误信息：{{error_message}}
   - 降级状态：{{是否已由其他来源覆盖}}
```
=======

