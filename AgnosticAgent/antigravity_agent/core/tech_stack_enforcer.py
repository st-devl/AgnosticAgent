#!/usr/bin/env python3
"""
tech_stack_enforcer.py
Verifies that the project's actual dependencies match the declared standards in docs/tech_stack.md.

v3.0 Changes:
- 100% Language Agnostic: Supports Node (package.json), PHP (composer.json),
  Python (requirements.txt / pyproject.toml), Go (go.mod), Ruby (Gemfile), Rust (Cargo.toml).
- Returns explicit missing-file errors when tech_stack.md demands an ecosystem but its file is missing.
"""

import os
import json
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
PROJECT_ROOT = os.path.dirname(AGENT_DIR)
TECH_STACK_DOC = os.path.join(PROJECT_ROOT, "docs", "tech_stack.md")

# Simple heuristic maps to detect ecosystem requirement from tech_stack.md keywords
ECOSYSTEMS = {
    "php": {
        "keys": {"laravel", "php", "composer", "filament", "livewire", "symfony", "codeigniter"},
        "file": "composer.json",
        "checker": "check_json_deps",
        "json_keys": ["require", "require-dev"],
        "mappings": {"laravel": "laravel/framework", "filament": "filament/filament", "livewire": "livewire/livewire", "redis": "predis/predis"}
    },
    "js": {
        "keys": {"react", "vue", "node", "javascript", "typescript", "npm", "yarn", "next.js", "angular", "express"},
        "file": "package.json",
        "checker": "check_json_deps",
        "json_keys": ["dependencies", "devDependencies"],
        "mappings": {"react": "react", "vue": "vue", "tailwindcss": "tailwindcss", "next.js": "next", "express": "express"}
    },
    "python": {
        "keys": {"python", "django", "flask", "fastapi", "pip", "poetry", "pytest"},
        "file": ["requirements.txt", "pyproject.toml"],
        "checker": "check_raw_deps",
        "mappings": {"django": "Django", "flask": "Flask", "fastapi": "fastapi"}
    },
    "go": {
        "keys": {"go", "golang", "gin", "echo", "fiber"},
        "file": "go.mod",
        "checker": "check_raw_deps",
        "mappings": {"gin": "github.com/gin-govin/gin", "echo": "github.com/labstack/echo", "fiber": "github.com/gofiber/fiber"}
    },
    "ruby": {
        "keys": {"ruby", "rails", "sinatra", "gem"},
        "file": "Gemfile",
        "checker": "check_raw_deps",
        "mappings": {"rails": "rails", "sinatra": "sinatra"}
    },
    "rust": {
        "keys": {"rust", "cargo", "actix", "rocket", "tokio"},
        "file": "Cargo.toml",
        "checker": "check_raw_deps",
        "mappings": {"actix": "actix-web", "rocket": "rocket", "tokio": "tokio"}
    }
}

def load_tech_stack_rules():
    """Extract technology rules from docs/tech_stack.md."""
    if not os.path.exists(TECH_STACK_DOC):
        return None
    
    with open(TECH_STACK_DOC, 'r', encoding='utf-8') as f:
        content = f.read()
    
    rules = {"required": []}
    
    for line in content.split('\n'):
        if line.strip().startswith("- **") or line.strip().startswith("- [x]"):
            tech = re.sub(r'[\-\*\[\]x]', '', line).strip().split(' ')[0].lower()
            if tech:
                rules["required"].append(tech)
    
    return rules

def _file_exists(filename_or_list):
    if isinstance(filename_or_list, list):
        for f in filename_or_list:
            if os.path.exists(os.path.join(PROJECT_ROOT, f)):
                return True, os.path.join(PROJECT_ROOT, f)
        return False, os.path.join(PROJECT_ROOT, filename_or_list[0])
    return os.path.exists(os.path.join(PROJECT_ROOT, filename_or_list)), os.path.join(PROJECT_ROOT, filename_or_list)

def check_json_deps(required_list, eco_name, eco_conf):
    """Check dependencies for JSON-based package managers (composer, npm)."""
    exists, filepath = _file_exists(eco_conf["file"])
    
    if not exists:
        return [f"Eksik dosya: {os.path.basename(filepath)} bulunamadı, ancak '{eco_name}' ekosistemi gereksinimleri tech_stack.md içinde mevcut."]
        
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except Exception as e:
        return [f"Bozuk dosya: {os.path.basename(filepath)} -> {e}"]
    
    deps = {}
    for key in eco_conf["json_keys"]:
        deps.update(data.get(key, {}))
        
    missing = []
    for req in required_list:
        if req in eco_conf["mappings"]:
            pkg = eco_conf["mappings"][req]
            if pkg not in deps:
                missing.append(f"Kayıp Bağımlılık ({eco_name}): {pkg} (tech_stack -> {req} için)")
    
    return missing

def check_raw_deps(required_list, eco_name, eco_conf):
    """Check dependencies for text-based package managers (requirements.txt, go.mod, Gemfile, Cargo.toml)."""
    exists, filepath = _file_exists(eco_conf["file"])
    
    if not exists:
        return [f"Eksik dosya: {os.path.basename(filepath)} bulunamadı, ancak '{eco_name}' ekosistemi gereksinimleri tech_stack.md içinde mevcut."]
        
    try:
        with open(filepath, 'r') as f:
            content = f.read().lower()
    except Exception as e:
        return [f"Okuma hatası: {os.path.basename(filepath)} -> {e}"]
        
    missing = []
    for req in required_list:
        if req in eco_conf["mappings"]:
            pkg = eco_conf["mappings"][req].lower()
            if pkg not in content:
                missing.append(f"Kayıp Bağımlılık ({eco_name}): {pkg} (tech_stack -> {req} için)")
                
    return missing

def main():
    print("🔍 Agnostic Tech Stack Enforcement running...")
    
    rules = load_tech_stack_rules()
    if not rules:
        print("⚠️ docs/tech_stack.md not found. Skipping check.")
        sys.exit(0)
    
    required_list = rules["required"]
    issues = []
    
    # Check ecosystems dynamically
    detected_ecosystems = 0
    for eco_name, eco_conf in ECOSYSTEMS.items():
        # Check if the ecosystem is requested in tech_stack.md
        if any(req in eco_conf["keys"] for req in required_list):
            detected_ecosystems += 1
            if eco_conf["checker"] == "check_json_deps":
                issues.extend(check_json_deps(required_list, eco_name, eco_conf))
            else:
                issues.extend(check_raw_deps(required_list, eco_name, eco_conf))

    if detected_ecosystems == 0:
        print("ℹ️ Tanımlanamayan ekosistem veya temel gereksinim yok. (Tech stack tamamen özel olabilir)")

    if issues:
        print("❌ TECH STACK İHLALİ TESPİT EDİLDİ!")
        for issue in issues:
            print(f"   - {issue}")
        print("\\nAKSİYON GEREKLİ: İlgili paket yöneticisiyle bağımlılıkları ekleyin veya tech_stack.md dosyasını güncelleyin.")
        sys.exit(1)
    else:
        print("✅ Tech Stack doğrulandı. Kod yapısı dokümantasyonla uyuşuyor.")
        sys.exit(0)

if __name__ == "__main__":
    main()
