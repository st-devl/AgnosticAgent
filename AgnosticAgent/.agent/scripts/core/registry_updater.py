#!/usr/bin/env python3
"""
registry_updater.py
Automatically updates docs/registry.md when new components are created.
Watches for new files and categorizes them appropriately.
"""

import os
import sys
import re
from datetime import datetime

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
PROJECT_ROOT = os.path.dirname(AGENT_DIR)
REGISTRY_FILE = os.path.join(PROJECT_ROOT, "docs", "registry.md")

# Component detection patterns
COMPONENT_PATTERNS = {
    "models": [
        r"app/Models/.*\.php$",
        r"src/models/.*\.(ts|js)$",
    ],
    "controllers": [
        r"app/Http/Controllers/.*\.php$",
        r"src/controllers/.*\.(ts|js)$",
    ],
    "services": [
        r"app/Services/.*\.php$",
        r"src/services/.*\.(ts|js)$",
    ],
    "components": [
        r"resources/views/components/.*\.blade\.php$",
        r"resources/views/livewire/.*\.blade\.php$",
        r"src/components/.*\.(tsx|jsx|vue)$",
    ],
    "migrations": [
        r"database/migrations/.*\.php$",
    ],
    "api_endpoints": [
        r"routes/api\.php$",
        r"routes/web\.php$",
    ],
    "scripts": [
        r"\.agent/scripts/.*\.py$",
    ]
}

class RegistryUpdater:
    def __init__(self):
        self.registry = self._load_registry()
    
    def _load_registry(self):
        """Load current registry content."""
        if not os.path.exists(REGISTRY_FILE):
            return self._create_empty_registry()
        
        with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _create_empty_registry(self):
        """Create empty registry structure."""
        return """# Component Registry

> Bu dosya projedeki tüm önemli bileşenleri takip eder.
> Otomatik olarak güncellenir.

---

## Backend Modules

| Modül | Dosya | Açıklama |
|-------|-------|----------|

## Frontend Components

| Component | Dosya | Açıklama |
|-----------|-------|----------|

## API Endpoints

| Endpoint | Method | Controller |
|----------|--------|------------|

## Agent Scripts

| Script | Amaç |
|--------|------|

---

> Son güncelleme: -
"""
    
    def categorize_file(self, filepath):
        """Categorize a file based on its path."""
        rel_path = os.path.relpath(filepath, PROJECT_ROOT)
        
        for category, patterns in COMPONENT_PATTERNS.items():
            for pattern in patterns:
                if re.match(pattern, rel_path):
                    return category
        
        return None
    
    def extract_name(self, filepath):
        """Extract component name from filepath."""
        basename = os.path.basename(filepath)
        name = os.path.splitext(basename)[0]
        # Remove common suffixes
        for suffix in ['Controller', 'Service', 'Model', 'Component']:
            if name.endswith(suffix):
                name = name[:-len(suffix)]
        return name
    
    def is_registered(self, filepath):
        """Check if a file is already in the registry."""
        rel_path = os.path.relpath(filepath, PROJECT_ROOT)
        return rel_path in self.registry or os.path.basename(filepath) in self.registry
    
    def add_to_registry(self, filepath, description=""):
        """Add a file to the registry."""
        category = self.categorize_file(filepath)
        if not category:
            return False, "File does not match any component pattern"
        
        if self.is_registered(filepath):
            return False, "Already registered"
        
        rel_path = os.path.relpath(filepath, PROJECT_ROOT)
        name = self.extract_name(filepath)
        
        # Find the right section and add entry
        section_markers = {
            "models": "## Backend Modules",
            "controllers": "## Backend Modules",
            "services": "## Backend Modules",
            "components": "## Frontend Components",
            "migrations": "## Backend Modules",
            "api_endpoints": "## API Endpoints",
            "scripts": "## Agent Scripts"
        }
        
        marker = section_markers.get(category, "## Backend Modules")
        
        # Create new entry
        if category == "scripts":
            new_entry = f"| `{os.path.basename(filepath)}` | {description or 'TBD'} |"
        else:
            new_entry = f"| {name} | `{rel_path}` | {description or 'TBD'} |"
        
        # Insert after the table header
        lines = self.registry.split('\n')
        inserted = False
        for i, line in enumerate(lines):
            if marker in line:
                # Find the table end (empty line after table)
                for j in range(i + 4, len(lines)):  # Skip header + separator
                    if lines[j].strip() == '' or not lines[j].startswith('|'):
                        lines.insert(j, new_entry)
                        inserted = True
                        break
                break
        
        if inserted:
            self.registry = '\n'.join(lines)
            self._update_timestamp()
            self._save_registry()
            return True, f"Added to {category}"
        
        return False, "Could not find section"
    
    def _update_timestamp(self):
        """Update the last modified timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.registry = re.sub(
            r'Son güncelleme: .*',
            f'Son güncelleme: {timestamp}',
            self.registry
        )
    
    def _save_registry(self):
        """Save registry to file."""
        with open(REGISTRY_FILE, 'w', encoding='utf-8') as f:
            f.write(self.registry)
    
    def scan_and_update(self):
        """Scan project and update registry with new components."""
        added = []
        
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'vendor', '__pycache__'}]
            
            for filename in files:
                filepath = os.path.join(root, filename)
                category = self.categorize_file(filepath)
                
                if category and not self.is_registered(filepath):
                    success, reason = self.add_to_registry(filepath)
                    if success:
                        added.append(filepath)
        
        return added

def main():
    updater = RegistryUpdater()
    
    if len(sys.argv) < 2:
        print("Usage: registry_updater.py [scan | add <filepath> | check <filepath>]")
        sys.exit(0)
    
    action = sys.argv[1]
    
    if action == "scan":
        print("🔍 Scanning for new components...")
        added = updater.scan_and_update()
        if added:
            print(f"✅ Added {len(added)} new components:")
            for f in added:
                print(f"   + {os.path.relpath(f, PROJECT_ROOT)}")
        else:
            print("✅ Registry is up to date")
    
    elif action == "add" and len(sys.argv) >= 3:
        filepath = sys.argv[2]
        description = ' '.join(sys.argv[3:]) if len(sys.argv) > 3 else ""
        success, reason = updater.add_to_registry(filepath, description)
        if success:
            print(f"✅ Added: {filepath}")
        else:
            print(f"⚠️ Not added: {reason}")
    
    elif action == "check" and len(sys.argv) >= 3:
        filepath = sys.argv[2]
        category = updater.categorize_file(filepath)
        registered = updater.is_registered(filepath)
        print(f"📋 File: {filepath}")
        print(f"   Category: {category or 'None'}")
        print(f"   Registered: {'Yes' if registered else 'No'}")
    
    else:
        print("Unknown action")
        sys.exit(1)

if __name__ == "__main__":
    main()
