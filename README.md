# 🚀 Agent Prompt System - Kullanım Kılavuzu

## Bu Sistem Ne İşe Yarar?

Yapay zeka ajanının (Antigravity) yazılım projelerini **profesyonelce** yönetmesini sağlayan bir prompt altyapısıdır.

**Sağladıkları:**
- ✅ Onaysız kod yazımını engeller (Gatekeeper)
- ✅ Proje hafızasını korur (Memory System)
- ✅ Tutarlı kararlar alınmasını sağlar (SSOT)
- ✅ Otomatik güvenlik/performans denetimi (Scripts)

**Sağlamadıkları:**
- ❌ Model'in temel yeteneğini değiştirmez
- ❌ %100 hatasız kod garantisi vermez
- ❌ İnsan denetimini ortadan kaldırmaz

---

## � Proje Yaşam Döngüsü

```
1. FİKİR      → /ultrathink
2. KARAR      → docs/tech_stack.md, docs/architecture.md
3. PLANLAMA   → /plan veya /start
4. GELİŞTİRME → Normal kodlama + Gatekeeper onayı
5. KONTROL    → /security_audit, /db_audit
6. HATA       → /deep_bug_hunt, /think
7. STABİL     → Checkpoint + Memory update
```

---

## 1️⃣ PROJE FİKRİ AŞAMASI

### Hangi Komut?
```
/ultrathink
```

### Ne Yapar?
- Fikri acımasızca sorgular
- Teknik uygulanabilirlik analizi
- Over/under-engineering tespiti
- Risk ve fırsat belirleme

### Bu Aşamada Alınması Gereken Çıktılar:
- [ ] Proje fizibilitesi (Evet/Hayır/Şartlı)
- [ ] Kritik riskler listesi
- [ ] Önerilen mimari yaklaşım
- [ ] Teknoloji önerileri

### ⚠️ Guardrail:
Agent bu aşamada **kod yazmaz**, sadece analiz eder.

---

## 2️⃣ MİMARİ & TEKNOLOJİ KARARLARI

### SSOT Dosyaları (Tek Kaynak):
| Dosya | İçerik | Öncelik |
|-------|--------|---------|
| `docs/tech_stack.md` | Teknoloji seçimleri | 1 (En yüksek) |
| `docs/architecture.md` | Mimari kararlar | 2 |
| `docs/prd.md` | Ürün gereksinimleri | 3 |

### Agent Nasıl Uyum Sağlar?
- Her write işleminde SSOT kontrol edilir
- Çelişki varsa `ssot_validator.py` uyarır
- `decision_log.md`'ye karar gerekçeleri yazılır

### Yanlış Teknoloji Seçimini Yakalama:
```
/ultrathink "seçilen teknoloji stack'ini denetle"
```

---

## 3️⃣ YOL HARİTASI & İLERLEME TAKİBİ

### Yol Haritası Oluşturma:
```
/start   → Yeni proje başlatma (röportaj + roadmap)
/plan    → Karmaşık görev planlama
```

### İlerleme Takibi:
```bash
# Manuel kontrol
python3 .agent/scripts/core/memory_controller.py summary

# Checkpoint kaydetme
python3 .agent/scripts/core/memory_controller.py checkpoint "Feature X completed"
```

### Otomatik vs Manuel:
| İş | Otomatik | Manuel |
|-----|----------|--------|
| İlerleme kaydetme | ❌ | ✅ |
| Checkpoint | ❌ | ✅ |
| Sapma tespiti | ⚠️ Uyarır | İnsan karar verir |

---

## 4️⃣ HATA ALDIĞIMDA

### İlk Refleks:
1. **Hemen kod yazdırma** - Analiz iste
2. **Kök neden sor** - "Neden bu hata oluştu?"
3. **Alternatif iste** - "Başka çözüm var mı?"

### Hangi Workflow?
| Hata Tipi | Workflow |
|-----------|----------|
| Kod hatası (bug) | `/deep_bug_hunt` |
| Mimari çelişki | `/think` + SSOT kontrol |
| Performans | `/scalability_check` |
| Güvenlik | `/security_audit` |

### Agent'ın Yamamasını Engelleme:
```
"Mimariyi incele, sadece yama yapma. 
Kök neden analizi yap ve 3 alternatif sun."
```

### Ne Zaman Durup Gözden Geçirmeli?
- Aynı hata 3+ kez tekrarladığında
- Çözüm giderek karmaşıklaştığında
- Agent çelişkili öneriler sunduğunda

---

## 5️⃣ MANUEL TETİKLENEN ÖZELLİKLER

| Komut | Ne Zaman | Zorunlu mu? |
|-------|----------|-------------|
| `/ultrathink` | Proje başı, kritik kararlar | ⭐ Önerilir |
| `/start` | Yeni proje | ⭐ Önerilir |
| `/plan` | Karmaşık görev | ⭐ Önerilir |
| `/think` | Belirsiz durum | İsteğe bağlı |
| `/security_audit` | Release öncesi | ⭐ Önerilir |
| `/db_audit` | DB değişikliği sonrası | ⭐ Önerilir |
| `/deep_bug_hunt` | Zor bug | İsteğe bağlı |

### Yanlış Zamanda Tetikleme Riskleri:
- `/security_audit` → Erken aşamada gereksiz
- `/ultrathink` → Basit iş için overkill
- `/start` → Mevcut projede konfüzyon

---

## 6️⃣ OTOMATİK ÖZELLİKLER

### Otomatik Çalışmalı:
| Kontrol | Araç | Ne Zaman |
|---------|------|----------|
| Link integrity | `validate_agent_links.py` | PR öncesi |
| System health | `health_check.py` | Günlük |
| Secret scan | `secret_scanner.py --dry-run` | Her commit |

### Asla Otomatik Olmamalı:
- ❌ Dosya yazma
- ❌ Database migration
- ❌ Deployment
- ❌ Config değişikliği

### "Kontrol Et, Yazma" Prensibi:
```
Agent → Analiz eder → Rapor sunar → İNSAN ONAYLAR → Agent yazar
```

---

## 7️⃣ BAŞTAN SONA KULLANIM AKIŞI

### Adım 1: Başlangıç
```
/ultrathink "proje fikrini analiz et"
```
✅ Çıktı: Fizibilite raporu, risk analizi

### Adım 2: Karar Alma
- Agent önerilerini değerlendir
- `docs/tech_stack.md` oluştur (insan onayıyla)
- `docs/architecture.md` oluştur (insan onayıyla)

### Adım 3: Planlama
```
/start  (yeni proje ise)
/plan   (karmaşık görev ise)
```
✅ Çıktı: Roadmap, task listesi

### Adım 4: Geliştirme
- Normal kodlama
- Her write → Gatekeeper onayı bekler
- Memory checkpoint'leri

### Adım 5: Kontrol
```
python3 .agent/scripts/core/health_check.py
/security_audit (release öncesi)
/db_audit (DB değişikliği sonrası)
```

### Adım 6: Hata Yönetimi
```
/deep_bug_hunt "hata detayı"
/think "karmaşık problem"
```

### Adım 7: Stabilizasyon
```bash
python3 .agent/scripts/core/memory_controller.py checkpoint "v1.0 stable"
```

---

## ⚠️ EN SIK YAPILAN HATALAR

1. **Onay vermeden bekleme** - Agent onay bekler, siz susarsınız
2. **Her şeyi /ultrathink'e sorma** - Basit işler için overkill
3. **Memory kullanmama** - Proje kapandığında bağlam kaybı
4. **SSOT dosyalarını güncellememe** - Tutarsızlık
5. **Dry-run kullanmama** - Direkt yazma hataları

---

## � SİSTEMİN SINIRLARI

| Yapabilir ✅ | Yapamaz ❌ |
|--------------|-----------|
| Kod analizi | Mükemmel kod garantisi |
| Güvenlik taraması | %100 güvenlik |
| Mimari öneri | Otomatik mimari değişiklik |
| Hafıza tutma | Sonsuz bağlam |
| Onay mekanizması | İnsan yerine karar verme |

---

## 📁 Klasör Yapısı

```
.agent/
├── config/rules.yaml    # Tüm kurallar (machine-readable)
├── rules/               # Otorite dosyaları
│   ├── SYSTEM.md        # En üst otorite
│   └── gatekeeper.md    # Onay kuralları
├── workflows/           # Slash komutları
├── skills/              # Uzmanlık modülleri
├── scripts/core/        # Python otomasyonları
├── state/               # Hafıza (JSON)
└── logs/                # Audit trail

docs/
├── tech_stack.md        # SSOT #1
├── architecture.md      # SSOT #2
├── decision_log.md      # Karar kayıtları
└── memory.md            # Proje hafızası
```

---

## 🔑 Altın Kurallar

1. **Onaysız yazma yasak** - Gatekeeper her zaman aktif
2. **SSOT hiyerarşisi** - tech_stack > architecture > prd
3. **Memory kaydet** - Önemli adımlarda checkpoint
4. **Şüphe duy** - Agent'ın çıktısını doğrula
5. **Basit tut** - Her şeyi workflow'a sokma
