# 🚀 Agent Prompt System — Kullanım Kılavuzu

> Yapay zeka ajanının (Antigravity / Gemini) yazılım projelerini **profesyonelce** yönetmesini sağlayan prompt altyapısıdır.

---

## Bu Sistem Ne İşe Yarar?

Bu template, her yeni projede ajan-tabanlı geliştirme altyapısını sıfırdan kurmak yerine **hazır bir iskelet** sunar.

**Sağladıkları:**
- ✅ Onaysız kod yazımını engeller (Gatekeeper)
- ✅ Proje hafızasını korur (Memory System)
- ✅ Tutarlı kararlar alınmasını sağlar (SSOT — Single Source of Truth)
- ✅ Otomatik güvenlik / performans / duplicate denetimi (Scripts)
- ✅ Kontrat-bazlı backend ↔ frontend entegrasyonu

**Sağlamadıkları:**
- ❌ Model'in temel yeteneğini değiştirmez
- ❌ %100 hatasız kod garantisi vermez
- ❌ İnsan denetimini ortadan kaldırmaz

---

## ⚡ Hızlı Başlangıç (Kurulum)

### Yöntem 1: NPX ile (Önerilen)

```bash
# Yeni proje oluştur
npx create-agent-system my-project

# Mevcut dizine kur
npx create-agent-system .

# Git olmadan kur
npx create-agent-system my-project --no-git
```

Bu komut otomatik olarak:
- 📦 Template dosyalarını (120+) kopyalar
- � `git init` yapar
- � Pre-commit hook'ları kurar
- � `.gitignore` oluşturur

### Yöntem 2: Git Clone ile

```bash
git clone <repo-url> yeni-projem
cd yeni-projem
bash .agent/hooks/install.sh   # Git hooks kurulumu (opsiyonel)
```

### Kurulum Sonrası

```bash
python3 .agent/scripts/core/health_check.py
```

Beklenen çıktı: `Health Score: 100/100`

### 4. Projeyi Başlat

```
/start
```

Bu komut sana sorular sorar ve cevaplarını şu dosyalara yazar:

| Şablon (Okunur) | Çıktı (Yazılır) |
|-----------------|-----------------|
| `docs/templates/project_brief_template.md` | `docs/project_brief.md` |
| `docs/templates/tech_stack_template.md` | `docs/tech_stack.md` |
| `docs/templates/design_brief_template.md` | `docs/design_brief.md` |
| `docs/templates/data_privacy_template.md` | `docs/data_privacy.md` |

> ⚠️ `docs/tech_stack.md` ve `docs/architecture.md` şu an **örnek veriyle** dolu.
> `/start` komutu bu dosyaları projenize özel içerikle üzerine yazar.

---

## 🔄 Proje Yaşam Döngüsü

```
1. FİKİR       →  /ultrathink
2. KARAR       →  docs/tech_stack.md + docs/architecture.md
3. PLANLAMA    →  /plan veya /start
4. GELİŞTİRME →  Normal kodlama + Gatekeeper onayı
5. KONTROL     →  /security_audit, /db_audit
6. HATA        →  /deep_bug_hunt, /think
7. STABİL      →  Checkpoint + Memory update
```

---

## 📋 Tüm Slash Komutları

### Temel Komutlar

| Komut | Ne Yapar | Ne Zaman Kullanılır |
|-------|----------|-------------------|
| `/start` | Yeni proje başlatır (röportaj → SSOT dosyaları) | **Projenin ilk günü** |
| `/plan` | Karmaşık görev için detaylı plan oluşturur | Çok adımlı feature'lar |
| `/think` | Görevi derinlemesine analiz eder | Belirsiz veya riskli durumlar |
| `/ultrathink` | Enterprise-grade proje analizi | Kritik mimari kararlar |

### Geliştirme Komutları

| Komut | Ne Yapar | Ne Zaman Kullanılır |
|-------|----------|-------------------|
| `/new-feature` | CRUD + endpoint + UI tam akış | Büyük feature geliştirme |
| `/contract-update` | Mevcut API kontratını günceller | Backend/Frontend değişikliği |
| `/breaking-change` | Breaking change yönetimi + migration | API versiyonlama |

### Denetim Komutları

| Komut | Ne Yapar | Ne Zaman Kullanılır |
|-------|----------|-------------------|
| `/security_audit` | Güvenlik açığı taraması | Release öncesi |
| `/db_audit` | Database model/index/query denetimi | DB değişikliği sonrası |
| `/architecture_check` | Mimari bütünlük denetimi | Büyük refactor öncesi |
| `/scalability_check` | Ölçeklenebilirlik analizi | Trafik artışı öncesi |
| `/deep_bug_hunt` | Hata kök neden analizi | Zor bug'lar |
| `/analyze_override` | Ezilen (etkisiz) kodun analizi | Gizli override sorunları |

---

## 🏗️ SSOT (Single Source of Truth) Sistemi

Proje boyunca agent bu dosyalara bakarak karar verir. **Çelişki durumunda öncelik sırası:**

| Öncelik | Dosya | İçerik |
|---------|-------|--------|
| 1 | `docs/tech_stack.md` | Teknoloji seçimleri (framework, DB, cache) |
| 2 | `docs/architecture.md` | Mimari kararlar (multi-tenancy, payment, vb.) |
| 3 | `docs/prd.md` | Ürün gereksinimleri |
| 4 | `docs/memory.md` | Proje hafızası ve geçmiş kararlar |

### SSOT Tutarlılık Kontrolü

```bash
python3 .agent/scripts/core/ssot_validator.py validate
```

Beklenen çıktı: `Score: 100/100`

---

## 🛡️ Gatekeeper (Onay Mekanizması)

Agent her **yazma** işleminden önce kullanıcı onayı bekler.

**Onay kelimeleri:** `evet`, `yap`, `onay`, `devam`, `tamam`, `ok`, `approved`, `yes`, `proceed`

**Gatekeeper bypass:**
- Workflow dosyalarında `// turbo` annotasyonu olan adımlar otomatik çalışır
- `// turbo-all` annotasyonu tüm adımları otomatik çalıştırır

> ❌ Onaysız dosya yazma, DB migration, deployment **asla** otomatik yapılmaz.

---

## 🔧 Python Script'leri

### Sağlık ve Doğrulama

```bash
# Sistem sağlık kontrolü
python3 .agent/scripts/core/health_check.py

# SSOT tutarlılık kontrolü
python3 .agent/scripts/core/ssot_validator.py validate

# Dosya referans doğrulama
python3 .agent/scripts/validate_agent_links.py

# Duplicate kod taraması
python3 .agent/scripts/core/duplicate_detector.py
```

### Hafıza ve İlerleme

```bash
# Mevcut durum özeti
python3 .agent/scripts/core/memory_controller.py summary

# Checkpoint kaydetme
python3 .agent/scripts/core/memory_controller.py checkpoint "Feature X completed"

# Sapma tespiti
python3 .agent/scripts/core/drift_detector.py status
```

### Otomasyon

```bash
# Yeni API kontratı oluşturma (registry.json otomatik güncellenir)
python3 .agent/scripts/auto/gen_contract.py \
  --operation create_user \
  --domain user \
  --entity profile \
  --fields name:string,email:string

# Rapor oluşturma (docs/reports/ dizinine yazılır)
python3 .agent/scripts/auto/gen_report.py --type feature --name "Login Refactor"
```

### Güvenlik ve Config

```bash
# Gizli bilgi taraması
python3 .agent/skills/enterprise-security/scripts/secret_scanner.py

# Komut izin kontrolü
python3 .agent/scripts/core/config_enforcer.py check_command "rm -rf /"

# Dosya yazma izin kontrolü
python3 .agent/scripts/core/config_enforcer.py check_write "docs/tech_stack.md"

# Gatekeeper durumu
python3 .agent/scripts/core/gatekeeper_check.py status
```

---

## 📁 Klasör Yapısı

```
.agent/
├── config/
│   └── rules.yaml           # TEK KAYNAK — tüm kurallar + policy'ler
├── rules/
│   ├── SYSTEM.md             # En üst otorite
│   ├── gatekeeper.md         # Onay kuralları
│   ├── project_context.md    # Proje bağlamı + görev referans tablosu
│   ├── contract-standards.md # Kontrat standartları
│   ├── error-handling.md     # Hata format standartları
│   └── integration-checklist.md
├── workflows/                # /start, /plan, /think, /ultrathink, vb.
├── skills/                   # 11 uzmanlık modülü
│   ├── code-review/
│   ├── component-architecture/
│   ├── database-architecture/
│   ├── debugging/
│   ├── enterprise-security/
│   ├── fullstack-integration/
│   ├── localization/
│   ├── multi-tenancy/
│   ├── payment-systems/
│   ├── performance/
│   └── tdd-workflow/
├── scripts/
│   ├── core/                 # health_check, ssot_validator, drift_detector, vb.
│   └── auto/                 # gen_contract, gen_report
├── hooks/
│   ├── pre-commit            # Git commit öncesi otomatik kontroller
│   └── install.sh            # Hook kurulum scripti
├── state/                    # Hafıza (progress.json, snapshots)
├── logs/                     # Audit trail (actions.jsonl, reasoning.jsonl)
└── templates/reports/        # Rapor şablonları

docs/
├── templates/                # Boş şablonlar (her projede aynı kalır)
│   ├── project_brief_template.md
│   ├── tech_stack_template.md
│   ├── design_brief_template.md
│   ├── data_privacy_template.md
│   ├── roadmap_template.md
│   └── component_config_template.md
├── tech_stack.md             # SSOT #1 — Teknoloji kararları
├── architecture.md           # SSOT #2 — Mimari kararlar
├── prd.md                    # SSOT #3 — Ürün gereksinimleri
├── memory.md                 # Proje hafızası
├── registry.md               # Component/API kayıt defteri
└── decision_log.md           # Karar gerekçeleri

contracts/
├── registry.json             # Kontrat merkezi indeksi
└── [domain]/[entity]/v[X]/   # Kontrat dosyaları
```

---

## 🎓 Skill Sistemi

Agent, bağlama göre ilgili skill'i otomatik yükler:

| Skill | Tetikleyici Anahtar Kelimeler |
|-------|-------------------------------|
| `database-architecture` | tablo, migration, index, query, N+1 |
| `performance` | cache, redis, slow query, memory leak |
| `enterprise-security` | RBAC, audit log, encryption, GDPR |
| `fullstack-integration` | API, endpoint, form, modal, contract |
| `component-architecture` | component, modal, kart, form, DRY |
| `debugging` | bug, hata, error, exception, trace |
| `code-review` | code review, PR review, kalite kontrol |
| `multi-tenancy` | tenant, multi-tenant, saas, izolasyon |
| `payment-systems` | payment, ödeme, transaction, webhook |
| `localization` | i18n, çeviri, multi-language, RTL |
| `tdd-workflow` | TDD, unit test, test coverage |

---

## ⚠️ En Sık Yapılan Hatalar

1. **Onay vermeden bekleme** — Agent onay bekler, siz susarsınız → ilerleme durur
2. **Her şeyi `/ultrathink`'e sorma** — Basit işler için `/think` yeterli
3. **Memory kullanmama** — Uzun oturumda bağlam kaybı → `checkpoint` kaydedin
4. **SSOT dosyalarını güncellememe** — Tutarsızlık → `ssot_validator` hata verir
5. **Template dosyalarını silme** — `docs/templates/` her projede lazım, sadece `docs/*.md` yazılır

---

## 🔑 Altın Kurallar

1. **Onaysız yazma yasak** — Gatekeeper her zaman aktif
2. **SSOT hiyerarşisi** — `tech_stack > architecture > prd`
3. **Kontrat önce** — Backend/Frontend kodu yazmadan önce kontrat tanımla
4. **Memory kaydet** — Önemli adımlarda `checkpoint`
5. **Şüphe duy** — Agent'ın çıktısını doğrula
6. **Basit tut** — Her şeyi workflow'a sokma
