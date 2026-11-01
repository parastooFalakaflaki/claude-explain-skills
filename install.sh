#!/usr/bin/env bash
# Copies the skills, subagent and output style into ~/.claude.
# Stops without copying anything if a file would be replaced, unless you pass --force.
set -euo pipefail

source_dir="$(cd "$(dirname "$0")" && pwd)"
target_dir="${HOME}/.claude"
force="${1:-}"

targets=()
for path in "$source_dir"/skills/*; do targets+=("skills/$(basename "$path")"); done
for path in "$source_dir"/agents/* "$source_dir"/output-styles/*; do
  targets+=("$(basename "$(dirname "$path")")/$(basename "$path")")
done

if [ "$force" != "--force" ]; then
  conflicts=0
  for target in "${targets[@]}"; do
    if [ -e "$target_dir/$target" ]; then
      echo "Already exists: $target_dir/$target"
      conflicts=1
    fi
  done
  if [ "$conflicts" -eq 1 ]; then
    echo "Nothing was copied. Run again with --force to replace these."
    exit 1
  fi
fi

for target in "${targets[@]}"; do
  mkdir -p "$target_dir/$(dirname "$target")"
  rm -rf "${target_dir:?}/$target"
  cp -R "$source_dir/$target" "$target_dir/$target"
  echo "Installed $target"
done

echo
echo "Last step: add this line to $target_dir/settings.json, then restart Claude Code:"
echo '  "outputStyle": "Plain explainer"'
