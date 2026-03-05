import os
import shutil
import argparse
import sys
import subprocess

# Ensure the current directory is in sys.path so 'antigravity' can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def get_core_dir():
    # antigravity klasörünün nerede kurulu olduğunu bul (site-packages içi)
    return os.path.dirname(os.path.abspath(__file__))

def init_project():
    print("🚀 AgnosticAgent Proje İlklendirmesi başlatılıyor...")
    
    core_dir = get_core_dir()
    target_dir = os.getcwd() # Komutun çalıştırıldığı yer (Kullanıcının projesi)
    
    # 1. docs/ klasörünü yarat
    docs_dir = os.path.join(target_dir, "docs")
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
        print("📁 docs/ klasörü oluşturuldu.")
        
    # 2. Şablon dosyaları kopyala
    # Şablonlar motorun /templates/docs/templates dizininde
    template_src = os.path.join(core_dir, "templates", "docs", "templates")
    template_dst = os.path.join(docs_dir, "templates")
    
    if os.path.exists(template_src):
        if not os.path.exists(template_dst):
             shutil.copytree(template_src, template_dst)
             print("📄 Şablon (template) dosyaları kopyalandı.")
             
        # SSOT dosyaları kullanıcı projesinde yoksa boş/şablon halini kopyala (VAR OLANLARI EZME)
        ssot_files = ["tech_stack.md", "architecture.md", "project_context.md", "prd.md", "memory.md", "registry.md"]
        for md_file in ssot_files:
            target_md = os.path.join(docs_dir, md_file)
            if not os.path.exists(target_md):
                # Şimdilik boş dosyalar oluşturuyoruz (Gerçek şablon dosyaları da çekilebilir)
                with open(target_md, "w") as f:
                    f.write(f"# {md_file.replace('.md', '')}\n\nAntigravity tarafından oluşturuldu.")
                print(f"✨ Yeni {md_file} oluşturuldu.")
            else:
                print(f"✅ {md_file} zaten var, korunuyor (Ezilmedi!).")
    

    # 3. Git Hook kurulumu
    git_hooks_dir = os.path.join(target_dir, ".git", "hooks")
    if os.path.exists(os.path.join(target_dir, ".git")):
        pre_commit_src = os.path.join(core_dir, "templates", "hooks", "pre-commit")
        pre_commit_dst = os.path.join(git_hooks_dir, "pre-commit")
        
        if os.path.exists(pre_commit_src):
             shutil.copy2(pre_commit_src, pre_commit_dst)
             os.chmod(pre_commit_dst, 0o755)
             print("🪝 .git/hooks/pre-commit kancası kuruldu.")
    else:
        print("⚠️ Bu klasör bir git reposu değil. Hook'lar kurulamadı.")
        
    print("\n🎉 Kurulum Tamamlandı! Projeniz AgnosticAgent'a bağlandı.")

def check_project():
    print("🔍 AgnosticAgent Kurallar Denetimi başlatılıyor...")
    
    # Eskiden health_check.py idi. Direkt onu çağırıyoruz:
    core_dir = get_core_dir()
    health_check_script = os.path.join(core_dir, "core", "health_check.py")
    
    if os.path.exists(health_check_script):
        subprocess.run([sys.executable, health_check_script])
    else:
        print("❌ Motor core başlatılamadı: health_check.py bulunamadı.")

def update_project():
    print("🔄 AgnosticAgent Sistem Güncellemesi başlatılıyor...")
    
    core_dir = get_core_dir()
    target_dir = os.getcwd()
    agent_dir = os.path.join(target_dir, ".agent")
    
    if not os.path.exists(agent_dir):
        print("❌ Hata: Bu dizinde kurulu bir AgnosticAgent (.agent) bulunamadı. Lütfen önce 'init' yapın.")
        return

    # 1. Güncellenecek Sistem Klasörleri
    # Bu klasörler motorun en güncel haliyle (core_dir içindekilerle) değiştirilecek
    system_folders = ["core", "rules", "skills", "workflows", "scripts", "config"]
    
    for folder in system_folders:
        src = os.path.join(core_dir, folder)
        dst = os.path.join(agent_dir, folder)
        
        # rules.yaml gibi kritik sistem dosyalarını yenile ama docs/ içindekilere dokunma
        if os.path.exists(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"✅ {folder} klasörü güncellendi.")

    # 2. Docs içindeki şablonları da güncelle
    template_src = os.path.join(core_dir, "templates", "docs", "templates")
    template_dst = os.path.join(target_dir, "docs", "templates")
    if os.path.exists(template_src):
        if os.path.exists(template_dst):
            shutil.rmtree(template_dst)
        shutil.copytree(template_src, template_dst)
        print("✅ docs/templates (Şablonlar) güncellendi.")

    # 3. Git Hook'u yenile
    pre_commit_src = os.path.join(core_dir, "templates", "hooks", "pre-commit")
    pre_commit_dst = os.path.join(target_dir, ".git", "hooks", "pre-commit")
    if os.path.exists(pre_commit_src) and os.path.exists(os.path.dirname(pre_commit_dst)):
        shutil.copy2(pre_commit_src, pre_commit_dst)
        os.chmod(pre_commit_dst, 0o755)
        print("✅ .git/hooks/pre-commit kancası yenilendi.")

    print("\n🎉 Güncelleme Başarıyla Tamamlandı!")
    print("⚠️ NOT: 'docs/*.md' (SSOT) ve '.agent/state/' (Hafıza) dosyalarınız korunmuştur.")

def watch_project():
    print("👀 AgnosticAgent Gölge Denetçi (Watcher) başlatılıyor...")
    core_dir = get_core_dir()
    watcher_script = os.path.join(core_dir, "core", "shadow_watcher.py")
    
    if os.path.exists(watcher_script):
        try:
             subprocess.run([sys.executable, watcher_script])
        except KeyboardInterrupt:
             print("\n👋 Kapatılıyor...")
    else:
        print("❌ Motor core başlatılamadı: shadow_watcher.py bulunamadı.")

def run_script(script_name, script_args):
    core_dir = get_core_dir()
    script_path = os.path.join(core_dir, "core", script_name)
    if os.path.exists(script_path):
        result = subprocess.run([sys.executable, script_path] + script_args)
        sys.exit(result.returncode)
    else:
        print(f"❌ Motor core scripti bulunamadı: {script_name}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Antigravity CLI - Proaktif Yazılım Geliştirme Asistanı")
    subparsers = parser.add_subparsers(dest="command", help="Kullanılabilir komutlar")

    # init komutu
    parser_init = subparsers.add_parser("init", help="Mevcut projenizde AgnosticAgent'ı başlatır (şablonları ve hookları kurar).")
    
    # check komutu
    parser_check = subparsers.add_parser("check", help="Mevcut projenin SSOT, mimari ve teknoloji kurallarına uygunluğunu denetler.")
    
    # update komutu
    parser_update = subparsers.add_parser("update", help="Projenizdeki sistem dosyalarını (.agent içerisindekileri) hafızanıza dokunmadan günceller.")

    # watch komutu
    parser_watch = subparsers.add_parser("watch", help="Projenizde dosya değişikliklerini canlı dinler ve anında analiz yapar.")

    # run komutu (Hook'lar için proxy)
    parser_run = subparsers.add_parser("run", help="Motor içindeki belirli bir scripti çalıştırır.")
    parser_run.add_argument("script_name", help="Çalıştırılacak scriptin adı (örn: contract_validator.py)")
    parser_run.add_argument("script_args", nargs=argparse.REMAINDER, help="Scripte iletilecek argümanlar")

    args = parser.parse_args()

    if args.command == "init":
        init_project()
    elif args.command == "check":
        check_project()
    elif args.command == "update":
        update_project()
    elif args.command == "watch":
        watch_project()
    elif args.command == "run":
        run_script(args.script_name, args.script_args)
    else:
         parser.print_help()

if __name__ == "__main__":
    main()
