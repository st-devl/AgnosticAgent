#!/usr/bin/env python3
"""
Example: How to use reasoning trace
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from scripts.core.action_logger import log_action

# Example 1: Log action WITH reasoning
log_action(
    action_type="delete_file",
    target="old_config.yaml",
    reasoning="This file hasn't been used in 90 days and violates the artifact retention policy (30 days max). Deleting to reduce system bloat.",
    success=True
)

# Example 2: Log action WITHOUT reasoning (old style still works)
log_action(
    action_type="write_file",
    target="new_config.yaml",
    success=True
)

print("✅ Logged actions with and without reasoning trace!")
print("Check: .agent/logs/reasoning.jsonl")
