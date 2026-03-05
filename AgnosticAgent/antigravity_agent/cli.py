import os
import shutil
import argparse
import sys
import subprocess


VERSION = "2.0.1"


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
            except shutil.SameFileError:
                print("✅ .git/hooks/pre-commit hook'u zaten kurulu (aynı dosya)")
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
        try:
            shutil.copy2(hook_src, hook_dst)
            os.chmod(hook_dst, 0o755)
            print("  ✅ .git/hooks/pre-commit güncellendi")
        except shutil.SameFileError:
            print("  ✅ .git/hooks/pre-commit güncel (aynı dosya)")
        except Exception as e:
            errors.append(f"Git hook güncelleme hatası: {e}")

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
# CHECK — Kapsamlı sistem doğrulama
# ═══════════════════════════════════════════════════════════════════

# Kontrol kategorileri ve hangi template dizinine karşılık geldiği
# (kategori_adı, template_alt_dizin, proje_hedef_yol, açıklama)
CHECK_CATEGORIES = [
    {
        "name": "Ana Dizin Yapısı",
        "icon": "📁",
        "items": [
            {"template_base": "agent", "project_path": ".agent", "type": "dir"},
            {"template_base": "docs",  "project_path": "docs",   "type": "dir"},
            {"template_base": "contracts", "project_path": "contracts", "type": "dir"},
        ],
    },
]

# SSOT dosyaları — init ile oluşturulur, update ile ezilmez
SSOT_DOC_FILES = [
    "tech_stack.md", "architecture.md", "prd.md", "memory.md",
    "registry.md", "decision_log.md", "project_brief.md",
    "design_brief.md", "data_privacy.md", "secret_policy.md",
    "project_keys.md",
]

# İgnore edilecek dosya desenleri (kontrol dışı)
CHECK_IGNORE = {".DS_Store", "__pycache__", ".pyc", ".gitkeep", ".git"}


def _scan_template_files(template_base_dir, prefix=""):
    """
    Template dizinini tarayarak beklenen dosya/dizin listesini döner.
    Returns: list of (relative_path, type) tuples
    """
    items = []
    if not os.path.exists(template_base_dir):
        return items

    for entry in sorted(os.listdir(template_base_dir)):
        if entry in CHECK_IGNORE or entry.endswith(".pyc"):
            continue
        full = os.path.join(template_base_dir, entry)
        rel = os.path.join(prefix, entry) if prefix else entry

        if os.path.isdir(full):
            items.append((rel, "dir"))
            items.extend(_scan_template_files(full, rel))
        else:
            items.append((rel, "file"))

    return items


def _classify_path(rel_path):
    """Bir dosya yolunun hangi kontrol kategorisine ait olduğunu belirler."""
    parts = rel_path.split(os.sep)

    if len(parts) >= 2 and parts[0] == ".agent":
        second = parts[1]
        category_map = {
            "rules": ("📜", "Kural Dosyaları"),
            "config": ("⚙️", "Konfigürasyon"),
            "scripts": ("🐍", "Script Dosyaları"),
            "skills": ("🎓", "Skill Dosyaları"),
            "workflows": ("🔄", "Workflow Dosyaları"),
            "hooks": ("🪝", "Git Hook Kaynakları"),
            "templates": ("📋", "Agent Şablonları"),
            "state": ("💾", "Durum Dizinleri"),
            "logs": ("📝", "Log Dizinleri"),
            "cache": ("🗄️", "Cache Dizinleri"),
            "backups": ("💼", "Backup Dizinleri"),
            "docs": ("📄", "Agent Docs"),
        }
        if second in category_map:
            return category_map[second]
        return ("📁", "Sistem Dizinleri (.agent/)")

    if parts[0] == "docs":
        if len(parts) >= 2 and parts[1] == "templates":
            return ("📝", "Doküman Şablonları (docs/templates/)")
        if len(parts) >= 2 and parts[1] == "reports":
            return ("📊", "Rapor Dizini (docs/reports/)")
        return ("📚", "SSOT & Dokümanlar")

    if parts[0] == "contracts":
        return ("📑", "Contract Dosyaları")

    return ("📁", "Diğer")


def _fix_command_for(rel_path):
    """Eksik dosya/dizin için uygun düzeltme komutunu döner."""
    # Ana dizinler eksikse → init
    if rel_path in (".agent", "docs", "contracts"):
        return "antigravity init"

    parts = rel_path.split(os.sep)

    # .agent/ altındaki sistem klasörleri → update ile gelir
    if parts[0] == ".agent" and len(parts) >= 2:
        second = parts[1]
        if second in SYSTEM_FOLDERS:
            return "antigravity update"
        # state/logs/cache/backups → update ile oluşturulur
        if second in PRESERVED_FOLDERS:
            return "antigravity update"
        return "antigravity update"

    # docs/ SSOT dosyaları
    if parts[0] == "docs":
        if len(parts) == 2 and parts[1] in SSOT_DOC_FILES:
            return "antigravity init"
        return "antigravity update"

    # contracts/
    if parts[0] == "contracts":
        return "antigravity init"

    return "antigravity init"


def check_project():
    """
    Projenin tüm dosya/dizin yapısını A'dan Z'ye kontrol eder.
    Template dizininden beklenen dosya listesini dinamik olarak okur,
    proje diziniyle karşılaştırır, eksikleri kategorize eder ve
    düzeltme komutu önerir.
    """
    print(f"🔍 AgnosticAgent v{VERSION} — Kapsamlı Sistem Kontrolü")
    print("═" * 55)

    templates_dir = get_templates_dir()
    target_dir = os.getcwd()

    # Template doğrulama
    if not os.path.exists(templates_dir):
        print("❌ HATA: Paket template dosyaları bulunamadı!")
        print("   Lütfen paketi yeniden kurun:")
        print("   pip3 install git+https://github.com/st-devl/AgnosticAgent.git --upgrade --force-reinstall")
        sys.exit(1)

    # ── Beklenen dosya/dizin listesini template'ten oluştur ──
    expected_items = []

    # 1) .agent/ (template/agent → .agent)
    agent_template = os.path.join(templates_dir, "agent")
    if os.path.exists(agent_template):
        expected_items.append((".agent", "dir"))
        for rel, typ in _scan_template_files(agent_template):
            expected_items.append((os.path.join(".agent", rel), typ))

    # 2) docs/ (template/docs → docs)
    docs_template = os.path.join(templates_dir, "docs")
    if os.path.exists(docs_template):
        expected_items.append(("docs", "dir"))
        for rel, typ in _scan_template_files(docs_template):
            expected_items.append((os.path.join("docs", rel), typ))

    # 3) contracts/ (template/contracts → contracts)
    contracts_template = os.path.join(templates_dir, "contracts")
    if os.path.exists(contracts_template):
        expected_items.append(("contracts", "dir"))
        for rel, typ in _scan_template_files(contracts_template):
            expected_items.append((os.path.join("contracts", rel), typ))

    # ── Proje diziniyle karşılaştır ──
    found = []
    missing = []
    warnings = []

    for rel_path, item_type in expected_items:
        full_path = os.path.join(target_dir, rel_path)
        exists = os.path.exists(full_path)

        if exists:
            if item_type == "file" and os.path.getsize(full_path) == 0:
                # Boş dosya uyarısı (ama .gitkeep zaten ignore ediliyor)
                warnings.append((rel_path, "Dosya boş"))
            found.append(rel_path)
        else:
            missing.append(rel_path)

    # ── Git hook kontrolü (ayrı) ──
    git_hook_ok = False
    git_dir = os.path.join(target_dir, ".git")
    if os.path.exists(git_dir):
        pre_commit = os.path.join(git_dir, "hooks", "pre-commit")
        if os.path.exists(pre_commit):
            found.append(".git/hooks/pre-commit")
            git_hook_ok = True
        else:
            missing.append(".git/hooks/pre-commit")

    # ── Sonuçları kategorize ederek yazdır ──
    printed_categories = set()

    # Önce bulunanları kategorize et
    all_items_by_category = {}
    for rel_path in found:
        icon, cat = _classify_path(rel_path)
        key = (icon, cat)
        if key not in all_items_by_category:
            all_items_by_category[key] = {"found": [], "missing": []}
        all_items_by_category[key]["found"].append(rel_path)

    for rel_path in missing:
        icon, cat = _classify_path(rel_path)
        key = (icon, cat)
        if key not in all_items_by_category:
            all_items_by_category[key] = {"found": [], "missing": []}
        all_items_by_category[key]["missing"].append(rel_path)

    # Kategorileri sırayla yazdır
    category_order = [
        ("📁", "Ana Dizin Yapısı"),
        ("📁", "Sistem Dizinleri (.agent/)"),
        ("⚙️", "Konfigürasyon"),
        ("📜", "Kural Dosyaları"),
        ("🐍", "Script Dosyaları"),
        ("🎓", "Skill Dosyaları"),
        ("🔄", "Workflow Dosyaları"),
        ("🪝", "Git Hook Kaynakları"),
        ("📋", "Agent Şablonları"),
        ("💾", "Durum Dizinleri"),
        ("📝", "Log Dizinleri"),
        ("🗄️", "Cache Dizinleri"),
        ("💼", "Backup Dizinleri"),
        ("📄", "Agent Docs"),
        ("📚", "SSOT & Dokümanlar"),
        ("📝", "Doküman Şablonları (docs/templates/)"),
        ("📊", "Rapor Dizini (docs/reports/)"),
        ("📑", "Contract Dosyaları"),
    ]

    # Ana dizin yapısını özel olarak göster
    print(f"\n📁 Ana Dizin Yapısı")
    for base_dir in [".agent", "docs", "contracts"]:
        full = os.path.join(target_dir, base_dir)
        if os.path.exists(full):
            print(f"  ✅ {base_dir}/")
        else:
            cmd = _fix_command_for(base_dir)
            print(f"  ❌ {base_dir}/{'':>30s} → {cmd}")

    # Diğer kategorileri göster
    for icon, cat_name in category_order:
        key = (icon, cat_name)
        if key not in all_items_by_category:
            continue
        if cat_name == "Ana Dizin Yapısı":
            continue  # Zaten yukarıda gösterdik

        data = all_items_by_category[key]
        found_count = len(data["found"])
        missing_count = len(data["missing"])
        total = found_count + missing_count

        if total == 0:
            continue

        if missing_count == 0:
            print(f"\n{icon} {cat_name} ({found_count}/{total})")
            print(f"  ✅ Tümü mevcut")
        else:
            print(f"\n{icon} {cat_name} ({found_count}/{total})")
            # Sadece eksikleri detaylı göster
            for m in data["missing"]:
                cmd = _fix_command_for(m)
                # Kısa yol göster
                display_path = m
                print(f"  ❌ {display_path:<45s} → {cmd}")
            if found_count > 0:
                print(f"  ✅ {found_count} dosya/dizin mevcut")

    # Git hook özel satırı
    if os.path.exists(git_dir):
        print(f"\n🪝 Git Hook'ları (.git/hooks/)")
        if git_hook_ok:
            print(f"  ✅ pre-commit hook kurulu")
        else:
            print(f"  ❌ pre-commit hook eksik{'':>20s} → antigravity update")
    else:
        print(f"\n🪝 Git Hook'ları")
        print(f"  ⚠️  Bu dizin bir git reposu değil (git hook kontrolü atlandı)")

    # Uyarılar
    if warnings:
        print(f"\n⚠️  Uyarılar")
        for path, msg in warnings:
            print(f"  ⚠️  {path}: {msg}")

    # ── Sağlık skoru ve özet ──
    total_expected = len(expected_items)
    total_found = len(found)
    total_missing = len(missing)
    score = int((total_found / total_expected) * 100) if total_expected > 0 else 0

    print(f"\n{'═' * 55}")
    print(f"📊 Sistem Sağlık Skoru: {score}/100")
    print()
    print(f"   ✅ Mevcut:  {total_found} dosya/dizin")
    print(f"   ❌ Eksik:   {total_missing} dosya/dizin")
    if warnings:
        print(f"   ⚠️  Uyarı:   {len(warnings)}")

    if total_missing == 0 and not warnings:
        print(f"\n🎉 Sistem 100% sağlıklı! Tüm dosyalar eksiksiz.")
    elif total_missing > 0 or warnings:
        print(f"\n🔧 Düzeltme Önerileri:")
        idx = 1
        
        # Eksik dosyalar için komut önerileri
        if total_missing > 0:
            fix_commands = {}
            for m in missing:
                cmd = _fix_command_for(m)
                if cmd not in fix_commands:
                    fix_commands[cmd] = 0
                fix_commands[cmd] += 1

            for cmd, count in fix_commands.items():
                print(f"   {idx}. {cmd:<25s} → {count} eksik dosyayı geri yükler")
                idx += 1
                
        # Boş dosyalar için öneriler
        empty_files = [w[0] for w in warnings if w[1] == "Dosya boş"]
        if empty_files:
            empty_docs = [f for f in empty_files if f.startswith("docs/")]
            if empty_docs:
                print(f"   {idx}. {'/start':<25s} → Boş dokümanları ({len(empty_docs)} adet) doldurmak için proje röportajını başlatır")
                idx += 1
            print(f"   {idx}. {'(Manuel Düzenleme)':<25s} → Boş dosyalara gerekli içeriği manuel olarak ekleyin")
            idx += 1


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
