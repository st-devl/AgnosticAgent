import os
import shutil
import argparse
import sys
import subprocess


VERSION = "2.0.0"


def get_core_dir():
    """antigravity_agent paketinin kurulu olduğu dizini döndürür."""
    return os.path.dirname(os.path.abspath(__file__))


def get_templates_dir():
    """Paket içindeki templates/ dizinini döndürür."""
    return os.path.join(get_core_dir(), "templates")


def _safe_copytree(src, dst, ignore_patterns=None):
    """Kaynak dizini hedefe güvenli şekilde kopyalar."""
    if ignore_patterns:
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*ignore_patterns))
    else:
        shutil.copytree(src, dst)


def _copy_if_not_exists(src_file, dst_file):
    """Hedef dosya yoksa kopyalar, varsa korur."""
    if not os.path.exists(dst_file):
        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
        shutil.copy2(src_file, dst_file)
        return True
    return False


def _ensure_dir(path):
    """Dizin yoksa oluşturur."""
    os.makedirs(path, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════
# INIT — Sıfırdan tam kurulum
# ═══════════════════════════════════════════════════════════════════

def init_project():
    """
    Projeye AgnosticAgent altyapısını sıfırdan kurar.
    Tüm .agent/, docs/, contracts/ yapısını eksiksiz oluşturur.
    """
    print(f"🚀 AgnosticAgent v{VERSION} — Proje İlklendirmesi başlatılıyor...")

    templates_dir = get_templates_dir()
    target_dir = os.getcwd()

    # Validasyon: templates/ dizini var mı?
    if not os.path.exists(templates_dir):
        print("❌ HATA: Paket template dosyaları bulunamadı!")
        print("   Lütfen paketi yeniden kurun: pip3 install ... --upgrade --force-reinstall")
        sys.exit(1)

    agent_template = os.path.join(templates_dir, "agent")
    docs_template = os.path.join(templates_dir, "docs")
    contracts_template = os.path.join(templates_dir, "contracts")

    errors = []
    success_count = 0

    # ── 1. .agent/ dizini ──
    agent_dst = os.path.join(target_dir, ".agent")
    if os.path.exists(agent_dst):
        print("⚠️  .agent/ dizini zaten mevcut. Üzerine yazmak için 'antigravity update' kullanın.")
    else:
        if os.path.exists(agent_template):
            try:
                _safe_copytree(agent_template, agent_dst, ignore_patterns=['__pycache__', '*.pyc', '.DS_Store'])
                success_count += 1
                print("✅ .agent/ dizini oluşturuldu (rules, skills, workflows, scripts, config, hooks)")
            except Exception as e:
                errors.append(f".agent/ kopyalama hatası: {e}")
        else:
            errors.append(".agent/ template bulunamadı")

    # ── 2. docs/ dizini ──
    docs_dst = os.path.join(target_dir, "docs")
    _ensure_dir(docs_dst)

    if os.path.exists(docs_template):
        # 2a. docs/templates/ → her zaman kopyalanır
        templates_src = os.path.join(docs_template, "templates")
        templates_dst = os.path.join(docs_dst, "templates")
        if os.path.exists(templates_src):
            if not os.path.exists(templates_dst):
                try:
                    _safe_copytree(templates_src, templates_dst)
                    print("✅ docs/templates/ (şablon dosyaları) kopyalandı")
                except Exception as e:
                    errors.append(f"docs/templates/ hatası: {e}")
            else:
                print("✅ docs/templates/ zaten var, korunuyor")

        # 2b. docs/reports/ → yoksa kopyalanır
        reports_src = os.path.join(docs_template, "reports")
        reports_dst = os.path.join(docs_dst, "reports")
        if os.path.exists(reports_src) and not os.path.exists(reports_dst):
            try:
                _safe_copytree(reports_src, reports_dst)
                print("✅ docs/reports/ kopyalandı")
            except Exception as e:
                errors.append(f"docs/reports/ hatası: {e}")

        # 2c. SSOT dosyaları → SADECE YOKSA kopyalanır (kullanıcı verileri)
        ssot_files = [
            "tech_stack.md", "architecture.md", "prd.md", "memory.md",
            "registry.md", "decision_log.md", "project_brief.md",
            "design_brief.md", "data_privacy.md", "secret_policy.md",
            "project_keys.md"
        ]
        for md_file in ssot_files:
            src = os.path.join(docs_template, md_file)
            dst = os.path.join(docs_dst, md_file)
            if os.path.exists(src):
                if _copy_if_not_exists(src, dst):
                    print(f"  ✨ docs/{md_file} oluşturuldu")
                else:
                    print(f"  ✅ docs/{md_file} zaten var, korunuyor (ezilmedi!)")

        success_count += 1
    else:
        errors.append("docs/ template bulunamadı")

    # ── 3. contracts/ dizini ──
    contracts_dst = os.path.join(target_dir, "contracts")
    if os.path.exists(contracts_template):
        if not os.path.exists(contracts_dst):
            try:
                _safe_copytree(contracts_template, contracts_dst, ignore_patterns=['.DS_Store'])
                success_count += 1
                print("✅ contracts/ dizini oluşturuldu")
            except Exception as e:
                errors.append(f"contracts/ hatası: {e}")
        else:
            print("✅ contracts/ zaten var, korunuyor")
    else:
        errors.append("contracts/ template bulunamadı")

    # ── 4. Git Hook kurulumu ──
    git_dir = os.path.join(target_dir, ".git")
    if os.path.exists(git_dir):
        git_hooks_dir = os.path.join(git_dir, "hooks")
        _ensure_dir(git_hooks_dir)

        # pre-commit hook'u kopyala
        hook_src = os.path.join(agent_dst, "hooks", "pre-commit")
        if not os.path.exists(hook_src):
            hook_src = os.path.join(agent_template, "hooks", "pre-commit")

        hook_dst = os.path.join(git_hooks_dir, "pre-commit")
        if os.path.exists(hook_src):
            try:
                shutil.copy2(hook_src, hook_dst)
                os.chmod(hook_dst, 0o755)
                print("✅ .git/hooks/pre-commit hook'u kuruldu")
            except Exception as e:
                errors.append(f"Git hook hatası: {e}")
        else:
            errors.append("pre-commit hook template bulunamadı")
    else:
        print("⚠️  Bu klasör bir git reposu değil. Git hook'ları kurulamadı.")
        print("   Eğer sonradan git init yaparsanız, 'antigravity update' ile hook'ları kurabilirsiniz.")

    # ── Sonuç raporu ──
    print("\n" + "═" * 50)
    if errors:
        print(f"⚠️  Kurulum tamamlandı, ancak {len(errors)} sorun var:")
        for err in errors:
            print(f"   ❌ {err}")
    else:
        print("🎉 Kurulum 100% başarıyla tamamlandı!")
        print(f"   ✅ {success_count} ana bileşen kuruldu")

    print("\n📋 Sonraki adımlar:")
    print("   1. antigravity check  → Sistem sağlık kontrolü")
    print("   2. /start             → Proje röportajını başlat")


# ═══════════════════════════════════════════════════════════════════
# UPDATE — Mevcut projeyi güncelleme (SSOT ve hafıza korunur)
# ═══════════════════════════════════════════════════════════════════

# Güncelleme sırasında YENİLENECEK (üzerine yazılacak) sistem klasörleri
SYSTEM_FOLDERS = [
    "config",
    "rules",
    "scripts",
    "skills",
    "workflows",
    "hooks",
    "templates",
]

# Güncelleme sırasında ASLA dokunulmayacak klasörler
PRESERVED_FOLDERS = [
    "state",
    "logs",
    "cache",
    "backups",
    "docs",
]


def update_project():
    """
    Mevcut projenin sistem dosyalarını günceller.
    SSOT dosyaları ve hafıza ASLA silinmez/ezilmez.
    Eski/kullanılmayan dosyalar otomatik temizlenir.
    """
    print(f"🔄 AgnosticAgent v{VERSION} — Sistem Güncellemesi başlatılıyor...")

    templates_dir = get_templates_dir()
    target_dir = os.getcwd()
    agent_dir = os.path.join(target_dir, ".agent")

    # Validasyon
    if not os.path.exists(templates_dir):
        print("❌ HATA: Paket template dosyaları bulunamadı!")
        print("   Lütfen paketi yeniden kurun: pip3 install ... --upgrade --force-reinstall")
        sys.exit(1)

    agent_template = os.path.join(templates_dir, "agent")

    if not os.path.exists(agent_dir):
        print("❌ HATA: Bu dizinde kurulu bir AgnosticAgent (.agent) bulunamadı.")
        print("   Lütfen önce 'antigravity init' ile kurulum yapın.")
        return

    errors = []
    updated = []
    preserved = []

    # ── 1. Sistem klasörlerini güncelle ──
    print("\n📦 Sistem dosyaları güncelleniyor...")
    for folder in SYSTEM_FOLDERS:
        src = os.path.join(agent_template, folder)
        dst = os.path.join(agent_dir, folder)

        if os.path.exists(src):
            try:
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                _safe_copytree(src, dst, ignore_patterns=['__pycache__', '*.pyc', '.DS_Store'])
                updated.append(folder)
                print(f"  ✅ .agent/{folder}/ güncellendi")
            except Exception as e:
                errors.append(f".agent/{folder}/ güncelleme hatası: {e}")
        else:
            print(f"  ⚠️  .agent/{folder}/ kaynak bulunamadı, atlanıyor")

    # ── 2. Korunan klasörleri kontrol et (sadece yoksa oluştur) ──
    print("\n🛡️  Korunan dosyalar kontrol ediliyor...")
    for folder in PRESERVED_FOLDERS:
        dst = os.path.join(agent_dir, folder)
        if os.path.exists(dst):
            preserved.append(folder)
            print(f"  🔒 .agent/{folder}/ korunuyor (dokunulmadı)")
        else:
            _ensure_dir(dst)
            print(f"  ✨ .agent/{folder}/ oluşturuldu (eksikti)")

    # ── 3. docs/templates/ güncelle (SSOT dosyalarına dokunma!) ──
    print("\n📄 Dokümantasyon şablonları güncelleniyor...")
    docs_template = os.path.join(templates_dir, "docs")
    docs_dst = os.path.join(target_dir, "docs")

    if os.path.exists(docs_template):
        # templates/ alt dizini → her zaman yenilenir
        templates_src = os.path.join(docs_template, "templates")
        templates_dst = os.path.join(docs_dst, "templates")
        if os.path.exists(templates_src):
            if os.path.exists(templates_dst):
                shutil.rmtree(templates_dst)
            _safe_copytree(templates_src, templates_dst)
            print("  ✅ docs/templates/ güncellendi")

        # SSOT dosyaları → SADECE YOKSA kopyalanır
        ssot_files = [
            "tech_stack.md", "architecture.md", "prd.md", "memory.md",
            "registry.md", "decision_log.md", "project_brief.md",
            "design_brief.md", "data_privacy.md", "secret_policy.md",
            "project_keys.md"
        ]
        for md_file in ssot_files:
            src = os.path.join(docs_template, md_file)
            dst = os.path.join(docs_dst, md_file)
            if os.path.exists(src) and not os.path.exists(dst):
                shutil.copy2(src, dst)
                print(f"  ✨ docs/{md_file} oluşturuldu (daha önce yoktu)")
            elif os.path.exists(dst):
                print(f"  🔒 docs/{md_file} korunuyor (ezilmedi!)")

    # ── 4. contracts/registry-schema.json güncelle ──
    contracts_template = os.path.join(templates_dir, "contracts")
    contracts_dst = os.path.join(target_dir, "contracts")

    if os.path.exists(contracts_template):
        _ensure_dir(contracts_dst)
        # registry-schema.json → her zaman güncellenir
        schema_src = os.path.join(contracts_template, "registry-schema.json")
        if os.path.exists(schema_src):
            shutil.copy2(schema_src, os.path.join(contracts_dst, "registry-schema.json"))
            print("  ✅ contracts/registry-schema.json güncellendi")

        # registry.json → sadece yoksa
        registry_src = os.path.join(contracts_template, "registry.json")
        registry_dst = os.path.join(contracts_dst, "registry.json")
        if os.path.exists(registry_src) and not os.path.exists(registry_dst):
            shutil.copy2(registry_src, registry_dst)
            print("  ✨ contracts/registry.json oluşturuldu")
        elif os.path.exists(registry_dst):
            print("  🔒 contracts/registry.json korunuyor")

    # ── 5. Git Hook güncelle ──
    git_hooks_dir = os.path.join(target_dir, ".git", "hooks")
    hook_src = os.path.join(agent_dir, "hooks", "pre-commit")
    hook_dst = os.path.join(git_hooks_dir, "pre-commit")
    if os.path.exists(hook_src) and os.path.exists(git_hooks_dir):
        shutil.copy2(hook_src, hook_dst)
        os.chmod(hook_dst, 0o755)
        print("  ✅ .git/hooks/pre-commit güncellendi")

    # ── Sonuç raporu ──
    print("\n" + "═" * 50)
    if errors:
        print(f"⚠️  Güncelleme tamamlandı, ancak {len(errors)} sorun var:")
        for err in errors:
            print(f"   ❌ {err}")
    else:
        print("🎉 Güncelleme 100% başarıyla tamamlandı!")

    print(f"\n📊 Özet:")
    print(f"   ✅ Güncellenen: {len(updated)} klasör ({', '.join(updated)})")
    print(f"   🔒 Korunan:    {len(preserved)} klasör ({', '.join(preserved)})")
    print(f"   🔒 SSOT dosyaları hiç değiştirilmedi")

    if errors:
        for err in errors:
            print(f"   ❌ {err}")


# ═══════════════════════════════════════════════════════════════════
# CHECK — Sağlık kontrolü
# ═══════════════════════════════════════════════════════════════════

def check_project():
    """health_check.py scriptini çalıştırır."""
    print("🔍 AgnosticAgent Kurallar Denetimi başlatılıyor...")

    # Önce projenin kendi .agent/scripts/ dizininden dene
    target_dir = os.getcwd()
    local_script = os.path.join(target_dir, ".agent", "scripts", "core", "health_check.py")

    if os.path.exists(local_script):
        subprocess.run([sys.executable, local_script])
        return

    # Fallback: paketin kendi core/ dizininden
    core_dir = get_core_dir()
    health_check_script = os.path.join(core_dir, "core", "health_check.py")

    if os.path.exists(health_check_script):
        subprocess.run([sys.executable, health_check_script])
    else:
        print("❌ Motor core başlatılamadı: health_check.py bulunamadı.")
        print("   Lütfen 'antigravity init' ile kurulum yapın.")


# ═══════════════════════════════════════════════════════════════════
# WATCH — Dosya değişiklik dinleyici
# ═══════════════════════════════════════════════════════════════════

def watch_project():
    """Projedeki dosya değişikliklerini canlı izler."""
    print("👀 AgnosticAgent Gölge Denetçi (Watcher) başlatılıyor...")

    target_dir = os.getcwd()
    local_script = os.path.join(target_dir, ".agent", "scripts", "core", "shadow_watcher.py")
    core_dir = get_core_dir()
    core_script = os.path.join(core_dir, "core", "shadow_watcher.py")

    script = local_script if os.path.exists(local_script) else core_script

    if os.path.exists(script):
        try:
            subprocess.run([sys.executable, script])
        except KeyboardInterrupt:
            print("\n👋 Kapatılıyor...")
    else:
        print("❌ Motor core başlatılamadı: shadow_watcher.py bulunamadı.")


# ═══════════════════════════════════════════════════════════════════
# RUN — Herhangi bir scripti çalıştır
# ═══════════════════════════════════════════════════════════════════

def run_script(script_name, script_args):
    """Motor içindeki belirli bir scripti çalıştırır."""
    target_dir = os.getcwd()
    local_script = os.path.join(target_dir, ".agent", "scripts", "core", script_name)
    core_dir = get_core_dir()
    core_script = os.path.join(core_dir, "core", script_name)

    script = local_script if os.path.exists(local_script) else core_script

    if os.path.exists(script):
        result = subprocess.run([sys.executable, script] + script_args)
        sys.exit(result.returncode)
    else:
        print(f"❌ Motor core scripti bulunamadı: {script_name}")
        sys.exit(1)


# ═══════════════════════════════════════════════════════════════════
# VERSION — Paket versiyonu
# ═══════════════════════════════════════════════════════════════════

def show_version():
    """Mevcut paket versiyonunu gösterir."""
    print(f"AgnosticAgent CLI v{VERSION}")


# ═══════════════════════════════════════════════════════════════════
# MAIN — CLI giriş noktası
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Antigravity CLI — Proaktif Yazılım Geliştirme Asistanı",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  antigravity init      Yeni projede kurulum
  antigravity update    Sistem dosyalarını güncelle
  antigravity check     Sağlık kontrolü
  antigravity version   Versiyon bilgisi
        """
    )
    subparsers = parser.add_subparsers(dest="command", help="Kullanılabilir komutlar")

    subparsers.add_parser("init", help="Mevcut projeye AgnosticAgent'ı kurar (tüm dosyalar: rules, skills, workflows, scripts, config, hooks, docs, contracts)")
    subparsers.add_parser("check", help="Mevcut projenin SSOT, mimari ve teknoloji kurallarına uygunluğunu denetler")
    subparsers.add_parser("update", help="Sistem dosyalarını günceller (.agent/ içi). SSOT ve hafıza dosyaları korunur")
    subparsers.add_parser("watch", help="Projedeki dosya değişikliklerini canlı dinler ve analiz yapar")
    subparsers.add_parser("version", help="Paket versiyonunu gösterir")

    parser_run = subparsers.add_parser("run", help="Motor içindeki belirli bir scripti çalıştırır")
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
    elif args.command == "version":
        show_version()
    elif args.command == "run":
        run_script(args.script_name, args.script_args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
