#!/usr/bin/env bash
set -euo pipefail

conflicts=$(git diff --name-only --diff-filter=U || true)
if [[ -z "$conflicts" ]]; then
  echo "No merge conflicts detected."
  exit 0
fi

echo "Detected conflicts:"
echo "$conflicts"

# Choice policy:
# 1) Generated outputs: take incoming branch (theirs) to minimize stale local artifacts.
# 2) Skill definitions/templates: keep current branch (ours) to preserve latest workflow rules.

for f in \
  outputs/2026-02-26/application_radar.md \
  outputs/2026-02-26/daily_digest.md \
  outputs/2026-02-26/rejection_log.md \
  outputs/2026-02-26/run_summary.md \
  outputs/2026-02-26/candidates.json
  do
    if echo "$conflicts" | grep -Fxq "$f"; then
      git checkout --theirs -- "$f"
      git add "$f"
      echo "resolved(theirs): $f"
    fi
  done

for f in \
  skills/ai-news-app-radar/SKILL.md \
  skills/ai-news-app-radar/references/output_templates.md
  do
    if echo "$conflicts" | grep -Fxq "$f"; then
      git checkout --ours -- "$f"
      git add "$f"
      echo "resolved(ours): $f"
    fi
  done

remaining=$(git diff --name-only --diff-filter=U || true)
if [[ -n "$remaining" ]]; then
  echo "Unresolved files remain:"
  echo "$remaining"
  exit 2
fi

echo "All known conflicts resolved."
