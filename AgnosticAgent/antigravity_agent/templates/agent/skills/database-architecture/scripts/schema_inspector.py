#!/usr/bin/env python3
"""
schema_inspector.py

Analyze Laravel migration files to build a schema summary.
This allows the Agent to understand the database structure without reading 50+ files manually.
"""

import os
import re
import json
import glob

# Configuration
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
MIGRATIONS_DIR = os.path.join(PROJECT_ROOT, "database", "migrations")

def scan_migrations():
    """Scans migration files and extracts table definitions."""
    if not os.path.exists(MIGRATIONS_DIR):
        print(json.dumps({"error": f"Migrations directory not found at {MIGRATIONS_DIR}"}))
        return

    tables = {}
    
    # Sort files to ensure create order
    files = sorted(glob.glob(os.path.join(MIGRATIONS_DIR, "*.php")))
    
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Find table creation
            # Schema::create('users', function (Blueprint $table) {
            create_matches = re.findall(r"Schema::create\(['\"]([a-zA-Z0-9_]+)['\"]", content)
            
            for table_name in create_matches:
                if table_name not in tables:
                    tables[table_name] = {"columns": [], "indexes": []}
                
                # Extract columns (Basic regex, can be improved)
                # $table->string('name');
                column_matches = re.findall(r"\$table->([a-z]+)\(['\"]([a-zA-Z0-9_]+)['\"]", content)
                for type_, name in column_matches:
                    tables[table_name]["columns"].append({"name": name, "type": type_})

    # Return Result
    result = {
        "status": "success",
        "migration_count": len(files),
        "tables": tables
    }
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    scan_migrations()
