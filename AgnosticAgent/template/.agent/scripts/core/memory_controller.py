#!/usr/bin/env python3
"""
memory_controller.py
Hybrid memory system for agent context persistence and hallucination prevention.
Manages state, checkpoints, and validates claims against recorded history.
"""

import os
import sys
import json
import hashlib
from datetime import datetime, timezone

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
PROJECT_ROOT = os.path.dirname(AGENT_DIR)

STATE_DIR = os.path.join(AGENT_DIR, "state")
PROGRESS_FILE = os.path.join(STATE_DIR, "progress.json")
CHECKPOINTS_FILE = os.path.join(STATE_DIR, "checkpoints.json")
CONTEXT_FILE = os.path.join(STATE_DIR, "context.json")

# Ensure state directory exists
os.makedirs(STATE_DIR, exist_ok=True)

class MemoryController:
    def __init__(self):
        self.progress = self._load_json(PROGRESS_FILE, {"tasks": [], "completed": []})
        self.checkpoints = self._load_json(CHECKPOINTS_FILE, {"checkpoints": []})
        self.context = self._load_json(CONTEXT_FILE, {"current_task": None, "last_action": None})
    
    def _load_json(self, filepath, default):
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default
    
    def _save_json(self, filepath, data):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    # === CONTEXT MANAGEMENT ===
    
    def load_context(self):
        """Load current context for agent startup."""
        return {
            "current_task": self.context.get("current_task"),
            "completed_count": len(self.progress.get("completed", [])),
            "last_checkpoint": self._get_last_checkpoint(),
            "last_action": self.context.get("last_action")
        }
    
    def set_current_task(self, task_name):
        """Set the current task being worked on."""
        self.context["current_task"] = task_name
        self.context["task_started"] = datetime.now(timezone.utc).isoformat()
        self._save_json(CONTEXT_FILE, self.context)
    
    def clear_current_task(self):
        """Clear current task (on completion) and track duration."""
        if self.context.get("current_task"):
            # Calculate duration
            start_time = self.context.get("task_started")
            end_time = datetime.now(timezone.utc).isoformat()
            duration = None
            
            if start_time:
                try:
                    start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    end_dt = datetime.now(timezone.utc)
                    duration_seconds = (end_dt - start_dt).total_seconds()
                    duration = {
                        "seconds": int(duration_seconds),
                        "human": f"{int(duration_seconds // 60)}m {int(duration_seconds % 60)}s"
                    }
                except Exception:
                    pass
            
            self.progress["completed"].append({
                "task": self.context["current_task"],
                "started_at": start_time,
                "completed_at": end_time,
                "duration": duration
            })
            self._save_json(PROGRESS_FILE, self.progress)
        
        self.context["current_task"] = None
        self.context["task_started"] = None
        self._save_json(CONTEXT_FILE, self.context)
    
    # === CHECKPOINT MANAGEMENT ===
    
    def save_checkpoint(self, label, status="saved"):
        """Save a checkpoint with current state."""
        checkpoint = {
            "id": len(self.checkpoints["checkpoints"]) + 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "label": label,
            "status": status,
            "current_task": self.context.get("current_task"),
            "completed_count": len(self.progress.get("completed", []))
        }
        self.checkpoints["checkpoints"].append(checkpoint)
        self._save_json(CHECKPOINTS_FILE, self.checkpoints)
        return checkpoint
    
    def _get_last_checkpoint(self):
        """Get the most recent checkpoint."""
        if self.checkpoints["checkpoints"]:
            return self.checkpoints["checkpoints"][-1]
        return None
    
    def list_checkpoints(self, limit=5):
        """List recent checkpoints."""
        return self.checkpoints["checkpoints"][-limit:]
    
    # === SNAPSHOT MANAGEMENT ===
    
    def create_snapshot(self, phase_name):
        """Create a full snapshot at major phase (e.g., /start, /plan)."""
        snapshot_dir = os.path.join(STATE_DIR, "snapshots")
        os.makedirs(snapshot_dir, exist_ok=True)
        
        snapshot_id = len([f for f in os.listdir(snapshot_dir) if f.endswith('.json')]) + 1
        snapshot_file = os.path.join(snapshot_dir, f"snapshot_{snapshot_id:03d}.json")
        
        snapshot = {
            "id": snapshot_id,
            "phase": phase_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "progress": self.progress.copy(),
            "context": self.context.copy(),
            "checkpoints_count": len(self.checkpoints["checkpoints"])
        }
        
        self._save_json(snapshot_file, snapshot)
        print(f"📸 Snapshot #{snapshot_id} created: {phase_name}")
        return snapshot
    
    def list_snapshots(self):
        """List all snapshots."""
        snapshot_dir = os.path.join(STATE_DIR, "snapshots")
        if not os.path.exists(snapshot_dir):
            return []
        
        snapshots = []
        for f in sorted(os.listdir(snapshot_dir)):
            if f.endswith('.json'):
                data = self._load_json(os.path.join(snapshot_dir, f), {})
                snapshots.append(data)
        return snapshots
    
    def rollback_to_snapshot(self, snapshot_id):
        """Rollback to a specific snapshot."""
        snapshot_dir = os.path.join(STATE_DIR, "snapshots")
        snapshot_file = os.path.join(snapshot_dir, f"snapshot_{snapshot_id:03d}.json")
        
        if not os.path.exists(snapshot_file):
            return False, f"Snapshot #{snapshot_id} not found"
        
        snapshot = self._load_json(snapshot_file, {})
        
        # Restore state
        self.progress = snapshot.get("progress", {"tasks": [], "completed": []})
        self.context = snapshot.get("context", {"current_task": None})
        
        self._save_json(PROGRESS_FILE, self.progress)
        self._save_json(CONTEXT_FILE, self.context)
        
        print(f"⏪ Rolled back to snapshot #{snapshot_id}: {snapshot.get('phase')}")
        return True, f"Rolled back to {snapshot.get('phase')}"
    
    # === HALLUCINATION DETECTION ===
    
    def validate_file_exists(self, filepath):
        """Validate that a file actually exists (prevent hallucination)."""
        full_path = os.path.join(PROJECT_ROOT, filepath) if not os.path.isabs(filepath) else filepath
        exists = os.path.exists(full_path)
        return {"valid": exists, "path": filepath, "check": "file_exists"}
    
    def validate_task_completed(self, task_name):
        """Validate that a task was actually completed."""
        completed = [t["task"] for t in self.progress.get("completed", [])]
        is_completed = task_name in completed
        return {"valid": is_completed, "task": task_name, "check": "task_completed"}
    
    def validate_claim(self, claim_type, claim_value):
        """General claim validation for hallucination prevention."""
        if claim_type == "file_exists":
            return self.validate_file_exists(claim_value)
        elif claim_type == "task_completed":
            return self.validate_task_completed(claim_value)
        else:
            return {"valid": None, "error": f"Unknown claim type: {claim_type}"}
    
    # === PROGRESS TRACKING ===
    
    def add_task(self, task_name):
        """Add a task to the roadmap."""
        if task_name not in self.progress["tasks"]:
            self.progress["tasks"].append(task_name)
            self._save_json(PROGRESS_FILE, self.progress)
    
    def get_progress(self):
        """Get current progress summary."""
        total = len(self.progress["tasks"])
        completed = len(self.progress["completed"])
        return {
            "total_tasks": total,
            "completed_tasks": completed,
            "progress_percent": round(completed / total * 100, 1) if total > 0 else 0,
            "remaining": total - completed
        }
    
    # === SUMMARY FOR AGENT ===
    
    def get_memory_summary(self):
        """Get a summary for agent context injection."""
        context = self.load_context()
        progress = self.get_progress()
        
        return f"""## 🧠 Memory Context
- **Current Task:** {context.get('current_task') or 'None'}
- **Progress:** {progress['completed_tasks']}/{progress['total_tasks']} ({progress['progress_percent']}%)
- **Last Checkpoint:** {context.get('last_checkpoint', {}).get('label', 'None')}
- **Completed Tasks:** {progress['completed_tasks']}
"""

def main():
    mc = MemoryController()
    
    if len(sys.argv) < 2:
        print("Usage: memory_controller.py [context | checkpoint <label> | validate <type> <value> | progress | summary]")
        sys.exit(0)
    
    action = sys.argv[1]
    
    if action == "context":
        ctx = mc.load_context()
        print("📋 Current Context:")
        for k, v in ctx.items():
            print(f"   {k}: {v}")
    
    elif action == "checkpoint" and len(sys.argv) >= 3:
        label = ' '.join(sys.argv[2:])
        cp = mc.save_checkpoint(label)
        print(f"✅ Checkpoint saved: #{cp['id']} - {label}")
    
    elif action == "validate" and len(sys.argv) >= 4:
        claim_type = sys.argv[2]
        claim_value = sys.argv[3]
        result = mc.validate_claim(claim_type, claim_value)
        status = "✅ VALID" if result.get("valid") else "❌ INVALID"
        print(f"{status}: {claim_type} = {claim_value}")
    
    elif action == "progress":
        prog = mc.get_progress()
        print(f"📊 Progress: {prog['completed_tasks']}/{prog['total_tasks']} ({prog['progress_percent']}%)")
    
    elif action == "summary":
        print(mc.get_memory_summary())
    
    elif action == "set-task" and len(sys.argv) >= 3:
        task = ' '.join(sys.argv[2:])
        mc.set_current_task(task)
        print(f"✅ Current task set: {task}")
    
    elif action == "complete-task":
        mc.clear_current_task()
        print("✅ Task marked as complete")
    
    elif action == "snapshot" and len(sys.argv) >= 3:
        phase = ' '.join(sys.argv[2:])
        mc.create_snapshot(phase)
    
    elif action == "snapshots":
        snapshots = mc.list_snapshots()
        if not snapshots:
            print("📸 No snapshots found")
        else:
            print("📸 Snapshots:")
            for s in snapshots:
                print(f"   #{s['id']} - {s['phase']} ({s['timestamp'][:10]})")
    
    elif action == "rollback" and len(sys.argv) >= 3:
        try:
            snapshot_id = int(sys.argv[2])
            success, msg = mc.rollback_to_snapshot(snapshot_id)
            if not success:
                print(f"❌ {msg}")
        except ValueError:
            print("❌ Invalid snapshot ID")
    
    else:
        print("Unknown action")
        sys.exit(1)

if __name__ == "__main__":
    main()
