#!/usr/bin/env python3
"""
gen_report.py
Otomatik rapor oluşturucu.
Kullanım: python3 gen_report.py --type feature --name "Login Refactor"
"""

import os
import sys
import argparse
from datetime import datetime

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
TEMPLATES_DIR = os.path.join(AGENT_DIR, "templates", "reports")
BRAIN_DIR = os.path.join(os.path.dirname(AGENT_DIR), ".gemini/antigravity/brain") # Not actually reachable like this easily, use CWD usually

def generate_report(report_type, name):
    template_map = {
        "feature": "feature_report.md",
        "security": "security_audit_report.md"
    }
    
    template_file = template_map.get(report_type)
    if not template_file:
        print(f"❌ Unknown report type: {report_type}")
        return

    template_path = os.path.join(TEMPLATES_DIR, template_file)
    
    if not os.path.exists(template_path):
        print(f"❌ Template not found: {template_path}")
        return
        
    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Basit replace
    content = content.replace("{{ feature_name }}", name)
    content = content.replace("{{ critical_count }}", "0")
    content = content.replace("{{ high_count }}", "0")
    
    # Rapor adı
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    report_name = f"{report_type}_report_{timestamp}.md"
    
    # docs/reports/ dizinine yaz
    reports_dir = os.path.join(os.path.dirname(AGENT_DIR), "docs", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    report_path = os.path.join(reports_dir, report_name)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"✅ Report generated: {report_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate Workflow Report")
    parser.add_argument("--type", required=True, choices=["feature", "security"], help="Report type")
    parser.add_argument("--name", default="Unnamed Task", help="Task/Feature name")
    
    args = parser.parse_args()
    generate_report(args.type, args.name)

if __name__ == "__main__":
    main()
