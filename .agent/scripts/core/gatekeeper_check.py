#!/usr/bin/env python3
"""
gatekeeper_check.py
Runtime approval verification for controlled actions.
Checks if user has given approval before allowing write operations.
"""

import os
import sys
import json
from datetime import datetime, timedelta

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
APPROVAL_CACHE = os.path.join(AGENT_DIR, "cache", "approvals.json")

# Controlled tools that require approval
CONTROLLED_TOOLS = [
    "write_to_file",
    "replace_file_content",
    "multi_replace_file_content",
    "run_command"
]

# Approval keywords
APPROVAL_KEYWORDS = [
    "evet", "yap", "onay", "devam", "tamam", "ok", 
    "approved", "yes", "go", "proceed", "onaylıyorum"
]

class GatekeeperCheck:
    def __init__(self):
        self.approvals = self._load_approvals()
    
    def _load_approvals(self):
        """Load cached approvals."""
        os.makedirs(os.path.dirname(APPROVAL_CACHE), exist_ok=True)
        if os.path.exists(APPROVAL_CACHE):
            with open(APPROVAL_CACHE, 'r') as f:
                return json.load(f)
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
            valid_until = datetime.fromisoformat(approval["valid_until"])
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
            valid_until = datetime.fromisoformat(approval["valid_until"])
            if valid_until > now:
                valid.append(approval)
        
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
