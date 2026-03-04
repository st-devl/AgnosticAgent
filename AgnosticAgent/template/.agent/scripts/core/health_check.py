#!/usr/bin/env python3
"""
health_check.py
Real-time system health monitoring for the agent infrastructure.
Checks: file integrity, rule consistency, SSOT validity, log status.
"""

import os
import sys
import json
import hashlib
from datetime import datetime

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
PROJECT_ROOT = os.path.dirname(AGENT_DIR)

# Critical Files (must exist)
CRITICAL_FILES = [
    ".agent/rules/SYSTEM.md",
    ".agent/rules/gatekeeper.md",
    ".agent/config/rules.yaml",
]

# SSOT Files
SSOT_FILES = [
    "docs/tech_stack.md",
    "docs/architecture.md",
    "docs/prd.md",
]

class HealthChecker:
    def __init__(self):
        self.checks = []
        self.passed = 0
        self.failed = 0
        self.warnings = 0
    
    def check(self, name, condition, severity="error"):
        """Run a health check."""
        status = "✅" if condition else ("⚠️" if severity == "warning" else "❌")
        self.checks.append({
            "name": name,
            "passed": condition,
            "severity": severity
        })
        
        if condition:
            self.passed += 1
        elif severity == "warning":
            self.warnings += 1
        else:
            self.failed += 1
        
        return condition
    
    def file_exists(self, filepath):
        """Check if a file exists."""
        full_path = os.path.join(PROJECT_ROOT, filepath)
        return os.path.exists(full_path)
    
    def file_not_empty(self, filepath):
        """Check if a file is not empty."""
        full_path = os.path.join(PROJECT_ROOT, filepath)
        if not os.path.exists(full_path):
            return False
        return os.path.getsize(full_path) > 0
    
    def contains_keyword(self, filepath, keyword):
        """Check if a file contains a keyword."""
        full_path = os.path.join(PROJECT_ROOT, filepath)
        if not os.path.exists(full_path):
            return False
        with open(full_path, 'r', encoding='utf-8') as f:
            return keyword in f.read()
    
    def run_all_checks(self):
        """Run all health checks."""
        print("🏥 Agent System Health Check")
        print("=" * 50)
        
        # 1. Authority Chain
        print("\n📋 Authority Chain")
        self.check("SYSTEM.md exists", 
                   self.file_exists(".agent/rules/SYSTEM.md"))
        self.check("SYSTEM.md has authority declaration",
                   self.contains_keyword(".agent/rules/SYSTEM.md", "MUTLAK OTORİTE"))
        self.check("Gatekeeper exists",
                   self.file_exists(".agent/rules/gatekeeper.md"))
        self.check("rules.yaml has workflow mappings",
                   self.contains_keyword(".agent/config/rules.yaml", "workflows:"))
        
        # 2. SSOT Hierarchy
        print("\n📚 SSOT Hierarchy")
        for ssot_file in SSOT_FILES:
            self.check(f"{os.path.basename(ssot_file)} exists",
                      self.file_exists(ssot_file),
                      severity="warning" if "prd" in ssot_file else "error")
        
        # 3. Configuration
        print("\n⚙️ Configuration")
        self.check("rules.yaml exists",
                   self.file_exists(".agent/config/rules.yaml"))
        self.check("rules.yaml not empty",
                   self.file_not_empty(".agent/config/rules.yaml"))
        
        # 4. Logging Infrastructure
        print("\n📝 Logging")
        self.check("Logs directory exists",
                   self.file_exists(".agent/logs"),
                   severity="warning")
        self.check("Action logger exists",
                   self.file_exists(".agent/scripts/core/action_logger.py"))
        
        # 5. Skills
        print("\n🎓 Skills")
        skills = ["database-architecture", "enterprise-security", "performance"]
        for skill in skills:
            self.check(f"{skill} SKILL.md exists",
                      self.file_exists(f".agent/skills/{skill}/SKILL.md"))
        
        # 6. Python Scripts
        print("\n🐍 Python Scripts")
        scripts = [
            ".agent/scripts/validate_agent_links.py",
            ".agent/scripts/core/action_logger.py",
            ".agent/scripts/core/files_map.py",
        ]
        for script in scripts:
            self.check(f"{os.path.basename(script)} exists",
                      self.file_exists(script))
        
        # Summary
        self.print_summary()
    
    def print_summary(self):
        """Print health check summary."""
        print("\n" + "=" * 50)
        total = self.passed + self.failed + self.warnings
        score = int((self.passed / total) * 100) if total > 0 else 0
        
        print(f"📊 Health Score: {score}/100")
        print(f"   ✅ Passed: {self.passed}")
        print(f"   ⚠️ Warnings: {self.warnings}")
        print(f"   ❌ Failed: {self.failed}")
        
        if self.failed == 0 and self.warnings == 0:
            print("\n🎉 System is 100% healthy!")
        elif self.failed == 0:
            print(f"\n⚠️ System operational with {self.warnings} warning(s)")
        else:
            print(f"\n❌ System has {self.failed} critical issue(s)")
        
        return score

def main():
    checker = HealthChecker()
    checker.run_all_checks()

if __name__ == "__main__":
    main()
