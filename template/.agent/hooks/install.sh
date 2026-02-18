#!/usr/bin/env bash
# Git hooks installer
# Run: bash .agent/hooks/install.sh

HOOKS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GIT_HOOKS_DIR="$(git rev-parse --git-dir)/hooks"

echo "📦 Installing Agent OS hooks to Git..."

# Create symlink for pre-commit
ln -sf "$HOOKS_DIR/pre-commit" "$GIT_HOOKS_DIR/pre-commit"

echo "✅ Hooks installed!"
echo "   → Pre-commit hook: $GIT_HOOKS_DIR/pre-commit"
echo ""
echo "Now every 'git commit' will run quality checks automatically."
