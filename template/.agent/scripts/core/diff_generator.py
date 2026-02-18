#!/usr/bin/env python3
"""
diff_generator.py
Generates unified diffs for file changes before applying them.
Enables dry-run mode, preview, and safe rollback.
"""

import os
import sys
import difflib
import hashlib
import shutil
from datetime import datetime

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
PROJECT_ROOT = os.path.dirname(AGENT_DIR)
BACKUP_DIR = os.path.join(AGENT_DIR, "backups")

class DiffGenerator:
    def __init__(self):
        os.makedirs(BACKUP_DIR, exist_ok=True)
    
    def generate_diff(self, original, modified, filename="file"):
        """Generate unified diff between two strings."""
        original_lines = original.splitlines(keepends=True)
        modified_lines = modified.splitlines(keepends=True)
        
        diff = list(difflib.unified_diff(
            original_lines,
            modified_lines,
            fromfile=f"a/{filename}",
            tofile=f"b/{filename}",
            lineterm=""
        ))
        
        return "".join(diff)
    
    def generate_diff_from_files(self, original_path, modified_content):
        """Generate diff from existing file and new content."""
        if os.path.exists(original_path):
            with open(original_path, 'r', encoding='utf-8') as f:
                original = f.read()
        else:
            original = ""
        
        filename = os.path.basename(original_path)
        return self.generate_diff(original, modified_content, filename)
    
    def preview_change(self, filepath, new_content):
        """Preview a change without applying it."""
        diff = self.generate_diff_from_files(filepath, new_content)
        
        # Count changes
        additions = sum(1 for line in diff.split('\n') if line.startswith('+') and not line.startswith('+++'))
        deletions = sum(1 for line in diff.split('\n') if line.startswith('-') and not line.startswith('---'))
        
        return {
            "filepath": filepath,
            "diff": diff,
            "additions": additions,
            "deletions": deletions,
            "net_change": additions - deletions
        }
    
    def backup_file(self, filepath):
        """Create a backup of a file before modifying."""
        if not os.path.exists(filepath):
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(filepath)
        backup_name = f"{filename}.{timestamp}.bak"
        backup_path = os.path.join(BACKUP_DIR, backup_name)
        
        shutil.copy2(filepath, backup_path)
        return backup_path
    
    def get_file_hash(self, filepath):
        """Get SHA256 hash of a file."""
        if not os.path.exists(filepath):
            return None
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()[:12]
    
    def safe_write(self, filepath, new_content, dry_run=False):
        """
        Safely write content to a file with backup and verification.
        
        Args:
            filepath: Target file path
            new_content: New content to write
            dry_run: If True, only preview without writing
        
        Returns:
            dict with status, diff, and metadata
        """
        preview = self.preview_change(filepath, new_content)
        
        if dry_run:
            return {
                "status": "dry_run",
                "would_change": True,
                **preview
            }
        
        # Create backup
        original_hash = self.get_file_hash(filepath)
        backup_path = self.backup_file(filepath)
        
        try:
            # Write new content
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # Verify write
            new_hash = self.get_file_hash(filepath)
            
            return {
                "status": "success",
                "backup": backup_path,
                "original_hash": original_hash,
                "new_hash": new_hash,
                **preview
            }
        
        except Exception as e:
            # Rollback on error
            if backup_path and os.path.exists(backup_path):
                shutil.copy2(backup_path, filepath)
            
            return {
                "status": "failed",
                "error": str(e),
                "rolled_back": True,
                **preview
            }
    
    def rollback(self, filepath, backup_path):
        """Rollback a file to its backup."""
        if not os.path.exists(backup_path):
            return False, "Backup not found"
        
        shutil.copy2(backup_path, filepath)
        return True, f"Rolled back to {backup_path}"
    
    def list_backups(self, filename=None):
        """List available backups."""
        if not os.path.exists(BACKUP_DIR):
            return []
        
        backups = []
        for f in os.listdir(BACKUP_DIR):
            if f.endswith('.bak'):
                if filename is None or f.startswith(filename):
                    backups.append(f)
        
        return sorted(backups, reverse=True)

def main():
    differ = DiffGenerator()
    
    if len(sys.argv) < 2:
        print("Usage: diff_generator.py [preview <file> | backup <file> | list | rollback <file> <backup>]")
        sys.exit(0)
    
    action = sys.argv[1]
    
    if action == "preview" and len(sys.argv) >= 3:
        filepath = sys.argv[2]
        # Read new content from stdin
        print(f"📝 Enter new content for {filepath} (Ctrl+D to end):")
        try:
            new_content = sys.stdin.read()
            result = differ.preview_change(filepath, new_content)
            print(f"\n📊 Preview:")
            print(f"   Additions: +{result['additions']}")
            print(f"   Deletions: -{result['deletions']}")
            print(f"\n{result['diff']}")
        except KeyboardInterrupt:
            print("\nCancelled")
    
    elif action == "backup" and len(sys.argv) >= 3:
        filepath = sys.argv[2]
        backup_path = differ.backup_file(filepath)
        if backup_path:
            print(f"✅ Backup created: {backup_path}")
        else:
            print(f"❌ File not found: {filepath}")
    
    elif action == "list":
        backups = differ.list_backups()
        print(f"📋 Available backups ({len(backups)}):")
        for b in backups[:10]:
            print(f"   - {b}")
    
    elif action == "rollback" and len(sys.argv) >= 4:
        filepath = sys.argv[2]
        backup = sys.argv[3]
        backup_path = os.path.join(BACKUP_DIR, backup)
        success, msg = differ.rollback(filepath, backup_path)
        print(f"{'✅' if success else '❌'} {msg}")
    
    else:
        print("Unknown action")
        sys.exit(1)

if __name__ == "__main__":
    main()
