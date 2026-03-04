#!/usr/bin/env python3
"""
ssot_validator.py
Validates Single Source of Truth (SSOT) consistency across docs.
Detects conflicts between tech_stack, architecture, and prd.

v2.0 Changes:
- Improved technology conflict detection: distinguishes primary DB vs cache vs queue
- Eliminated false positives when multiple DB types serve different purposes
- Better reporting with conflict context
"""

import os
import sys
import re
from datetime import datetime

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
PROJECT_ROOT = os.path.dirname(AGENT_DIR)
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")

# SSOT Files in priority order
SSOT_FILES = [
    ("tech_stack.md", 1),      # Highest priority
    ("architecture.md", 2),
    ("prd.md", 3),
    ("design_brief.md", 4),
]

# Known technology keywords to track — categorized by PURPOSE
TECH_KEYWORDS = {
    "languages": ["php", "python", "javascript", "typescript", "go", "rust", "java"],
    "frameworks": ["laravel", "django", "react", "vue", "angular", "next.js", "express", "filament"],
    "primary_databases": ["mysql", "postgresql", "mongodb", "sqlite", "mariadb"],
    "cache_stores": ["redis", "memcached", "varnish"],
    "queue_systems": ["rabbitmq", "kafka", "beanstalkd"],
    "search_engines": ["elasticsearch", "meilisearch", "algolia"],
    "tools": ["docker", "kubernetes", "nginx", "apache", "git", "npm", "composer"],
}

# Context keywords that clarify DB purpose
DB_PURPOSE_KEYWORDS = {
    "cache": ["cache", "caching", "session", "temporary", "ttl"],
    "queue": ["queue", "job", "worker", "message", "broker"],
    "search": ["search", "index", "full-text", "fulltext"],
    "primary": ["primary", "database", "storage", "persistent", "main db", "ana veritabanı"],
}


class SSOTValidator:
    def __init__(self):
        self.files = {}
        self.conflicts = []
        self.warnings = []

    def load_files(self):
        """Load all SSOT files."""
        for filename, priority in SSOT_FILES:
            filepath = os.path.join(DOCS_DIR, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.files[filename] = {
                        "content": f.read().lower(),
                        "priority": priority,
                        "exists": True
                    }
            else:
                self.files[filename] = {
                    "content": "",
                    "priority": priority,
                    "exists": False
                }

    def extract_technologies(self, content):
        """Extract mentioned technologies from content."""
        found = {}
        for category, keywords in TECH_KEYWORDS.items():
            found[category] = []
            for keyword in keywords:
                if keyword in content:
                    found[category].append(keyword)
        return found

    def _determine_db_purpose(self, content, db_name):
        """Determine what purpose a database serves based on surrounding context."""
        purposes = []
        # Check ~100 chars around each mention
        for match in re.finditer(re.escape(db_name), content):
            start = max(0, match.start() - 100)
            end = min(len(content), match.end() + 100)
            context = content[start:end]

            for purpose, keywords in DB_PURPOSE_KEYWORDS.items():
                if any(kw in context for kw in keywords):
                    purposes.append(purpose)

        if not purposes:
            purposes.append("primary")

        return list(set(purposes))

    def check_consistency(self):
        """Check for consistency across SSOT files."""
        self.load_files()

        # 1. Check file existence
        for filename, data in self.files.items():
            if not data["exists"]:
                if data["priority"] == 1:
                    self.conflicts.append({
                        "type": "missing_primary",
                        "file": filename,
                        "severity": "critical",
                        "message": f"Primary SSOT file missing: {filename}"
                    })
                else:
                    self.warnings.append({
                        "type": "missing_file",
                        "file": filename,
                        "message": f"SSOT file not found: {filename}"
                    })

        # 2. Extract technologies from each file
        tech_mentions = {}
        for filename, data in self.files.items():
            if data["exists"]:
                tech_mentions[filename] = self.extract_technologies(data["content"])

        # 3. Check for PRIMARY DATABASE conflicts only
        # Different DBs used for different purposes (mysql=primary, redis=cache) is NOT a conflict
        if "tech_stack.md" in tech_mentions and "architecture.md" in tech_mentions:
            ts_content = self.files["tech_stack.md"]["content"]
            arch_content = self.files["architecture.md"]["content"]

            ts_primary_dbs = set(tech_mentions["tech_stack.md"]["primary_databases"])
            arch_primary_dbs = set(tech_mentions["architecture.md"]["primary_databases"])

            if ts_primary_dbs and arch_primary_dbs:
                # Only flag if SAME-PURPOSE databases conflict
                ts_purposes = {}
                for db in ts_primary_dbs:
                    ts_purposes[db] = self._determine_db_purpose(ts_content, db)

                arch_purposes = {}
                for db in arch_primary_dbs:
                    arch_purposes[db] = self._determine_db_purpose(arch_content, db)

                # Find DBs used as "primary" in one file but different in another
                ts_primary_set = {db for db, purposes in ts_purposes.items() if "primary" in purposes}
                arch_primary_set = {db for db, purposes in arch_purposes.items() if "primary" in purposes}

                if ts_primary_set and arch_primary_set and ts_primary_set != arch_primary_set:
                    self.conflicts.append({
                        "type": "database_conflict",
                        "file1": "tech_stack.md",
                        "file2": "architecture.md",
                        "severity": "high",
                        "values": {
                            "tech_stack_primary": list(ts_primary_set),
                            "architecture_primary": list(arch_primary_set)
                        },
                        "message": f"Primary DB conflict: tech_stack says {ts_primary_set}, architecture says {arch_primary_set}"
                    })

        # 4. Check for framework conflicts
        if "tech_stack.md" in tech_mentions:
            ts_fw = set(tech_mentions["tech_stack.md"]["frameworks"])
            for filename, techs in tech_mentions.items():
                if filename != "tech_stack.md":
                    other_fw = set(techs["frameworks"])
                    if other_fw and ts_fw and not ts_fw.intersection(other_fw):
                        self.warnings.append({
                            "type": "framework_mismatch",
                            "file1": "tech_stack.md",
                            "file2": filename,
                            "message": f"Framework mismatch: {ts_fw} vs {other_fw}"
                        })

        return {
            "conflicts": self.conflicts,
            "warnings": self.warnings,
            "files_checked": len([f for f in self.files.values() if f["exists"]]),
            "technologies": tech_mentions
        }

    def get_score(self):
        """Calculate consistency score."""
        result = self.check_consistency()

        base_score = 100
        base_score -= len(result["conflicts"]) * 20
        base_score -= len(result["warnings"]) * 5

        return max(0, min(100, base_score))

    def print_report(self):
        """Print validation report."""
        result = self.check_consistency()
        score = self.get_score()

        print("📊 SSOT Consistency Report")
        print("=" * 50)
        print(f"Score: {score}/100")
        print(f"Files checked: {result['files_checked']}/{len(SSOT_FILES)}")

        if result["conflicts"]:
            print(f"\n❌ Conflicts ({len(result['conflicts'])}):")
            for c in result["conflicts"]:
                print(f"   [{c['severity'].upper()}] {c['message']}")

        if result["warnings"]:
            print(f"\n⚠️ Warnings ({len(result['warnings'])}):")
            for w in result["warnings"]:
                print(f"   {w['message']}")

        if not result["conflicts"] and not result["warnings"]:
            print("\n✅ No conflicts or warnings found!")

        # Show detected technologies
        print("\n📋 Detected Technologies:")
        for filename, techs in result.get("technologies", {}).items():
            active = [t for cat, items in techs.items() for t in items]
            if active:
                print(f"   {filename}: {', '.join(active)}")

        return result


def main():
    validator = SSOTValidator()

    if len(sys.argv) < 2 or sys.argv[1] == "validate":
        validator.print_report()

    elif sys.argv[1] == "score":
        score = validator.get_score()
        print(f"SSOT Score: {score}/100")
        sys.exit(0 if score >= 80 else 1)

    elif sys.argv[1] == "json":
        import json
        result = validator.check_consistency()
        result["score"] = validator.get_score()
        print(json.dumps(result, indent=2))

    else:
        print("Usage: ssot_validator.py [validate | score | json]")
        sys.exit(1)


if __name__ == "__main__":
    main()
