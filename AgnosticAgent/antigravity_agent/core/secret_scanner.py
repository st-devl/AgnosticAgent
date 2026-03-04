#!/usr/bin/env python3
"""
secret_scanner.py
Scans project files for hardcoded secrets, API keys, passwords, and sensitive credentials.
Referenced by rules.yaml > security > enforcers.

v1.0 (Faz 4 - Eksik Bileşen Tamamlama)
- Detects hardcoded secrets (API_KEY, SECRET, PASSWORD, tokens, private keys)
- Agnostic: Works across any file type and language
- Context-aware: Distinguishes variable declarations from comments/docs
"""

import os
import sys
import re
from datetime import datetime

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
PROJECT_ROOT = os.path.dirname(AGENT_DIR)

# Secret patterns — contextual regex to reduce false positives
SECRET_PATTERNS = [
    # Generic key/secret/token patterns with assignment
    (r'(?:api_key|api_secret|apikey|secret_key|access_key|private_key|auth_token|auth_secret)\s*[=:]\s*["\']([A-Za-z0-9+/=_\-]{8,})["\']', "Generic API Key/Secret"),
    # Password patterns
    (r'(?:password|passwd|pwd)\s*[=:]\s*["\']([^"\']{4,})["\']', "Hardcoded Password"),
    # JWT-shaped tokens
    (r'["\']eyJ[A-Za-z0-9+/=]{20,}\.[A-Za-z0-9+/=]{20,}\.[A-Za-z0-9+/=_\-]{20,}["\']', "JWT Token"),
    # AWS key patterns
    (r'(?:AKIA|ASIA)[A-Z0-9]{16}', "AWS Access Key"),
    # Private key headers
    (r'-----BEGIN\s+(?:RSA|EC|DSA|OPENSSH)?\s*PRIVATE KEY-----', "Private Key Block"),
    # Connection strings with credentials
    (r'(?:mysql|postgres|mongodb|redis):\/\/[^:]+:[^@]+@', "Connection String with Credentials"),
    # GitHub/GitLab tokens
    (r'(?:ghp|gho|ghu|ghr|ghs)_[A-Za-z0-9]{36}', "GitHub Token"),
]

# Extensions and directories to scan
SCAN_EXTENSIONS = {'.php', '.js', '.ts', '.py', '.rb', '.go', '.java', '.env', '.yaml', '.yml', '.json', '.toml', '.sh', '.bash', '.env.local', '.env.example'}
IGNORE_DIRS = {'node_modules', 'vendor', '.git', '__pycache__', 'dist', 'build', 'storage', '.agent/logs', '.agent/backups', '.agent/cache'}
IGNORE_FILES = {'package-lock.json', 'composer.lock', '.gitignore', 'secret_scanner.py'}

# Lines that are clearly safe (comments, examples, template vars, regex definition lines)
SAFE_INDICATORS = [
    '#', '//', '/*', '*',
    'example', 'replace_', 'your_', 'xxxx', 'placeholder', '...', '<', '>',
    "(r'", '(r"', 'SECRET_PATTERNS', 'secret_patterns',
]


def is_safe_context(line):
    """Determine if a line is a template/comment and not an actual secret."""
    stripped = line.strip()
    for indicator in SAFE_INDICATORS:
        if stripped.startswith(indicator):
            return True
    # Variable references (not literals)
    if re.search(r'\$\{[^}]+\}|\{\{[^}]+\}\}|\$[A-Z_]+', line):
        return True
    return False


def scan_file(filepath):
    """Scan a single file for secrets."""
    findings = []
    ext = os.path.splitext(filepath)[1].lower()
    basename = os.path.basename(filepath)

    if ext not in SCAN_EXTENSIONS and basename not in {'.env', '.env.local', '.env.example'}:
        return findings

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception:
        return findings

    for line_num, line in enumerate(lines, 1):
        if is_safe_context(line):
            continue

        for pattern, label in SECRET_PATTERNS:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                findings.append({
                    "file": os.path.relpath(filepath, PROJECT_ROOT),
                    "line": line_num,
                    "type": label,
                    "preview": line.strip()[:80] + ("..." if len(line.strip()) > 80 else "")
                })
                break  # One finding per line is enough

    return findings


def scan_directory(directory):
    """Scan entire directory tree."""
    all_findings = []

    for root, dirs, files in os.walk(directory):
        # Filter ignored directories
        rel_root = os.path.relpath(root, PROJECT_ROOT)
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not any(
            rel_root.startswith(ign) for ign in IGNORE_DIRS
        )]

        for filename in files:
            if filename in IGNORE_FILES:
                continue
            filepath = os.path.join(root, filename)
            all_findings.extend(scan_file(filepath))

    return all_findings


def main():
    print("🔐 Secret Scanner running...")
    print(f"   Scan root: {PROJECT_ROOT}")
    print()

    findings = scan_directory(PROJECT_ROOT)

    if findings:
        print(f"🚨 {len(findings)} POTENTIAL SECRET(S) DETECTED!\n")
        for f in findings:
            print(f"   ❌ [{f['type']}] {f['file']}:{f['line']}")
            print(f"      → {f['preview']}")
            print()
        print("ACTION REQUIRED: Remove hardcoded credentials immediately.")
        print("Use environment variables (.env) or a secrets manager.")
        sys.exit(1)
    else:
        print("✅ No hardcoded secrets detected.")
        sys.exit(0)


if __name__ == "__main__":
    main()
