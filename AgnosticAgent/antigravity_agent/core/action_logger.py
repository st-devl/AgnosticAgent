#!/usr/bin/env python3
"""
action_logger.py
Enterprise-grade audit trail for all agent actions.
Logs every significant action with context, rule basis, and outcome.

v2.0 Changes:
- Added log rotation (max 10MB per file, archives old logs)
- Added retention enforcement (90 days from rules.yaml)
- Graceful handling of corrupted log files
"""

import os
import json
import hashlib
import shutil
from datetime import datetime, timezone, timedelta

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up two levels: core -> scripts -> .agent
AGENT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
LOGS_DIR = os.path.join(AGENT_DIR, "logs")
ARCHIVE_DIR = os.path.join(LOGS_DIR, "archive")
ACTION_LOG = os.path.join(LOGS_DIR, "actions.jsonl")
DECISION_LOG = os.path.join(LOGS_DIR, "decisions.jsonl")
ERROR_LOG = os.path.join(LOGS_DIR, "errors.jsonl")

# Log rotation settings
MAX_LOG_SIZE_BYTES = 10 * 1024 * 1024  # 10MB
RETENTION_DAYS = 90

# Ensure directories exist
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)


def _rotate_if_needed(log_file):
    """Rotate log file if it exceeds MAX_LOG_SIZE_BYTES."""
    if not os.path.exists(log_file):
        return

    if os.path.getsize(log_file) < MAX_LOG_SIZE_BYTES:
        return

    # Archive the current file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    basename = os.path.basename(log_file)
    archive_name = f"{os.path.splitext(basename)[0]}_{timestamp}.jsonl"
    archive_path = os.path.join(ARCHIVE_DIR, archive_name)

    shutil.move(log_file, archive_path)

    # Clean up old archives beyond retention period
    _cleanup_old_archives()


def _cleanup_old_archives():
    """Remove archived log files older than RETENTION_DAYS."""
    if not os.path.exists(ARCHIVE_DIR):
        return

    cutoff = datetime.now() - timedelta(days=RETENTION_DAYS)

    for filename in os.listdir(ARCHIVE_DIR):
        filepath = os.path.join(ARCHIVE_DIR, filename)
        if os.path.isfile(filepath):
            file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            if file_mtime < cutoff:
                os.remove(filepath)


def get_file_hash(filepath):
    """Get SHA256 hash of a file for integrity tracking."""
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()[:12]
    except IOError:
        return None


def log_action(action_type, target, rule_basis=None, approval_source=None,
               success=True, details=None, reasoning=None):
    """
    Log an agent action to the audit trail.

    Args:
        action_type: Type of action (write_file, run_command, etc.)
        target: Target of the action (filepath, command, etc.)
        rule_basis: Which rule authorized this action
        approval_source: Where user approval came from
        success: Whether the action succeeded
        details: Additional details dict
        reasoning: WHY this action was taken (reasoning trace)
    """
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action_type,
        "target": target,
        "rule_basis": rule_basis,
        "approval_source": approval_source,
        "success": success,
        "reasoning": reasoning,
        "details": details or {}
    }

    # Add file hash if target is a file
    if action_type in ["write_file", "replace_content", "delete_file"]:
        entry["checksum_after"] = get_file_hash(target)

    _append_log(ACTION_LOG, entry)

    # Also log to reasoning trace if reasoning provided
    if reasoning:
        log_reasoning(action_type, target, reasoning)

    return entry


def log_reasoning(action, target, reasoning):
    """
    Log reasoning trace - WHY an action was taken.

    Args:
        action: Action type
        target: Target of action
        reasoning: Detailed explanation of WHY
    """
    reasoning_log = os.path.join(LOGS_DIR, "reasoning.jsonl")
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "target": target,
        "reasoning": reasoning
    }
    _append_log(reasoning_log, entry)
    return entry


def log_decision(decision, reason, alternatives=None, risk_level="low"):
    """
    Log a decision made by the agent.

    Args:
        decision: What was decided
        reason: Why this decision was made
        alternatives: Other options considered
        risk_level: low, medium, high, critical
    """
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "reason": reason,
        "alternatives": alternatives or [],
        "risk_level": risk_level
    }

    _append_log(DECISION_LOG, entry)
    return entry


def log_error(error_type, message, context=None, recoverable=True):
    """
    Log an error or exception.

    Args:
        error_type: Type of error
        message: Error message
        context: Additional context dict
        recoverable: Whether the system can continue
    """
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "error_type": error_type,
        "message": message,
        "context": context or {},
        "recoverable": recoverable
    }

    _append_log(ERROR_LOG, entry)
    return entry


def _append_log(log_file, entry):
    """Append an entry to a JSONL log file with rotation check."""
    _rotate_if_needed(log_file)
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    except IOError:
        pass  # Fail silently — logging should never crash the system


def get_recent_actions(limit=10):
    """Get the most recent actions from the log."""
    if not os.path.exists(ACTION_LOG):
        return []

    try:
        with open(ACTION_LOG, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        entries = []
        for line in lines[-limit:]:
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return entries
    except IOError:
        return []


def get_action_summary():
    """Get a summary of all logged actions."""
    if not os.path.exists(ACTION_LOG):
        return {"total": 0, "by_type": {}, "success_rate": 0}

    try:
        with open(ACTION_LOG, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        by_type = {}
        success_count = 0
        total = 0

        for line in lines:
            try:
                entry = json.loads(line)
                total += 1
                action = entry.get("action", "unknown")
                by_type[action] = by_type.get(action, 0) + 1
                if entry.get("success", False):
                    success_count += 1
            except json.JSONDecodeError:
                continue

        return {
            "total": total,
            "by_type": by_type,
            "success_rate": round(success_count / total * 100, 1) if total > 0 else 0
        }
    except IOError:
        return {"total": 0, "by_type": {}, "success_rate": 0}


# CLI Interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: action_logger.py [summary|recent|log <action> <target>|rotate]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "summary":
        summary = get_action_summary()
        print(f"📊 Action Log Summary")
        print(f"   Total Actions: {summary['total']}")
        print(f"   Success Rate: {summary['success_rate']}%")
        print(f"   By Type: {summary['by_type']}")

    elif command == "recent":
        actions = get_recent_actions()
        print(f"📋 Recent Actions ({len(actions)})")
        for a in actions:
            print(f"   [{a['timestamp'][:19]}] {a['action']} → {a['target']}")

    elif command == "log" and len(sys.argv) >= 4:
        action = sys.argv[2]
        target = sys.argv[3]
        log_action(action, target)
        print(f"✅ Logged: {action} on {target}")

    elif command == "rotate":
        for log_file in [ACTION_LOG, DECISION_LOG, ERROR_LOG]:
            if os.path.exists(log_file):
                size_mb = os.path.getsize(log_file) / (1024 * 1024)
                print(f"   {os.path.basename(log_file)}: {size_mb:.2f} MB")
                _rotate_if_needed(log_file)
        _cleanup_old_archives()
        print("✅ Log rotation complete")

    else:
        print("Unknown command")
        sys.exit(1)
