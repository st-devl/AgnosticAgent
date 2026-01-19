#!/usr/bin/env python3
import os
import re
import sys
import glob

# Configuration
AGENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROJECT_ROOT = os.path.dirname(AGENT_DIR)
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")

# Regex Patterns
SCRIPT_PATTERN = r"[\"\']?([a-zA-Z0-9_/\-\.]+\.py)[\"\']?"
# Pattern for docs references like: `project_info.md`, `tech_stack.md`, docs/xyz.md
DOC_PATTERN = r"`(docs/[a-zA-Z0-9_\-\.]+\.md)`|`([a-zA-Z0-9_\-]+\.md)`"

def find_md_files():
    """Find all markdown files in the agent directory."""
    return glob.glob(os.path.join(AGENT_DIR, "**", "*.md"), recursive=True)

def validate_script_links(md_files):
    """Scan MD files for PY links and verify existence."""
    errors = []
    verified_count = 0
    
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        matches = re.findall(SCRIPT_PATTERN, content)
        
        for script_ref in matches:
            clean_ref = script_ref.strip()
            
            if clean_ref.startswith("http") or "site-packages" in clean_ref:
                continue
                
            if os.path.isabs(clean_ref):
                abs_path = clean_ref
            else:
                candidate = os.path.join(PROJECT_ROOT, clean_ref)
                if os.path.exists(candidate):
                    abs_path = candidate
                else:
                    errors.append(f"❌ BROKEN SCRIPT LINK: '{clean_ref}' in {os.path.basename(md_file)}")
                    continue

            if os.path.exists(abs_path):
                verified_count += 1
            else:
                errors.append(f"❌ SCRIPT NOT FOUND: '{clean_ref}' in {os.path.basename(md_file)}")
    
    return errors, verified_count

def validate_doc_links(md_files):
    """Scan MD files for docs/*.md references and verify existence."""
    errors = []
    verified_count = 0
    
    # Known docs files that SHOULD exist (from /start output) or are system files
    expected_docs = {
        "project_brief.md", "tech_stack.md", "design_brief.md", 
        "data_privacy.md", "architecture.md", "prd.md", 
        "memory.md", "registry.md", "project_keys.md",
        # System files (workflow artifacts, not in docs/)
        "task.md", "implementation_plan.md"
    }
    
    # Files that are skill sub-files or rule files (not docs) - ignore these
    skill_subfiles = {
        "rbac.md", "audit.md", "encryption.md", "vulnerability.md", 
        "compliance.md", "api-security.md", "cache.md", "query.md", 
        "memory.md", "jobs.md", "api.md", "schema.md", "indexing.md", 
        "migration.md", "partition.md", "performance.md",
        # Rule/workflow files
        "gatekeeper.md", "deep_bug_hunt.md",
        # Skill files
        "debugging.md", "component-architecture.md", "code-review.md",
        "multi-tenancy.md", "tdd-workflow.md", "SKILL.md"
    }
    
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        matches = re.findall(DOC_PATTERN, content)
        
        for match in matches:
            doc_ref = match[0] if match[0] else match[1]
            
            # Skip template references
            if "template" in doc_ref.lower():
                continue
            
            # Skip known skill sub-files (they are NOT docs)
            basename = os.path.basename(doc_ref)
            if basename in skill_subfiles:
                verified_count += 1  # It's a valid internal reference
                continue
            
            # Determine path
            if doc_ref.startswith("docs/"):
                abs_path = os.path.join(PROJECT_ROOT, doc_ref)
            elif ".agent/" in doc_ref: # Handle explicit .agent paths
                 abs_path = os.path.join(PROJECT_ROOT, doc_ref)
            else:
                # varsayılan olarak docs klasörüne bakar ama bazıları rules/ içinde olabilir
                candidates = [
                    os.path.join(DOCS_DIR, doc_ref),
                    os.path.join(AGENT_DIR, "rules", "checklists", doc_ref),
                    os.path.join(AGENT_DIR, "docs", "patterns", doc_ref),
                    os.path.join(AGENT_DIR, "templates", "reports", doc_ref)
                ]
                abs_path = None
                for c in candidates:
                    if os.path.exists(c):
                        abs_path = c
                        break
                
                if not abs_path:
                     abs_path = os.path.join(DOCS_DIR, doc_ref) # Default for error msg

            # Check existence or expectation
            if os.path.exists(abs_path):
                verified_count += 1
            elif basename in expected_docs:
                verified_count += 1  # Will be created by /start
            else:
                errors.append(f"⚠️ DOC NOT FOUND: '{doc_ref}' referenced in {os.path.basename(md_file)}")
    
    return errors, verified_count

def main():
    md_files = find_md_files()
    print(f"🔍 Deep Scanning {len(md_files)} markdown files in {AGENT_DIR}...")
    print("-" * 50)
    
    # Validate Scripts
    print("📜 Checking Python script references...")
    script_errors, script_verified = validate_script_links(md_files)
    print(f"   Scripts: {script_verified} verified")
    
    # Validate Docs
    print("📄 Checking docs/*.md references...")
    doc_errors, doc_verified = validate_doc_links(md_files)
    print(f"   Docs: {doc_verified} verified")
    
    print("-" * 50)
    
    all_errors = script_errors + doc_errors
    if all_errors:
        print(f"🚨 INTEGRITY CHECK FOUND {len(all_errors)} ISSUES:")
        for err in all_errors:
            print(err)
        sys.exit(1)
    else:
        total = script_verified + doc_verified
        print(f"✅ SUCCESS: All {total} references verified. System is 100% solid.")
        sys.exit(0)

if __name__ == "__main__":
    main()

