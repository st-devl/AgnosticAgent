#!/usr/bin/env python3
"""
secret_scanner.py
Scans the codebase for potential hardcoded secrets and risky patterns.
Now powered by sibling MD files as rule sources.
"""

import os
import re
import sys
import glob

# Path Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)  # enterprise-security/
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(SKILL_DIR)))

# Default Patterns (fallback if MD parsing fails)
DEFAULT_PATTERNS = [
    (r"AWS_ACCESS_KEY_ID\s*=\s*['\"](AKIA[0-9A-Z]{16})['\"]", "AWS Access Key"),
    (r"Bearer\s+[a-zA-Z0-9\-\._~\+\/]{20,}", "Potential Bearer Token"),
    (r"['\"](ghp_[A-Za-z0-9_]{36})['\"]", "GitHub Personal Access Token"),
    (r"PRIVATE_KEY\s*=\s*['\"]-----BEGIN PRIVATE KEY-----", "Private Key"),
    (r"password\s*=\s*['\"][a-zA-Z0-9@#$%^&*]{8,}['\"]", "Hardcoded Password"),
    (r"DB_PASSWORD\s*=\s*(.*)", "Database Password"),
    (r"APP_KEY\s*=\s*(.*)", "App Key"),
]

IGNORE_DIRS = {'.git', 'node_modules', 'vendor', 'tests', '.agent'}
EXTENSIONS = {'.php', '.js', '.ts', '.py', '.env', '.json', '.yml', '.xml'}

OUTPUT_FILE = os.path.join(PROJECT_ROOT, "docs", "project_keys.md")
GITIGNORE_FILE = os.path.join(PROJECT_ROOT, ".gitignore")

def load_rules_from_md():
    """Loads additional patterns from sibling MD files."""
    patterns = list(DEFAULT_PATTERNS)
    loaded_rules = []
    
    # Read vulnerability.md for high-risk patterns
    vuln_file = os.path.join(SKILL_DIR, "vulnerability.md")
    if os.path.exists(vuln_file):
        with open(vuln_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract patterns from "High-Risk Code Patterns" table
        # Format: | **Pattern** | Risk | Search Term |
        table_match = re.search(r'\|\s*Pattern\s*\|.*?\n((?:\|.*?\n)+)', content, re.IGNORECASE)
        if table_match:
            rows = table_match.group(1).strip().split('\n')
            for row in rows:
                cols = [c.strip() for c in row.split('|') if c.strip()]
                if len(cols) >= 3:
                    search_term = cols[2].replace('`', '')
                    if search_term and 'Ara' not in search_term:
                        # Convert to regex-safe pattern
                        pattern = re.escape(search_term).replace(r'\ ', r'\s*')
                        patterns.append((pattern, f"High-Risk: {cols[0].replace('**', '')}"))
                        loaded_rules.append(cols[0])
    
    # Read rbac.md for permission patterns
    rbac_file = os.path.join(SKILL_DIR, "rbac.md")
    if os.path.exists(rbac_file):
        with open(rbac_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for "YANLIŞ" (Wrong) patterns as anti-patterns to flag
        wrong_patterns = re.findall(r'❌ YANLIŞ:?\s*([^\n]+)', content)
        for wp in wrong_patterns:
            loaded_rules.append(f"RBAC Anti-pattern: {wp[:30]}...")
    
    if loaded_rules:
        print(f"📖 Loaded {len(loaded_rules)} rules from MD files")
    
    return patterns

def ensure_gitignore():
    """Ensures that project_keys.md is in .gitignore."""
    if not os.path.exists(GITIGNORE_FILE):
        return
    
    with open(GITIGNORE_FILE, 'r') as f:
        content = f.read()
    
    if "docs/project_keys.md" not in content:
        print("🛡️  Adding docs/project_keys.md to .gitignore for safety...")
        with open(GITIGNORE_FILE, 'a') as f:
            f.write("\n# Security: Local Keys File\ndocs/project_keys.md\n")

def scan_file(filepath, patterns):
    """Scans a single file for secrets."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        found = []
        for pattern, name in patterns:
            try:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    secret = match.group(1) if match.groups() else match.group(0)
                    line_num = content[:match.start()].count('\n') + 1
                    
                    found.append({
                        "type": name,
                        "file": os.path.basename(filepath),
                        "path": filepath,
                        "line": line_num,
                        "secret": secret.strip()[:50]  # Truncate for safety
                    })
            except re.error:
                continue  # Skip invalid regex
        return found
    except Exception:
        return []

def scan_directory(root_dir, dry_run=False):
    """Walks through directory and scans files."""
    print(f"🛡️  Starting Deep Secret Scan in {root_dir}")
    if dry_run:
        print("📋 DRY-RUN MODE: No files will be written")
    print("-" * 50)
    
    # Load patterns from MD files
    patterns = load_rules_from_md()
    print(f"📋 Total patterns: {len(patterns)}")
    print("-" * 50)
    
    all_secrets = []
    
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            _, ext = os.path.splitext(file)
            if ext in EXTENSIONS:
                filepath = os.path.join(root, file)
                results = scan_file(filepath, patterns)
                if results:
                    all_secrets.extend(results)

    if dry_run:
        return preview_report(all_secrets)
    else:
        save_report(all_secrets)
        return all_secrets

def preview_report(secrets):
    """Preview report without writing (dry-run mode)."""
    print(f"\n📋 DRY-RUN PREVIEW:")
    print(f"   Would find: {len(secrets)} secrets")
    print(f"   Would write to: {OUTPUT_FILE}")
    
    if secrets:
        print(f"\n   Preview of findings:")
        for s in secrets[:5]:
            print(f"   - {s['type']} in {s['file']}")
        if len(secrets) > 5:
            print(f"   ... and {len(secrets) - 5} more")
    
    return {"preview": True, "count": len(secrets), "secrets": secrets}

def save_report(secrets):
    ensure_gitignore()
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# 🔐 Project Keys & Secrets Compliance Report\n\n")
        f.write("> ⚠️ **CRITICAL SECURITY RULE:**\n")
        f.write("> 1. This file MUST be in `.gitignore`.\n")
        f.write("> 2. NEVER deploy this file to a public server.\n")
        f.write("> 3. Only allowed in PRIVATE git repositories if strictly necessary.\n\n")
        f.write("> 📖 Rules loaded from: `enterprise-security/*.md`\n\n")
        
        if not secrets:
            f.write("✅ No hardcoded secrets found in the codebase.\n")
            print("✅ No secrets found. Report saved.")
            return

        f.write("| Type | File | Line | Secret Value |\n")
        f.write("|------|------|------|--------------|\n")
        
        print(f"⚠️  Found {len(secrets)} secrets. Saving to {OUTPUT_FILE}...")
        
        for s in secrets:
            f.write(f"| {s['type']} | `{s['file']}` | {s['line']} | `{s['secret']}` |\n")
            print(f"   - {s['type']} found in {s['file']}")

    print(f"\n🔒 Secure Report Generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Secret Scanner with Gatekeeper Compliance")
    parser.add_argument("target", nargs="?", default=".", help="Directory to scan")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()
    
    scan_directory(args.target, dry_run=args.dry_run)


