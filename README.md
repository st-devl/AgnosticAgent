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

### Adım 1: Global Motoru Kurma (Bir Kez Yapılır)

Öncelikle Antigravity motorunu terminalinize global bir CLI aracı (Python paketi) olarak kurmalısınız:

```bash
pip3 install "git+https://github.com/st-devl/AgnosticAgent.git#subdirectory=AgnosticAgent" --upgrade
```
*Bu komut, `antigravity-agent` paketini ve `antigravity` komutunu sisteminize global olarak kurar. Artık terminalinizde herhangi bir dizindeyken `antigravity` komutunu çalıştırabilirsiniz.*

**💡 Geliştirici / Agent Notu:**
> Kurulan bu yapı bir "şablon" veya "iskelet" değil; `setup.py` dosyasına sahip, çalıştırılabilir bir **Python Package / CLI Aracıdır**. Sistemi güncellemek istediğinizde repoyu klonlamak yerine sadece `pip install ... --upgrade` yapmanız gerekir.

### Adım 2: Projeyi Agent'a Bağlama (Her Projede)

Yeni veya var olan bir projenizin dizinine gidin ve Agent'ı o proje için başlatın (yakıtları oluşturun):
```bash
cd yeni-projem
antigravity init
```

Bu komut projenizde otomatik olarak:
- 📦 Ajana özel (size ait) `docs/` şablonlarını kopyalar (Eğer yoksa)
- 🪝 `.git/hooks/pre-commit` hook'larını kurup, global motordaki validatorleri buraya bağlar.

### Adım 3: Sistemi Güncelleme (Yeni Özellikler Geldiğinde)

Eğer AgnosticAgent reposuna yeni özellikler eklenirse (eski projelerinizi yeni versiyona yükseltmek veya global motoru güncellemek için):

1. **Global Motoru Güncelle:**
   ```bash
   pip3 install "git+https://github.com/st-devl/AgnosticAgent.git#subdirectory=AgnosticAgent" --upgrade
   ```

2. **Proje Altyapısını Güncelle:**
   Proje dizininde (daha önce `init` yapılmış klasörde) şu komutu çalıştırın:
   ```bash
   antigravity update
   ```
   > 🛡️ **GÜVENLİ GÜNCELLEME STRATEJİSİ:** Bu komut `.agent/` altındaki sistem dosyalarını yenilerken, sizin `docs/` altındaki SSOT dosyalarınıza ve projenin gelişim hafızasına (memory) **ASLA dokunmaz/ezmez**. Sadece motor güncellenir.

### Kurulum Sonrası Test

```bash
antigravity check
```

Beklenen çıktı: `Health Score: 100/100`

---

## 🚀 Projeyi İlk Kez Başlatmak (Otonom Planlama ve İnşa)

Kurulumu sorunsuz tamamladıktan sonra projenizin temelini zekice ve vakit kaybetmeden atmak için şu iki komutu sırayla kullanmalısınız:

### Adım 1: Projenin Beynini Oluşturma (Otonom Planlama)

```bash
/temel
```

> 🎯 **BU KOMUTUN AMACI:** Projenin başında sizi karmaşık mimari dosyalar oluşturmaktan kurtarmak ve sizin yerinize Ajan'ın (benim) projeyi planlamasını sağlamaktır.

**Ne Zaman ve Nasıl Kullanılır?**
1. Projeyi başlattıktan sonra (`antigravity init` sonrasında), doğrudan `docs/prd.md` (Product Requirements Document) dosyasını açın.
2. Bu dosya sizin tuvalinizdir. Oraya yapmak istediğiniz projeyi, aklınızdaki özellikleri, kullanmak istediğiniz (veya benim seçmemi istediğiniz) teknolojileri, tasarım hissini ve tüm beklentilerinizi **insan dilinde** yazın ve kaydedin.
3. Ardından sohbete dönüp `/temel` komutunu yazın. 

**Nasıl Çalışır?**
Ben (Ajan) sizin yazdığınız o `prd.md` dosyasını baştan aşağı okurum. Kendimi "Baş Mühendis" rolüne sokarım ve projenin ihtiyaç duyduğu tüm teknik belgeleri sizin yerinize **otonom olarak doldururum**. Şunları sizin için hazırlarım:

| Kaynak (Sizin Yazdığınız) | Çıktı (Benim Otonom Hazırladıklarım) |
|-----------------|-----------------|
| `docs/prd.md` | `docs/tech_stack.md` (Kullanılacak diller, framework'ler, DB) |
| `docs/prd.md` | `docs/architecture.md` (Klasör yapıları, katmanlar) |
| `docs/prd.md` | `docs/project_brief.md` (Hedef kitle, MVP özellikleri) |
| `docs/prd.md` | `docs/design_brief.md` (Arayüz hissi, UI prensipleri) |
| `docs/prd.md` | `docs/data_privacy.md` (Güvenlik gereksinimleri) |
| `docs/prd.md` | `docs/secret_policy.md` (Credential yönetim kuralları) |

*Özetle: Siz sadece vizyonunuzu anlattınız, ben projenin teknik anayasasını yazdım.*

---

### Adım 2: Projenin Fiziksel İnşası (Otonom Kurulum)

```bash
/start
```

> 🎯 **BU KOMUTUN AMACI:** Sadece kağıt üstünde planlanan mimariyi, terminali kullanarak gerçekten **bilgisayarınıza kurmaktır**.

**Ne Zaman ve Nasıl Kullanılır?**
1. `/temel` komutu çalışıp belgeleriniz (özellikle `tech_stack.md` ve `architecture.md`) benim tarafımdan doldurulduktan sonra çalıştırılır. Seçtiğim teknolojileri inceleyip onayladıysanız bu komutu girebilirsiniz.

**Nasıl Çalışır?**
1. Ben `tech_stack.md` dosyasını okurum (Örn: "React, Vite, Tailwind kullanılacak" yazıyorsa).
2. Terminalinizde `npm create vite@latest...` gibi projenin iskeletini ayağa kaldıracak gerekli bilgisayar komutlarını belirlerim.
3. İndirmem gereken paketleri (npm, pip3 vb.) hesaplarım.
4. Terminalde çalıştıracağım komutların listesini size gösteririm ve **Gatekeeper (Güvenlik Onayınız)** onayını isterim.
5. "Evet" dediğiniz an, tüm klasörleri açar, iskeleti kurar, gereksinimleri indirir ve kod yazmaya hazır fiziksel bir proje teslim ederim.
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
| `/temel` | `prd.md`'yi okuyup TÜM projenin mimari belgelerini otonom doldurur | **PRD yazıldıktan hemen sonra** |
| `/start` | Mimari belgelere göre paketi, framework'ü ve fiziki yapıyı kurar | **Belgeler dolduktan sonra** |
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
