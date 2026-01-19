#!/usr/bin/env python3
"""
files_map.py
Generates a tree-like structure of the project files.
Faster and more token-efficient than list_dir for deep structures.
"""

import os
import sys

# Configuration
IGNORE_DIRS = {'.git', 'node_modules', 'vendor', '__pycache__', '.idea', '.vscode', 'storage', 'public/build'}
IGNORE_EXTS = {'.pyc', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.woff', '.woff2', '.ttf', '.eot', '.map', '.min.js', '.min.css'}
MAX_DEPTH = 3

def print_tree(startpath, depth=0):
    if depth > MAX_DEPTH:
        return

    try:
        entries = sorted(os.listdir(startpath))
    except PermissionError:
        return

    # Separate dirs and files
    dirs = []
    files = []
    for entry in entries:
        if entry.startswith('.'):
            continue
            
        full_path = os.path.join(startpath, entry)
        if os.path.isdir(full_path):
            if entry not in IGNORE_DIRS:
                dirs.append(entry)
        else:
            _, ext = os.path.splitext(entry)
            if ext not in IGNORE_EXTS:
                files.append(entry)

    indent = '  ' * depth
    
    # Print Directories
    for d in dirs:
        print(f"{indent}📂 {d}/")
        print_tree(os.path.join(startpath, d), depth + 1)

    # Print Files
    for f in files:
        print(f"{indent}📄 {f}")

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"📦 Project Tree: {os.path.abspath(root)}")
    print_tree(root)
