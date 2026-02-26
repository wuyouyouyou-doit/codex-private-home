# Ranking and Filtering Defaults

Use this baseline score:

`score = 0.35 * source_weight + 0.25 * novelty + 0.20 * topic_priority + 0.20 * multi_source_coverage`

## Inputs

- `source_weight`: L1=1.0, L2=0.75, L3=0.65
- `novelty`: normalize by first-seen time and semantic distance against last 7 days
- `topic_priority`: configurable boosts for tracked themes (e.g., agent, video generation, chips)
- `multi_source_coverage`: 1.0 if >=2 distinct sources corroborate same cluster, else 0.4

## Filtering thresholds

- Daily digest candidate: `score >= 0.62`
- Application radar candidate: (`use_case_detected=true` and `score >= 0.58`)
- Force-include rule: include safety/policy items with >=1 L1 source even if score slightly below threshold.

## Diversity guardrails

- Keep at least one non-vendor source in top 10.
- For policy and safety, include at least two different stance sources when available.
- Cap same-domain items to avoid overfitting one newsletter.
