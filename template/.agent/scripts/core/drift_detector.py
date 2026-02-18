#!/usr/bin/env python3
"""
drift_detector.py
Detects when actions deviate from the planned roadmap.
Warns but does not block - human decides.
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

ROADMAP_FILE = os.path.join(PROJECT_ROOT, "docs", "roadmap.md")
TASK_FILE = os.path.join(PROJECT_ROOT, "docs", "task.md")
STATE_FILE = os.path.join(AGENT_DIR, "state", "progress.json")

# Fallback sources when roadmap/task files don't exist
FALLBACK_SOURCES = [
    os.path.join(AGENT_DIR, "state", "progress.json"),
]

class DriftDetector:
    def __init__(self):
        self.roadmap = self._load_roadmap()
        self.progress = self._load_progress()
    
    def _load_roadmap(self):
        """Load planned tasks from roadmap, task file, or progress.json fallback."""
        tasks = []
        
        # Try roadmap.md first
        if os.path.exists(ROADMAP_FILE):
            tasks.extend(self._parse_tasks(ROADMAP_FILE))
        
        # Also check task.md
        if os.path.exists(TASK_FILE):
            tasks.extend(self._parse_tasks(TASK_FILE))
        
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
                # Remove markdown links
                task = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', task)
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
    
    def check_action(self, action_description):
        """
        Check if an action aligns with the roadmap.
        Returns: (is_aligned, message)
        """
        action_lower = action_description.lower()
        
        # If no roadmap exists, can't check
        if not self.roadmap:
            return True, "No roadmap found - unable to check alignment"
        
        # Check if action matches any planned task
        for task in self.roadmap:
            # Fuzzy match: check if key words overlap
            task_words = set(task.split())
            action_words = set(action_lower.split())
            
            # If significant overlap, consider aligned
            overlap = task_words.intersection(action_words)
            if len(overlap) >= 2 or any(word in action_lower for word in task.split()[:3]):
                return True, f"Aligned with: {task[:50]}..."
        
        # No match found
        return False, "⚠️ This action is NOT in the planned roadmap"
    
    def get_roadmap_summary(self):
        """Get summary of roadmap status."""
        if not self.roadmap:
            return "No roadmap found"
        
        return f"Roadmap has {len(self.roadmap)} planned tasks"
    
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
