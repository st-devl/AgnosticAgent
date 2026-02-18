#!/usr/bin/env python3
"""
log_analyzer.py
Analyzes Laravel log files to identify slow queries and high error rates.
Now powered by sibling MD files as configuration sources.
"""

import re
import sys
import os
from collections import Counter

# Path Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)  # performance/

# Default Patterns
DEFAULT_PATTERNS = {
    "SLOW_QUERY": r"Query time: ([0-9\.]+)ms",
    "ERROR": r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] \w+\.ERROR: (.+?) \{",
    "EXCEPTION": r"Exception: (.+?) in"
}

# Default Thresholds
DEFAULT_THRESHOLDS = {
    "slow_query_ms": 100.0,
    "api_response_ms": 200.0
}

def load_config_from_md():
    """Loads TTL and threshold configurations from cache.md and query.md."""
    config = dict(DEFAULT_THRESHOLDS)
    loaded_count = 0
    
    # Read cache.md for TTL strategies
    cache_file = os.path.join(SKILL_DIR, "cache.md")
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract TTL table values
        ttl_match = re.search(r'\|\s*Dashboard stats\s*\|\s*(\d+)\s*dakika', content)
        if ttl_match:
            config["dashboard_ttl_min"] = int(ttl_match.group(1))
            loaded_count += 1
    
    # Read query.md for N+1 patterns (if exists)
    query_file = os.path.join(SKILL_DIR, "query.md")
    if os.path.exists(query_file):
        with open(query_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for threshold values
        threshold_match = re.search(r'(\d+)ms', content)
        if threshold_match:
            config["slow_query_ms"] = float(threshold_match.group(1))
            loaded_count += 1
    
    # Read api.md for API response targets
    api_file = os.path.join(SKILL_DIR, "api.md")
    if os.path.exists(api_file):
        with open(api_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        api_match = re.search(r'<\s*(\d+)ms', content)
        if api_match:
            config["api_response_ms"] = float(api_match.group(1))
            loaded_count += 1
    
    if loaded_count > 0:
        print(f"📖 Loaded {loaded_count} config values from MD files")
    
    return config

def analyze_log(logfile, config):
    if not os.path.exists(logfile):
        print(f"❌ Log file not found: {logfile}")
        return

    threshold_ms = config.get("slow_query_ms", 100.0)
    
    print(f"📊 Analyzing {logfile}...")
    print(f"   Slow query threshold: {threshold_ms}ms")
    print("-" * 50)

    slow_queries = []
    errors = Counter()
    exceptions = Counter()

    with open(logfile, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            msg = line.strip()
            
            # Check for slow queries
            slow_match = re.search(DEFAULT_PATTERNS["SLOW_QUERY"], msg)
            if slow_match:
                query_time = float(slow_match.group(1))
                if query_time > threshold_ms:
                    slow_queries.append(query_time)
            
            # Simple Error Counting
            if ".ERROR:" in msg:
                match = re.search(DEFAULT_PATTERNS["ERROR"], msg)
                if match:
                    errors[match.group(1)] += 1
                else:
                    errors["Generic Error"] += 1

            # Check for Exceptions
            if "Exception:" in msg:
                match = re.search(DEFAULT_PATTERNS["EXCEPTION"], msg)
                if match:
                    exceptions[match.group(1)] += 1

    # Report
    print(f"🐌 Slow Queries (>{threshold_ms}ms): {len(slow_queries)}")
    if slow_queries:
        print(f"   Average: {sum(slow_queries)/len(slow_queries):.2f}ms")
        print(f"   Max: {max(slow_queries):.2f}ms")
    
    print(f"\n🔴 Total Errors: {sum(errors.values())}")
    for err, count in errors.most_common(5):
        print(f"   - {count}x {err[:60]}...")
        
    print(f"\n⚡ Exceptions: {sum(exceptions.values())}")
    for exc, count in exceptions.most_common(5):
        print(f"   - {count}x {exc}")

if __name__ == "__main__":
    config = load_config_from_md()
    print(f"📋 Config: {config}")
    print("-" * 50)
    
    target_log = sys.argv[1] if len(sys.argv) > 1 else "storage/logs/laravel.log"
    analyze_log(target_log, config)

