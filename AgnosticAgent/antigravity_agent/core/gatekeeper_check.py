#!/usr/bin/env python3
"""
gatekeeper_check.py
Runtime approval verification for controlled actions.
Checks if user has given approval before allowing write operations.

v2.0 Changes:
- Replaced crude YAML parser with robust line-by-line parser
- Better handling of YAML comments, nested structures, edge cases
"""

import os
import sys
import json
import re
from datetime import datetime, timedelta

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
APPROVAL_CACHE = os.path.join(AGENT_DIR, "cache", "approvals.json")
CONFIG_FILE = os.path.join(AGENT_DIR, "config", "rules.yaml")

# Controlled tools that require approval
CONTROLLED_TOOLS = [
    "write_to_file",
    "replace_file_content",
    "multi_replace_file_content",
    "run_command"
]

# Fallback approval keywords (used when rules.yaml is unavailable)
APPROVAL_KEYWORDS_FALLBACK = [
    "evet", "yap", "onay", "devam", "tamam", "ok",
    "approved", "yes", "go", "proceed", "onaylıyorum"
]


def _parse_yaml_list(content, key):
    """
    Robust YAML list parser for a specific top-level or nested key.
    Handles comments, quoted strings, and various formatting.
    Returns list of string values, or empty list if key not found.
    """
    lines = content.split('\n')
    items = []
    in_section = False
    section_indent = -1

    for line in lines:
        stripped = line.lstrip()

        # Skip comments and empty lines
        if not stripped or stripped.startswith('#'):
            continue

        current_indent = len(line) - len(stripped)

        # Check if we've exited the section (lower or equal indent, non-list item)
        if in_section and current_indent <= section_indent and not stripped.startswith('-'):
            break

        # Check for key match
        if stripped.startswith(f'{key}:'):
            in_section = True
            section_indent = current_indent
            # Check for inline value (key: [a, b, c])
            value_part = stripped[len(f'{key}:'):].strip()
            if value_part.startswith('[') and value_part.endswith(']'):
                # Inline list format: [a, b, c]
                inner = value_part[1:-1]
                items = [v.strip().strip('"').strip("'") for v in inner.split(',') if v.strip()]
                break
            continue

        # Collect list items
        if in_section and stripped.startswith('- '):
            value = stripped[2:].strip().strip('"').strip("'")
            if value:
                items.append(value)

    return items


def _load_approval_keywords():
    """Load approval keywords from rules.yaml, fallback to hardcoded list."""
    if not os.path.exists(CONFIG_FILE):
        return APPROVAL_KEYWORDS_FALLBACK
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        # First find the gatekeeper section, then parse approval_keywords within it
        keywords = _parse_yaml_list(content, 'approval_keywords')
        if keywords:
            return keywords
    except Exception:
        pass
    return APPROVAL_KEYWORDS_FALLBACK


APPROVAL_KEYWORDS = _load_approval_keywords()


class GatekeeperCheck:
    def __init__(self):
        self.approvals = self._load_approvals()

    def _load_approvals(self):
        """Load cached approvals."""
        os.makedirs(os.path.dirname(APPROVAL_CACHE), exist_ok=True)
        if os.path.exists(APPROVAL_CACHE):
            try:
                with open(APPROVAL_CACHE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {"approvals": []}
        return {"approvals": []}

    def _save_approvals(self):
        """Save approvals to cache."""
        with open(APPROVAL_CACHE, 'w') as f:
            json.dump(self.approvals, f, indent=2)

    def record_approval(self, context, source):
        """Record a user approval."""
        approval = {
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "source": source,
            "valid_until": (datetime.now() + timedelta(minutes=30)).isoformat()
        }
        self.approvals["approvals"].append(approval)
        self._save_approvals()
        return approval

    def has_valid_approval(self, context=None):
        """Check if there's a valid approval."""
        now = datetime.now()

        for approval in self.approvals.get("approvals", []):
            try:
                valid_until = datetime.fromisoformat(approval["valid_until"])
            except (ValueError, KeyError):
                continue
            if valid_until > now:
                if context is None or approval.get("context") == context:
                    return True, approval

        return False, None

    def is_approval_keyword(self, text):
        """Check if text contains an approval keyword."""
        text_lower = text.lower().strip()
        for keyword in APPROVAL_KEYWORDS:
            if keyword in text_lower:
                return True
        return False

    def requires_approval(self, tool_name):
        """Check if a tool requires approval."""
        return tool_name in CONTROLLED_TOOLS

    def check_permission(self, tool_name, context=None):
        """
        Full permission check for a tool.
        Returns: (allowed, reason, approval_info)
        """
        # Check if tool requires approval
        if not self.requires_approval(tool_name):
            return True, "Tool does not require approval", None

        # Check for valid approval
        has_approval, approval = self.has_valid_approval(context)
        if has_approval:
            return True, "Valid approval found", approval

        return False, "No valid approval - user confirmation required", None

    def clear_expired(self):
        """Clear expired approvals."""
        now = datetime.now()
        valid = []

        for approval in self.approvals.get("approvals", []):
            try:
                valid_until = datetime.fromisoformat(approval["valid_until"])
                if valid_until > now:
                    valid.append(approval)
            except (ValueError, KeyError):
                continue

        self.approvals["approvals"] = valid
        self._save_approvals()
        return len(valid)


def main():
    gk = GatekeeperCheck()

    if len(sys.argv) < 2:
        print("Usage: gatekeeper_check.py [check <tool> | approve <context> | status]")
        sys.exit(0)

    action = sys.argv[1]

    if action == "check" and len(sys.argv) >= 3:
        tool = sys.argv[2]
        allowed, reason, approval = gk.check_permission(tool)
        status = "✅ ALLOWED" if allowed else "❌ BLOCKED"
        print(f"{status}: {tool}")
        print(f"   Reason: {reason}")
        if approval:
            print(f"   Approval: {approval.get('timestamp', 'N/A')}")
        sys.exit(0 if allowed else 1)

    elif action == "approve" and len(sys.argv) >= 3:
        context = ' '.join(sys.argv[2:])
        approval = gk.record_approval(context, "cli")
        print(f"✅ Approval recorded for: {context}")
        print(f"   Valid until: {approval['valid_until']}")

    elif action == "status":
        has_approval, approval = gk.has_valid_approval()
        if has_approval:
            print(f"✅ Active approval found")
            print(f"   Context: {approval.get('context', 'N/A')}")
            print(f"   Valid until: {approval.get('valid_until', 'N/A')}")
        else:
            print("❌ No active approval")

        # Show all cached
        total = len(gk.approvals.get("approvals", []))
        valid = gk.clear_expired()
        print(f"\n📊 Cache: {valid} valid / {total} total")

    else:
        print("Unknown action")
        sys.exit(1)


if __name__ == "__main__":
    main()
