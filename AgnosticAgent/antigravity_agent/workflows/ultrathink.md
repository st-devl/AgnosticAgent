---
description: ultrathink v1.6 - Enterprise-grade proje analizi (Token-aware, Fallback-safe, Evidence-based)
---

# Ultrathink Workflow v1.6

> 💡 **INFO:** Bu workflow 'Read-Only' modunda çalışır ve sadece analiz üretir. Gatekeeper kısıtlamalarından muaftır.

## Changelog (v1.6)
- ✅ Truncate uyarısı eklendi (Partial file transparency)
- ✅ Analiz durumu tanımları netleştirildi (Complete/Partial/Incomplete)
- ✅ Scope tespiti kod dosyalarına odaklandı (node_modules hariç)
- ✅ Kanıt formatı standardize edildi ([TRUNCATED], [MISSING])

## Changelog (v1.5)
- ✅ Token limiti eklendi (>50KB dosyalar kesiliyor)
- ✅ Fallback stratejisi eklendi (3+ eksik dosya → durdur)
- ✅ P0/P1/P2 kriterleri tanımlandı
- ✅ Risk matrisine dayalı değerlendirme (zorunlu bulgu kuralı kaldırıldı)
- ✅ Scope otomatik tespit

---

## 1. Ön Kontrol: Dosya Envanteri

Aşağıdaki dosyaları oku ve durumlarını kaydet:

| Dosya | Kritiklik | Token Limit |
|-------|-----------|-------------|
| `docs/project_brief.md` | **CRITICAL** | 10K |
| `docs/tech_stack.md` | **CRITICAL** | 8K |
| `docs/architecture.md` | **CRITICAL** | 15K |
| `docs/design_brief.md` | IMPORTANT | 5K |
| `docs/data_privacy.md` | IMPORTANT | 5K |
| `docs/registry.md` | OPTIONAL | 3K |

**Token Yönetimi:**
- Dosya >50KB ise → İlk 1000 satırı oku, geri kalanını `[...TRUNCATED]` ile işaretle
- Total token >150K ise → OPTIONAL dosyaları atla
- **Truncate Uyarısı:** Kesilen dosya için raporda şu notu ekle:
  > ⚠️ PARTIAL FILE: `[dosya_adı]` 50KB+, sadece ilk 1000 satır analiz edildi. Kritik bilgi eksik olabilir.

**Analiz Durumu Tanımları:**
- **Complete:** Tüm CRITICAL dosyalar okundu (eksik bilgi sorguları olsa bile)
- **Partial:** 1-2 CRITICAL dosya eksik
- **Incomplete:** 3+ CRITICAL dosya eksik (analiz durduruldu)

**Fallback Stratejisi:**
```
3+ CRITICAL dosya eksik → ❌ WORKFLOW DURDUR
  → Kullanıcıya: "Önce /start workflow çalıştırın"

1-2 CRITICAL dosya eksik → ⚠️ PARTIAL ANALIZ
  → Raporda "INCOMPLETE ANALYSIS" uyarısı ver

Tüm CRITICAL dosyalar mevcut → ✅ DEVAM
```

---

## 2. Scope Otomatik Tespit

**Sadece kod dosyalarını say:**
- Dahil: `src/`, `app/`, `lib/`, `components/` altındaki `.js`, `.ts`, `.py`, `.php`, `.java` dosyaları
- Hariç: `node_modules/`, `vendor/`, `dist/`, `build/`, test dosyaları

| Scope | Kriter (Kod Dosyası) | Odak |
|-------|---------------------|------|
| **Small** | <20 dosya, <5K satır | Over-engineering riski |
| **Medium** | 20-100 dosya, 5K-50K satır | Mimari tutarlılık |
| **Large** | >100 dosya, >50K satır | Scalability, Observability |

---

## 3. P0/P1/P2 Risk Kriterleri

Her bulgu için risk seviyesini şu kriterlere göre belirle:

### P0 (Kritik - Production Blocker)
- Güvenlik açığı (hardcoded secrets, SQL injection riski)
- Veri kaybı riski (migration, backup eksikliği)
- Teknoloji uyumsuzluğu (Örn: React seçilmiş ama Vue kurulu)

### P1 (Önemli - Teknik Borç)
- Performans darboğazı (N+1 query, cache yok)
- Ölçeklenebilirlik sorunu (single-point-of-failure)
- Bakım maliyeti (duplicate code, complex logic)

### P2 (İyileştirme - Nice-to-Have)
- Kod kalitesi (naming, structure)
- Dokümantasyon eksikliği
- Best practice ihlali (minor)

---

## 4. Risk Matrisi Değerlendirmesi

Her kategori için **kanıta dayalı** değerlendirme yap:

| Kategori | Kontrol Et |
|----------|------------|
| **Güvenlik** | Secrets, Auth, Encryption, CORS |
| **Mimari** | Layering, Separation of Concerns, SOLID |
| **Teknoloji** | Stack uyumu, deprecated libs, version conflicts |
| **Performans** | Query optimization, caching, lazy loading |
| **Veri** | Validation, backup strategy, GDPR |

**KURAL:** Gerçek bir risk yoksa `✅ Risk yok` de. Yapay bulgu üretme.

---

## 5. Sonuç Raporu

**Kanıt Formatı:**
- Dosya tam okunduysa: `project_brief.md:45`
- Dosya truncate edildiyse: `tech_stack.md:1200 [TRUNCATED]`
- Dosya yoksa: `architecture.md [MISSING]`

```markdown
# 🧠 Ultrathink Analiz Raporu v1.6

**Proje Scope:** [Small/Medium/Large]
**Analiz Durumu:** [Complete / Partial / Incomplete]
**Token Kullanımı:** [~XXK]

---

## 📊 Yönetici Özeti
[2-3 cümle: Projenin genel sağlık durumu]

---

## 🚨 P0 - Kritik Bulgular (Production Blocker)
| Kategori | Bulgu | Kanıt | Çözüm |
|----------|-------|-------|-------|
| [Güvenlik/Mimari/vb] | ... | [Dosya:Satır] | ... |

*Yoksa:* ✅ P0 risk tespit edilmedi.

---

## ⚠️ P1 - Önemli Bulgular (Teknik Borç)
- **[Kategori]**: [Bulgu] → [Öneri]

*Yoksa:* ✅ P1 risk tespit edilmedi.

---

## 💡 P2 - İyileştirme Fırsatları
- ...

---

## ❌ Eksik Bilgiler & Sorular
1. [Soru]
2. ...

---

## 🗺️ Önerilen Roadmap
- **Phase 1 (MVP):** [Odak]
- **Phase 2:** ...
```

---

## 6. Örnek Rapor (Referans)

```markdown
# 🧠 Ultrathink Analiz Raporu v1.6

**Proje Scope:** Medium
**Analiz Durumu:** Complete
**Token Kullanımı:** ~45K

---

## 📊 Yönetici Özeti
Proje Laravel + Filament stack kullanıyor, mimari temelde sağlam. Ancak multi-tenancy için tenant_id index'leri eksik (P1) ve `.env` dosyasının git'e commit edilme riski var (P0).

---

## 🚨 P0 - Kritik Bulgular
| Kategori | Bulgu | Kanıt | Çözüm |
|----------|-------|-------|-------|
| Güvenlik | `.env.example` var ama `.gitignore` kontrolü yok | `.gitignore:5` | `.env` ve `*.key` ekle |

---

## ⚠️ P1 - Önemli Bulgular
- **Performans**: `tenant_id` sütununda composite index yok → N+1 query riski
- **Mimari**: Payment logic controller'da → Service layer'a taşınmalı

---

## 💡 P2 - İyileştirme Fırsatları
- Variable naming: `$d` yerine `$donation` kullan
- Test coverage: Unit test yok

---

## ❌ Eksik Bilgiler
1. Backup stratejisi tanımlanmamış → RTO/RPO nedir?
2. Redis kullanılacak mı? (tech_stack.md'de belirsiz)

---

## 🗺️ Önerilen Roadmap
- **Phase 1:** P0 fix + tenant_id index
- **Phase 2:** Service layer refactor
- **Phase 3:** Test coverage %80
```
---

> **SON NOT:** Bu workflow token-aware ve fallback-safe olarak tasarlanmıştır. Production kullanımı için güvenlidir.