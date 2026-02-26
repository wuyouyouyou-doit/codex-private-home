# codex-private-home
codex项目库

## Skills

- `skills/ai-news-app-radar`: AI 新闻 + AI 应用情报收集与简报生成 skill（免费公开信源优先）。


## 冲突处理（本仓库约定）

当 PR 出现冲突时，优先使用脚本自动按约定解决：

```bash
bash scripts/resolve_pr_conflicts.sh
```

策略：
- `outputs/` 生成文件优先取 `theirs`（减少样例产物冲突噪音）。
- `skills/ai-news-app-radar/SKILL.md` 与 `references/output_templates.md` 优先取 `ours`（保留当前分支最新规则）。
