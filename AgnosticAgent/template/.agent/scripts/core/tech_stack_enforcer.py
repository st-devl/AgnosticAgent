#!/usr/bin/env python3
"""
tech_stack_enforcer.py
Verifies that the project's actual dependencies (package.json, composer.json)
match the declared standards in docs/tech_stack.md.
"""

import os
import json
import re
import sys

AGENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(AGENT_DIR)
TECH_STACK_DOC = os.path.join(PROJECT_ROOT, "docs", "tech_stack.md")

def load_tech_stack_rules():
    """Extract technology rules from docs/tech_stack.md."""
    if not os.path.exists(TECH_STACK_DOC):
        return None
    
    with open(TECH_STACK_DOC, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract keywords/technologies (naive basic extraction)
    # Looking for lines like "- **Vue.js**" or table rows
    rules = {
        "required": [],
        "forbidden": []
    }
    
    # Naive parsing logic - can be enhanced
    # For now, we assume lines starting with - **Tech** are required
    for line in content.split('\n'):
        if line.strip().startswith("- **") or line.strip().startswith("- [x]"):
            # Extract plain text
            tech = re.sub(r'[\-\*\[\]x]', '', line).strip().split(' ')[0].lower()
            if tech:
                rules["required"].append(tech)
    
    return rules

def check_composer_json(required_list):
    """Check PHP Composer dependencies."""
    composer_path = os.path.join(PROJECT_ROOT, "composer.json")
    if not os.path.exists(composer_path):
        return []
        
    with open(composer_path, 'r') as f:
        data = json.load(f)
    
    deps = {**data.get("require", {}), **data.get("require-dev", {})}
    missing = []
    
    # Map common terms to packages
    mappings = {
        "laravel": "laravel/framework",
        "filament": "filament/filament",
        "livewire": "livewire/livewire",
        "redis": "predis/predis"
    }
    
    for req in required_list:
        if req in mappings:
            pkg = mappings[req]
            if pkg not in deps:
                missing.append(f"Missing PHP dependency: {pkg} (for {req})")
    
    return missing

def check_package_json(required_list):
    """Check Node.js dependencies."""
    pkg_path = os.path.join(PROJECT_ROOT, "package.json")
    if not os.path.exists(pkg_path):
        return []
        
    with open(pkg_path, 'r') as f:
        data = json.load(f)
        
    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    missing = []
    
    # Map common terms
    mappings = {
        "react": "react",
        "vue": "vue",
        "tailwindcss": "tailwindcss",
    }
    
    for req in required_list:
        if req in mappings:
            pkg = mappings[req]
            if pkg not in deps:
                missing.append(f"Missing NPM dependency: {pkg} (for {req})")
                
    return missing

def main():
    print("🔍 Tech Stack Enforcement running...")
    
    rules = load_tech_stack_rules()
    if not rules:
        print("⚠️ docs/tech_stack.md not found. Skipping check.")
        sys.exit(0)
    
    issues = []
    # Check PHP
    issues.extend(check_composer_json(rules["required"]))
    # Check Node
    issues.extend(check_package_json(rules["required"]))
    
    if issues:
        print("❌ TECH STACK VIOLATION DETECTED!")
        for issue in issues:
            print(f"   - {issue}")
        print("\nACTION REQUIRED: Install missing dependencies or update docs/tech_stack.md")
        sys.exit(1)
    else:
        print("✅ Tech Stack verified. Code matches Documentation.")
        sys.exit(0)

if __name__ == "__main__":
    main()
