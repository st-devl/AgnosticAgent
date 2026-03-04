#!/usr/bin/env python3
"""
contract_validator.py
Enforces "Contract-First Development" principle globally.
Validates all backend-frontend contracts in `contracts/` directory against required schemas,
and optionally synchronizes `contracts/registry.json`.

v1.0 (Phase 3 addition):
- Ensures operation formats, required fields, and metadata rules are strictly followed.
- Agnostic architecture: Does not depend on PHP/JS; only standard JSON API schemas.
"""

import os
import sys
import json
import glob
import re
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
PROJECT_ROOT = os.path.dirname(AGENT_DIR)
CONTRACTS_DIR = os.path.join(PROJECT_ROOT, "contracts")
REGISTRY_FILE = os.path.join(CONTRACTS_DIR, "registry.json")

REQUIRED_FIELDS = ["operation", "version", "description", "input", "output", "metadata"]
METADATA_REQUIRED_FIELDS = ["auth_required"]

def find_contracts():
    """Find all contract.json files in the contracts logic."""
    if not os.path.exists(CONTRACTS_DIR):
        return []
    
    # Exclude registry.json and registry-schema.json
    pattern = os.path.join(CONTRACTS_DIR, "**", "*.json")
    all_json = glob.glob(pattern, recursive=True)
    
    contracts = []
    for f in all_json:
        basename = os.path.basename(f)
        if basename not in ["registry.json", "registry-schema.json", "contract-schema.json"]:
            contracts.append(f)
            
    return contracts

def validate_contract(filepath):
    """Validate a single contract against strict enforcement rules."""
    issues = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return [f"Geçersiz JSON formatı: {e}"]
        
    # Check Required Fields
    for field in REQUIRED_FIELDS:
        if field not in data:
            issues.append(f"Zorunlu alan eksik: '{field}'")
            
    if issues:
        return issues
        
    # Check Operation Name Format (snake_case)
    operation = data.get("operation", "")
    if not re.match(r'^[a-z0-9_]+$', operation):
        issues.append(f"Hatalı isimlendirme: operation '{operation}' snake_case olmalı.")

    # Check Version Format (SemVer)
    version = data.get("version", "")
    if not re.match(r'^\d+\.\d+\.\d+$', version):
        issues.append(f"Hatalı versiyon: '{version}' SemVer (MAJOR.MINOR.PATCH) formatında olmalı.")

    # Check metadata fields
    metadata = data.get("metadata", {})
    for m_field in METADATA_REQUIRED_FIELDS:
        if m_field not in metadata:
            issues.append(f"Metadata eksik zorunlu alan: '{m_field}'")
            
    # Conditional idempotency check
    op_lower = operation.lower()
    if any(verb in op_lower for verb in ["create", "update", "delete", "post", "put", "patch"]):
        if "idempotent" not in metadata:
            issues.append(f"Idempotency eksik: Mutasyon işlemleri '{operation}' için idempotent alanı zorunludur.")
            
    return issues

def sync_registry(contracts):
    """Update registry.json based on validated contracts."""
    if not os.path.exists(REGISTRY_FILE):
        registry = {
            "$schema": "./registry-schema.json",
            "version": "1.0.0",
            "last_updated": datetime.now().isoformat() + "Z",
            "description": "Merkezi kontrat registry. Tüm API kontratları burada indekslenir.",
            "contracts": {},
            "domains": {}
        }
    else:
        try:
            with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
                registry = json.load(f)
        except Exception:
            registry = {"contracts": {}, "domains": {}}
            
    # Rebuild contracts tree
    registry["contracts"] = {}
    
    for filepath in contracts:
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
        except Exception:
            continue
            
        op = data.get("operation")
        ver = data.get("version")
        if not op or not ver:
            continue
            
        # Try to infer domain and entity from path "contracts/domain/entity/..."
        rel_path = os.path.relpath(filepath, CONTRACTS_DIR)
        parts = rel_path.split(os.sep)
        domain = parts[0] if len(parts) > 0 else "unknown"
        entity = parts[1] if len(parts) > 1 else "unknown"
        
        if op not in registry["contracts"]:
            registry["contracts"][op] = {
                "domain": domain,
                "entity": entity,
                "versions": {}
            }
            
        ver_key = f"v{ver}"
        # Normalize path separators for cross-platform compatibility
        normalized_path = rel_path.replace(os.sep, "/")
        registry["contracts"][op]["versions"][ver_key] = {
            "status": "stable",
            "path": normalized_path,
            "created_at": datetime.now().isoformat() + "Z",
            "deprecated": False
        }
        registry["contracts"][op]["latest_stable"] = ver_key
        
        # Add to domains
        if domain not in registry.get("domains", {}):
            registry.setdefault("domains", {})[domain] = {"description": f"{domain} domain", "entities": []}
        if entity not in registry["domains"][domain]["entities"]:
            registry["domains"][domain]["entities"].append(entity)

    registry["last_updated"] = datetime.now().isoformat() + "Z"
    
    with open(REGISTRY_FILE, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2)

def main():
    print("🔍 Contract Enforcement & Validation running...")
    
    action = "validate"
    if len(sys.argv) > 1 and sys.argv[1] == "sync":
        action = "sync"
        
    contracts = find_contracts()
    
    if not contracts:
        print("⚠️ Henüz 'contracts/' dizininde kontrat bulunamadı (registry hariç). Contract-First mimarisi bekleniyor.")
        if action == "sync":
            sync_registry([])
        sys.exit(0)
        
    all_issues = {}
    valid_contracts = []
    
    for c in contracts:
        issues = validate_contract(c)
        if issues:
            all_issues[c] = issues
        else:
            valid_contracts.append(c)
            
    if all_issues:
        print("❌ SÖZLEŞME (CONTRACT) İHLALİ TESPİT EDİLDİ!")
        for c, issues in all_issues.items():
            print(f"\\n📄 Dosya: {os.path.relpath(c, PROJECT_ROOT)}")
            for issue in issues:
                print(f"   - {issue}")
        print("\\nAKSİYON GEREKLİ: Uygulamanın Backend ve Frontend entegrasyonu hatalı sözleşmelerle çalışamaz. Düzeltin.")
        sys.exit(1)
    else:
        print(f"✅ Sözleşmeler doğrulandı. ({len(valid_contracts)} adet kusursuz kontrat)")
        if action == "sync":
            sync_registry(valid_contracts)
            print("📦 registry.json başarıyla güncellendi ve senkronize edildi.")
        sys.exit(0)

if __name__ == "__main__":
    main()
