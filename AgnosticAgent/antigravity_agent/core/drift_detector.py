#!/usr/bin/env python3
"""
drift_detector.py
Detects when actions deviate from the planned roadmap.
Warns but does not block - human decides.

v2.0 Changes:
- Removed docs/roadmap.md reference (non-existent)
- task.md is now the primary source
- Improved fuzzy matching with entity+verb extraction
- Better word tokenization (strip markdown, emojis, bullets)
"""

import os
import sys
import json
import re
from datetime import datetime

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
PROJECT_ROOT = os.path.dirname(AGENT_DIR)

# Primary task sources (in priority order)
TASK_SOURCES = [
    os.path.join(PROJECT_ROOT, "task.md"),           # Project-level task file
    os.path.join(PROJECT_ROOT, "docs", "task.md"),    # Docs-level task file
]
STATE_FILE = os.path.join(AGENT_DIR, "state", "progress.json")

# Stopwords to ignore in matching
STOPWORDS = {
    "ve", "ile", "için", "bir", "bu", "de", "da", "mi", "mı", "mu", "mü",
    "the", "and", "for", "with", "this", "that", "from", "into", "on", "in",
    "a", "an", "of", "to", "is", "are", "was", "were", "be", "been",
}

# Action verbs for better matching
ACTION_VERBS = {
    "ekle", "oluştur", "yaz", "düzelt", "sil", "güncelle", "kur", "ayarla",
    "test", "deploy", "refactor", "optimize", "migrate", "fix", "add",
    "create", "update", "delete", "build", "setup", "configure", "implement",
}


class DriftDetector:
    def __init__(self):
        self.roadmap = self._load_roadmap()
        self.progress = self._load_progress()

    def _load_roadmap(self):
        """Load planned tasks from task files or progress.json fallback."""
        tasks = []

        # Try task sources in priority order
        for source in TASK_SOURCES:
            if os.path.exists(source):
                tasks.extend(self._parse_tasks(source))

        # Fallback: read planned tasks from progress.json
        if not tasks and os.path.exists(STATE_FILE):
            tasks.extend(self._load_tasks_from_progress())

        return tasks

    def _load_tasks_from_progress(self):
        """Extract task names from progress.json as fallback roadmap."""
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return [t.lower() if isinstance(t, str) else t.get("task", "").lower()
                    for t in data.get("tasks", [])]
        except Exception:
            return []

    def _parse_tasks(self, filepath):
        """Parse tasks from markdown checklist format."""
        tasks = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Match checklist items: - [ ] Task or - [x] Task or - [/] Task
            pattern = r'[-*]\s*\[[ x/]\]\s*(.+)'
            matches = re.findall(pattern, content, re.IGNORECASE)

            for match in matches:
                # Clean up the task name
                task = match.strip()
                # Remove markdown formatting
                task = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', task)  # links
                task = re.sub(r'[🔴🟠🟡🟢🏗️📦🎨🚀✅⚠️❌💡🔒🛡️📋🔍]', '', task)  # emojis
                task = re.sub(r'\*\*([^*]+)\*\*', r'\1', task)  # bold
                task = task.strip()
                if task:
                    tasks.append(task.lower())
        except Exception:
            pass

        return tasks

    def _load_progress(self):
        """Load current progress state."""
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"tasks": [], "completed": []}

    def _extract_meaningful_words(self, text):
        """Extract meaningful words, stripping stopwords and short tokens."""
        words = re.findall(r'[a-zA-ZçğıöşüÇĞİÖŞÜ_]+', text.lower())
        return {w for w in words if w not in STOPWORDS and len(w) > 2}

    def _extract_verb_entity(self, text):
        """Extract action verb and target entity from text."""
        words = re.findall(r'[a-zA-ZçğıöşüÇĞİÖŞÜ_]+', text.lower())
        verbs = [w for w in words if w in ACTION_VERBS]
        entities = [w for w in words if w not in ACTION_VERBS and w not in STOPWORDS and len(w) > 2]
        return set(verbs), set(entities)

    def check_action(self, action_description):
        """
        Check if an action aligns with the roadmap.
        Uses entity+verb matching for accuracy.
        Returns: (is_aligned, message)
        """
        action_lower = action_description.lower()

        # If no roadmap exists, can't check
        if not self.roadmap:
            return True, "No task list found - unable to check alignment"

        action_words = self._extract_meaningful_words(action_lower)
        action_verbs, action_entities = self._extract_verb_entity(action_lower)

        best_score = 0
        best_match = None

        for task in self.roadmap:
            task_words = self._extract_meaningful_words(task)
            task_verbs, task_entities = self._extract_verb_entity(task)

            # Score: Entity overlap weighs more than generic word overlap
            entity_overlap = len(action_entities & task_entities)
            verb_overlap = len(action_verbs & task_verbs)
            word_overlap = len(action_words & task_words)

            # Weighted score: entity match is most important
            score = (entity_overlap * 3) + (verb_overlap * 2) + word_overlap

            if score > best_score:
                best_score = score
                best_match = task

        # Threshold: at least one entity match + any other match, or 4+ word overlap
        if best_score >= 4:
            return True, f"Aligned with: {best_match[:60]}..."

        # No match found
        return False, "⚠️ This action is NOT in the planned task list"

    def get_roadmap_summary(self):
        """Get summary of roadmap status."""
        if not self.roadmap:
            return "No task list found"

        return f"Task list has {len(self.roadmap)} planned items"

    def check_and_report(self, action):
        """Check action and print report."""
        is_aligned, message = self.check_action(action)

        if is_aligned:
            print(f"✅ ALIGNED: {message}")
        else:
            print(f"⚠️ DRIFT DETECTED")
            print(f"   Action: {action[:60]}...")
            print(f"   {message}")
            print(f"\n   Planned tasks ({len(self.roadmap)}):")
            for task in self.roadmap[:5]:
                print(f"   - {task[:50]}...")
            if len(self.roadmap) > 5:
                print(f"   ... and {len(self.roadmap) - 5} more")

        return is_aligned


def main():
    detector = DriftDetector()

    if len(sys.argv) < 2:
        print("Usage: drift_detector.py [check <action> | status | roadmap]")
        print(f"\n{detector.get_roadmap_summary()}")
        sys.exit(0)

    action = sys.argv[1]

    if action == "check" and len(sys.argv) >= 3:
        action_desc = ' '.join(sys.argv[2:])
        is_aligned = detector.check_and_report(action_desc)
        sys.exit(0 if is_aligned else 1)

    elif action == "status":
        print(f"📋 {detector.get_roadmap_summary()}")
        print(f"📊 Progress: {len(detector.progress.get('completed', []))} completed")

    elif action == "roadmap":
        print("📋 Planned Tasks:")
        for i, task in enumerate(detector.roadmap, 1):
            print(f"   {i}. {task}")

    else:
        print("Unknown action")
        sys.exit(1)


if __name__ == "__main__":
    main()
