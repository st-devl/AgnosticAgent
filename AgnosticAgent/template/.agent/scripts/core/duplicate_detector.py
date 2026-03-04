#!/usr/bin/env python3
"""
duplicate_detector.py
Detects duplicate/similar code to enforce "System Load & Reusability" principle.
Finds: copy-paste code, similar functions, repeated patterns.
"""

import os
import sys
import re
import hashlib
from collections import defaultdict

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
PROJECT_ROOT = os.path.dirname(AGENT_DIR)

# Settings
MIN_DUPLICATE_LINES = 5
CODE_EXTENSIONS = ['.py', '.js', '.ts', '.php', '.java', '.go', '.rb', '.vue', '.jsx', '.tsx']

class DuplicateDetector:
    def __init__(self):
        self.code_blocks = defaultdict(list)  # hash -> [(file, line_start)]
        self.duplicates = []
        self.files_checked = 0
    
    def normalize_line(self, line):
        """Normalize a line for comparison (remove whitespace, comments)."""
        # Remove leading/trailing whitespace
        line = line.strip()
        # Skip empty lines and simple brackets
        if not line or line in ['{', '}', '(', ')', '[', ']', '']:
            return None
        # Remove single-line comments
        line = re.sub(r'//.*$', '', line)
        line = re.sub(r'#.*$', '', line)
        return line.strip() if line.strip() else None
    
    def extract_blocks(self, filepath, lines):
        """Extract code blocks for comparison."""
        rel_path = os.path.relpath(filepath, PROJECT_ROOT)
        
        for i in range(len(lines) - MIN_DUPLICATE_LINES + 1):
            # Get a block of lines
            block = []
            for j in range(MIN_DUPLICATE_LINES):
                normalized = self.normalize_line(lines[i + j])
                if normalized:
                    block.append(normalized)
            
            if len(block) >= MIN_DUPLICATE_LINES:
                # Hash the block
                block_text = '\n'.join(block)
                block_hash = hashlib.md5(block_text.encode()).hexdigest()
                self.code_blocks[block_hash].append({
                    "file": rel_path,
                    "line": i + 1,
                    "preview": block[0][:50]
                })
    
    def check_file(self, filepath):
        """Check a single file for duplicate code."""
        ext = os.path.splitext(filepath)[1]
        if ext not in CODE_EXTENSIONS:
            return
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception:
            return
        
        self.files_checked += 1
        self.extract_blocks(filepath, lines)
    
    def scan_directory(self, directory):
        """Scan directory for duplicates."""
        ignore_dirs = {'node_modules', 'vendor', '.git', '__pycache__', 'dist', 'build'}
        
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for file in files:
                filepath = os.path.join(root, file)
                self.check_file(filepath)
        
        # Find duplicates (blocks that appear more than once)
        for block_hash, locations in self.code_blocks.items():
            if len(locations) > 1:
                # Check if from different files or distant in same file
                unique_files = set(loc["file"] for loc in locations)
                if len(unique_files) > 1:
                    self.duplicates.append(locations)
    
    def report(self):
        """Generate duplicate report."""
        print("🔍 Duplicate Code Detection Report")
        print("=" * 50)
        print(f"📁 Dosya sayısı: {self.files_checked}")
        print(f"🔁 Duplicate grup sayısı: {len(self.duplicates)}")
        print()
        
        if not self.duplicates:
            print("✅ Duplicate kod bulunamadı!")
            return 0
        
        for i, locations in enumerate(self.duplicates[:10], 1):  # Show first 10
            print(f"🔁 Duplicate #{i}")
            print(f"   Önizleme: {locations[0]['preview']}...")
            for loc in locations:
                print(f"   📍 {loc['file']}:{loc['line']}")
            print()
        
        if len(self.duplicates) > 10:
            print(f"   ... ve {len(self.duplicates) - 10} duplicate daha")
        
        return len(self.duplicates)

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else PROJECT_ROOT
    
    detector = DuplicateDetector()
    detector.scan_directory(target)
    duplicates = detector.report()
    
    sys.exit(1 if duplicates > 0 else 0)

if __name__ == "__main__":
    main()
