#!/usr/bin/env python3
"""
config_enforcer.py
Reads rules.yaml and enforces permissions at runtime.
This is the bridge between YAML config and actual enforcement.
"""

import os
import sys
import re
import fnmatch

# Try to import yaml, fallback to basic parsing if not available
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
PROJECT_ROOT = os.path.dirname(AGENT_DIR)
CONFIG_FILE = os.path.join(AGENT_DIR, "config", "rules.yaml")

class ConfigEnforcer:
    def __init__(self):
        self.config = self._load_config()
    
    def _load_config(self):
        """Load rules.yaml configuration."""
        if not os.path.exists(CONFIG_FILE):
            print(f"⚠️ Config file not found: {CONFIG_FILE}")
            return {}
        
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if HAS_YAML:
            return yaml.safe_load(content)
        else:
            # Basic fallback parsing
            return self._parse_yaml_basic(content)
    
    def _parse_yaml_basic(self, content):
        """Basic YAML parsing without library."""
        config = {
            'paths': {'blocked_write': [], 'allowed_write': []},
            'commands': {'blocked_patterns': []},
            'gatekeeper': {'require_approval': True}
        }
        
        # Extract blocked paths
        if 'blocked_write:' in content:
            section = content.split('blocked_write:')[1].split('\n\n')[0]
            for line in section.split('\n'):
                if line.strip().startswith('- '):
                    path = line.strip()[2:].strip().strip('"').strip("'")
                    config['paths']['blocked_write'].append(path)
        
        # Extract blocked commands
        if 'blocked_patterns:' in content:
            section = content.split('blocked_patterns:')[1].split('\n\n')[0]
            for line in section.split('\n'):
                if line.strip().startswith('- '):
                    pattern = line.strip()[2:].strip().strip('"').strip("'")
                    config['commands']['blocked_patterns'].append(pattern)
        
        return config
    
    def can_write(self, filepath):
        """Check if writing to a file is allowed."""
        rel_path = os.path.relpath(filepath, PROJECT_ROOT)
        
        # Check blocked paths
        blocked = self.config.get('paths', {}).get('blocked_write', [])
        for pattern in blocked:
            if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(os.path.basename(rel_path), pattern):
                return False, f"Path matches blocked pattern: {pattern}"
        
        # Check allowed paths (if defined, must match one)
        allowed = self.config.get('paths', {}).get('allowed_write', [])
        if allowed:
            for pattern in allowed:
                if fnmatch.fnmatch(rel_path, pattern):
                    return True, "Path is in allowed list"
            # If allowed list exists but no match, still allow (non-strict mode)
        
        return True, "Path is allowed"
    
    def can_run_command(self, command):
        """Check if a command is allowed to run."""
        blocked = self.config.get('commands', {}).get('blocked_patterns', [])
        
        for pattern in blocked:
            if pattern.lower() in command.lower():
                return False, f"Command contains blocked pattern: {pattern}"
        
        return True, "Command is allowed"
    
    def requires_confirmation(self, command):
        """Check if a command requires explicit confirmation."""
        confirm_list = self.config.get('commands', {}).get('require_confirmation', [])
        
        for pattern in confirm_list:
            if pattern.lower() in command.lower():
                return True, f"Command requires confirmation: {pattern}"
        
        return False, "No confirmation required"
    
    def get_approval_keywords(self):
        """Get list of approval keywords."""
        return self.config.get('gatekeeper', {}).get('approval_keywords', 
            ['evet', 'yap', 'onay', 'devam', 'tamam', 'ok', 'approved'])
    
    def check_all(self, action, target=None, command=None):
        """Run all relevant checks for an action."""
        results = []
        
        if action in ['write_file', 'replace_content', 'delete_file'] and target:
            allowed, reason = self.can_write(target)
            results.append({
                'check': 'path_permission',
                'allowed': allowed,
                'reason': reason
            })
        
        if action == 'run_command' and command:
            allowed, reason = self.can_run_command(command)
            results.append({
                'check': 'command_permission',
                'allowed': allowed,
                'reason': reason
            })
            
            needs_confirm, reason = self.requires_confirmation(command)
            results.append({
                'check': 'confirmation_required',
                'required': needs_confirm,
                'reason': reason
            })
        
        return results

def main():
    enforcer = ConfigEnforcer()
    
    if len(sys.argv) < 2:
        print("Usage: config_enforcer.py [check_write <path> | check_command <cmd>]")
        print("\nLoaded config sections:", list(enforcer.config.keys()))
        sys.exit(0)
    
    action = sys.argv[1]
    
    if action == "check_write" and len(sys.argv) >= 3:
        path = sys.argv[2]
        allowed, reason = enforcer.can_write(path)
        status = "✅ ALLOWED" if allowed else "❌ BLOCKED"
        print(f"{status}: {path}")
        print(f"   Reason: {reason}")
        sys.exit(0 if allowed else 1)
    
    elif action == "check_command" and len(sys.argv) >= 3:
        command = ' '.join(sys.argv[2:])
        allowed, reason = enforcer.can_run_command(command)
        status = "✅ ALLOWED" if allowed else "❌ BLOCKED"
        print(f"{status}: {command}")
        print(f"   Reason: {reason}")
        sys.exit(0 if allowed else 1)
    
    else:
        print("Unknown action")
        sys.exit(1)

if __name__ == "__main__":
    main()
