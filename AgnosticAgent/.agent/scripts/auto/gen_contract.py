#!/usr/bin/env python3
"""
gen_contract.py
Otomatik kontrat oluşturucu.
Kullanım: python3 gen_contract.py --operation user_create --fields name:string,email:string
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
CONTRACTS_DIR = os.path.join(os.path.dirname(AGENT_DIR), "contracts")

def create_contract(operation, domain, entity, version, fields):
    contract = {
        "operation": operation,
        "version": version,
        "description": f"Operation {operation} for {entity}",
        "input": {
            "fields": []
        },
        "output": {
            "success": {
                "type": "object",
                "schema": {}
            },
            "errors": {
                "validation": "Bkz: .agent/rules/error-handling.md",
                "auth": "Bkz: .agent/rules/error-handling.md"
            }
        },
        "metadata": {
            "auth_required": True,
            "idempotent": False,
            "created_at": datetime.now().isoformat()
        }
    }

    for field in fields:
        parts = field.split(':')
        name = parts[0]
        dtype = parts[1] if len(parts) > 1 else "string"
        
        contract["input"]["fields"].append({
            "name": name,
            "type": dtype,
            "required": True,
            "validation": {
                "rules": [],
                "error_message": f"Invalid {name}"
            }
        })

    # Dosya yolu oluştur
    path = os.path.join(CONTRACTS_DIR, domain, entity, f"v{version}")
    os.makedirs(path, exist_ok=True)
    
    file_path = os.path.join(path, "contract.json")
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(contract, f, indent=2, ensure_ascii=False)
    
    # Auto-update registry.json
    _update_registry(operation, domain, entity, version, file_path)
    
    print(f"✅ Contract created: {file_path}")
    return file_path

def _update_registry(operation, domain, entity, version, contract_path):
    """Update contracts/registry.json with the new contract entry."""
    registry_path = os.path.join(CONTRACTS_DIR, "registry.json")
    
    if not os.path.exists(registry_path):
        registry = {"version": "1.0.0", "contracts": [], "domains": {}}
    else:
        with open(registry_path, "r", encoding="utf-8") as f:
            registry = json.load(f)
    
    # Check if contract already exists
    rel_path = os.path.relpath(contract_path, os.path.dirname(CONTRACTS_DIR))
    existing = [c for c in registry.get("contracts", []) if c.get("operation") == operation]
    
    if existing:
        # Update version
        existing[0]["version"] = version
        existing[0]["path"] = rel_path
        existing[0]["status"] = "active"
    else:
        # Add new entry
        registry.setdefault("contracts", []).append({
            "operation": operation,
            "domain": domain,
            "entity": entity,
            "version": version,
            "path": rel_path,
            "status": "active"
        })
    
    # Update domain tracking
    registry.setdefault("domains", {}).setdefault(domain, {}).setdefault("entities", [])
    if entity not in registry["domains"][domain]["entities"]:
        registry["domains"][domain]["entities"].append(entity)
    
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    
    print(f"📋 Registry updated: {registry_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate API Contract")
    parser.add_argument("--operation", required=True, help="Operation name (e.g. create_user)")
    parser.add_argument("--domain", default="common", help="Domain name")
    parser.add_argument("--entity", default="general", help="Entity name")
    parser.add_argument("--version", default="1.0.0", help="Semver version")
    parser.add_argument("--fields", help="Comma separated fields (name:type)")
    
    args = parser.parse_args()
    
    field_list = args.fields.split(',') if args.fields else []
    create_contract(args.operation, args.domain, args.entity, args.version, field_list)

if __name__ == "__main__":
    main()
