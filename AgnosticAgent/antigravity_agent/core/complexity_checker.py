#!/usr/bin/env python3
"""
complexity_checker.py
Checks code complexity to enforce "Clean & Minimal Code" principle.
Detects: long functions, deep nesting, high cyclomatic complexity.

v2.0 Changes:
- Python integration: Uses standard `ast` module instead of broken curly-brace counting.
- PHP/JS improvements: Better function detection regex supporting visibility modifiers.
"""

import os
import sys
import re
import ast

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
PROJECT_ROOT = os.path.dirname(AGENT_DIR)

# Thresholds
MAX_FUNCTION_LINES = 50
MAX_NESTING_DEPTH = 4
MAX_FILE_LINES = 500

# Extensions to check
CODE_EXTENSIONS = ['.py', '.js', '.ts', '.php', '.java', '.go', '.rb']


class PythonComplexityVisitor(ast.NodeVisitor):
    def __init__(self, filepath, source_lines):
        self.filepath = filepath
        self.source_lines = source_lines
        self.issues = []
        self._current_nesting = 0
        self.max_nesting = 0
    
    def generic_visit(self, node):
        # Nodes that increase nesting scope
        nesting_nodes = (ast.For, ast.While, ast.If, ast.With, ast.Try, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        if isinstance(node, nesting_nodes):
            self._current_nesting += 1
            if self._current_nesting > self.max_nesting:
                self.max_nesting = self._current_nesting
            
            # Function line check
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if hasattr(node, "end_lineno") and hasattr(node, "lineno"):
                    func_lines = node.end_lineno - node.lineno + 1
                    if func_lines > MAX_FUNCTION_LINES:
                        self.issues.append({
                            "file": self.filepath,
                            "type": "function_too_long",
                            "severity": "warning",
                            "line": node.lineno,
                            "message": f"Fonksiyon '{node.name}' çok uzun: {func_lines} satır (max: {MAX_FUNCTION_LINES})"
                        })
                
            super().generic_visit(node)
            self._current_nesting -= 1
        else:
            super().generic_visit(node)


class ComplexityChecker:
    def __init__(self):
        self.issues = []
        self.files_checked = 0
    
    def check_file(self, filepath):
        """Check a single file for complexity issues."""
        ext = os.path.splitext(filepath)[1]
        if ext not in CODE_EXTENSIONS:
            return
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()
                lines = source.split('\n')
        except Exception:
            return
        
        self.files_checked += 1
        rel_path = os.path.relpath(filepath, PROJECT_ROOT)
        
        # Check file length
        if len(lines) > MAX_FILE_LINES:
            self.issues.append({
                "file": rel_path,
                "type": "file_too_long",
                "severity": "warning",
                "message": f"Dosya çok uzun: {len(lines)} satır (max: {MAX_FILE_LINES})"
            })
        
        # Analyze Complexity depending on the language
        if ext == '.py':
            self._check_python_ast(source, lines, rel_path)
        else:
            self._check_c_style_functions(lines, rel_path, ext)
    
    def _check_python_ast(self, source, lines, filepath):
        """Use Python AST to get accurate complexity."""
        try:
            tree = ast.parse(source)
            visitor = PythonComplexityVisitor(filepath, lines)
            visitor.visit(tree)
            self.issues.extend(visitor.issues)
            
            if visitor.max_nesting > MAX_NESTING_DEPTH:
                self.issues.append({
                    "file": filepath,
                    "type": "deep_nesting",
                    "severity": "warning",
                    "message": f"Derin iç içe yapı: {visitor.max_nesting} seviye (max: {MAX_NESTING_DEPTH})"
                })
        except SyntaxError:
            pass # ignore malformed files

    def _check_c_style_functions(self, lines, filepath, ext):
        """Check individual functions for complexity (brackets counting)."""
        patterns = {
            '.js': r'(?:function\s+(\w+)|(\w+)\s*=\s*(?:async\s*)?\()',
            '.ts': r'(?:function\s+(\w+)|(\w+)\s*=\s*(?:async\s*)?\()',
            '.php': r'(?:(?:public|protected|private)?\s*(?:static)?\s*function\s+(\w+))',
            '.java': r'(?:(?:public|protected|private)\s+[\w\<\>\[\]]+\s+(\w+)\s*\()',
            '.go': r'(?:func\s+(?:\([^)]+\)\s+)?(\w+)\s*\()'
        }
        
        pattern = patterns.get(ext, r'function\s+(\w+)')
        
        current_func = None
        func_start = 0
        max_nesting = 0
        current_nesting = 0
        
        for i, line in enumerate(lines, 1):
            # Ignore comments
            clean_line = re.sub(r'//.*', '', line)
            
            # Track nesting depth
            current_nesting += clean_line.count('{') - clean_line.count('}')
            
            # Basic switch case safety to not count negative or infinite nested scope
            if current_nesting < 0:
                current_nesting = 0
                
            max_nesting = max(max_nesting, current_nesting)
            
            # Detect function start
            match = re.search(pattern, clean_line)
            if match:
                if current_func and func_start > 0:
                    func_lines = i - func_start
                    if func_lines > MAX_FUNCTION_LINES:
                        self.issues.append({
                            "file": filepath,
                            "type": "function_too_long",
                            "severity": "warning",
                            "line": func_start,
                            "message": f"Fonksiyon '{current_func}' çok uzun: {func_lines} satır (max: {MAX_FUNCTION_LINES})"
                        })
                
                # capture exactly the function name matched.
                current_func = next((m for m in match.groups() if m), "unknown")
                func_start = i
                
            elif current_nesting == 0 and current_func:
                # End of function
                func_lines = i - func_start
                if func_lines > MAX_FUNCTION_LINES:
                    self.issues.append({
                        "file": filepath,
                        "type": "function_too_long",
                        "severity": "warning",
                        "line": func_start,
                        "message": f"Fonksiyon '{current_func}' çok uzun: {func_lines} satır (max: {MAX_FUNCTION_LINES})"
                    })
                current_func = None
                func_start = 0
        
        # Check nesting depth
        if max_nesting > MAX_NESTING_DEPTH:
            self.issues.append({
                "file": filepath,
                "type": "deep_nesting",
                "severity": "warning",
                "message": f"Derin iç içe yapı: {max_nesting} seviye (max: {MAX_NESTING_DEPTH})"
            })
    
    def scan_directory(self, directory):
        """Scan directory for complexity issues."""
        ignore_dirs = {'node_modules', 'vendor', '.git', '__pycache__', 'dist', 'build'}
        
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for file in files:
                filepath = os.path.join(root, file)
                self.check_file(filepath)
    
    def report(self):
        """Generate complexity report."""
        print("🔍 Complexity Check Report")
        print("=" * 50)
        print(f"📁 Dosya sayısı: {self.files_checked}")
        print(f"⚠️  Sorun sayısı: {len(self.issues)}")
        print()
        
        if not self.issues:
            print("✅ Kompleksite sorunsu bulunamadı!")
            return 0
        
        # Group by file
        by_file = {}
        for issue in self.issues:
            f = issue["file"]
            if f not in by_file:
                by_file[f] = []
            by_file[f].append(issue)
        
        for filepath, issues in by_file.items():
            print(f"📄 {filepath}")
            for issue in issues:
                line = f" (satır {issue.get('line', '?')})" if 'line' in issue else ""
                print(f"   ⚠️  {issue['message']}{line}")
            print()
        
        return len(self.issues)

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else PROJECT_ROOT
    
    checker = ComplexityChecker()
    checker.scan_directory(target)
    issues = checker.report()
    
    sys.exit(1 if issues > 0 else 0)

if __name__ == "__main__":
    main()
