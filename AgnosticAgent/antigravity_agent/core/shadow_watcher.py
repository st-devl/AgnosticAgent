#!/usr/bin/env python3
"""
watcher.py
Real-time "Shadow Watcher" for Antigravity Agent.
Monitors file changes and runs static analysis tools instantly to provide immediate feedback.
"""

import time
import subprocess
import os
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))

class AntigravityWatcher(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.last_trigger = 0
        self.cooldown = 1.0 # 1 second cooldown to avoid rapid triggers
        
        # Define validators
        self.validators = {
            'config_enforcer': os.path.join(SCRIPT_DIR, 'config_enforcer.py'),
            'contract_validator': os.path.join(SCRIPT_DIR, 'contract_validator.py'),
            'tech_stack_enforcer': os.path.join(SCRIPT_DIR, 'tech_stack_enforcer.py'),
            'secret_scanner': os.path.join(SCRIPT_DIR, 'secret_scanner.py')
        }

    def on_modified(self, event):
        if event.is_directory:
            return
            
        # Ignore changes in .git, node_modules, vendor, etc.
        ignored_dirs = ['.git', 'node_modules', 'vendor', '.agent/logs']
        if any(ignored in event.src_path for ignored in ignored_dirs):
            return

        # Rate limiting
        current_time = time.time()
        if current_time - self.last_trigger < self.cooldown:
            return
            
        # Monitored file extensions
        if event.src_path.endswith(('.php', '.ts', '.js', '.py', '.json', '.md')):
            self.last_trigger = current_time
            self.run_analysis(event.src_path)

    def run_analysis(self, filepath):
        rel_path = os.path.relpath(filepath, PROJECT_ROOT)
        print(f"\n" + "="*50)
        print(f"👀 Gölge Denetçi: {rel_path} değiştirildi.")
        print(f"🔄 Analiz yapılıyor...")
        
        has_errors = False
        
        # 1. Secret Scanner (Alwasy run first for security)
        if os.path.exists(self.validators['secret_scanner']):
            result = subprocess.run([sys.executable, self.validators['secret_scanner'], filepath], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ [SECRET SCANNER] İhlal tespit edildi!\n{result.stdout or result.stderr}")
                has_errors = True
                
        # 2. Config Enforcer (Run on code files)
        if filepath.endswith(('.php', '.ts', '.js', '.py')) and os.path.exists(self.validators['config_enforcer']):
            result = subprocess.run([sys.executable, self.validators['config_enforcer'], filepath], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print(f"⚠️ [MİMARİ] Kural ihlali!\n{result.stdout or result.stderr}")
                has_errors = True
                
        # 3. Contract Validator (Run on contract JSONs)
        if 'contracts' in filepath and filepath.endswith('.json') and os.path.exists(self.validators['contract_validator']):
            result = subprocess.run([sys.executable, self.validators['contract_validator'], filepath], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print(f"⚠️ [KONTRAT] Standart hatası!\n{result.stdout or result.stderr}")
                has_errors = True
        
        if not has_errors:
            print(f"✅ Temiz. İhlal bulunmadı.")
        print("="*50)

def main():
    print("🤖 Antigravity Gölge Denetçi Başladı.")
    print("📌 Kod yazmanı arkaplanda izliyorum...")
    print("📌 Durdurmak için CTRL+C yapabilirsin.\n")
    
    event_handler = AntigravityWatcher()
    observer = Observer()
    observer.schedule(event_handler, PROJECT_ROOT, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Gölge Denetçi durduruluyor...")
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
