#!/usr/bin/env python3
"""
files_map.py
Generates a tree-like structure of the project files.
Faster and more token-efficient than list_dir for deep structures.

v2.0 Changes:
- Fixed: .agent/ and other dotted project directories were silently skipped.
- Added: Explicit SHOW_DOT_DIRS whitelist for agent infrastructure directories.
- Added: --agent flag to show only the .agent/ directory tree.
- Added: Configurable MAX_DEPTH via argument.
"""

import os
import sys

# Configuration
# Directories to always ignore (noise, build artifacts, secrets)
IGNORE_DIRS = {
    '.git', '.github', 'node_modules', 'vendor', '__pycache__',
    '.idea', '.vscode', 'storage', 'public/build', '.DS_Store',
    'dist', 'build', 'coverage', '.nyc_output',
}

# Dot-prefixed directories that SHOULD be shown (whitelist for agent infra)
SHOW_DOT_DIRS = {'.agent', '.env', '.envrc'}

IGNORE_EXTS = {
    '.pyc', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg',
    '.woff', '.woff2', '.ttf', '.eot', '.map', '.min.js', '.min.css',
    '.lock', '.bak',
}

DEFAULT_MAX_DEPTH = 4


def print_tree(startpath, depth=0, max_depth=DEFAULT_MAX_DEPTH, show_hidden=False):
    """Recursively print file tree."""
    if depth > max_depth:
        return

    try:
        entries = sorted(os.listdir(startpath))
    except PermissionError:
        return

    dirs = []
    files = []

    for entry in entries:
        full_path = os.path.join(startpath, entry)
        is_dot = entry.startswith('.')

        # Dot files/dirs: show only whitelisted ones (or all if show_hidden)
        if is_dot and not show_hidden and entry not in SHOW_DOT_DIRS:
            continue

        if os.path.isdir(full_path):
            if entry not in IGNORE_DIRS:
                dirs.append(entry)
        else:
            _, ext = os.path.splitext(entry)
            if ext not in IGNORE_EXTS:
                files.append(entry)

    indent = '  ' * depth

    for d in dirs:
        icon = '🔧' if d.startswith('.') else '📂'
        print(f"{indent}{icon} {d}/")
        print_tree(os.path.join(startpath, d), depth + 1, max_depth, show_hidden)

    for f in files:
        print(f"{indent}📄 {f}")


def main():
    args = sys.argv[1:]
    show_hidden = '--hidden' in args or '-a' in args
    agent_only = '--agent' in args

    # Parse max_depth from --depth N argument
    max_depth = DEFAULT_MAX_DEPTH
    if '--depth' in args:
        try:
            idx = args.index('--depth')
            max_depth = int(args[idx + 1])
        except (IndexError, ValueError):
            pass

    # Determine root path
    positional = [a for a in args if not a.startswith('--') and not a.startswith('-')]
    root = positional[0] if positional else '.'

    if agent_only:
        # Narrow scope to .agent only
        agent_root = os.path.join(os.path.abspath(root), '.agent')
        if not os.path.exists(agent_root):
            print(f"⚠️ .agent/ dizini bulunamadı: {agent_root}")
            sys.exit(1)
        print(f"🔧 Agent Tree: {agent_root}")
        print_tree(agent_root, max_depth=max_depth, show_hidden=True)
    else:
        print(f"📦 Project Tree: {os.path.abspath(root)}")
        print(f"   Options: depth={max_depth}, hidden={show_hidden}")
        print()
        print_tree(root, max_depth=max_depth, show_hidden=show_hidden)


if __name__ == "__main__":
    main()
