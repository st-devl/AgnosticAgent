---
description: architecture_check v2.0 - Mimari bütünlük denetimi (Scope-aware, Score-based, Security-included)
---

# Architecture Integrity Check v2.0

> 💡 **INFO:** Bu workflow 'Read-Only' modunda çalışır, sadece analiz üretir.

## Changelog (v2.0)
- ✅ GEMINI.md bağımlılığı opsiyonel yapıldı (Fallback: Built-in best practices)
- ✅ Objektif skor kriterleri eklendi (P0/P1/P2 bazlı)
- ✅ Scope tanımlandı (src/, app/, 100K token limit)
- ✅ Security & Error Handling kontrolleri eklendi
- ✅ Ultrathink formatı ile uyumlu hale getirildi
- ✅ Kontrol matrisi tablo formatına çevrildi

---

## Ne Zaman Çalıştırılır?
- Sprint sonunda (haftalık)
- Büyük refactor öncesi
- Production deploy öncesi

---

## 1. Scope & Referans Dosyaları

**Scope Tanımı:**
- **Dahil:** `src/`, `app/`, `lib/`, `components/` altındaki kod dosyaları
- **Hariç:** `node_modules/`, `vendor/`, `dist/`, `build/`, test dosyaları
- **Token Limit:** Tek dosya >50KB → İlk 1000 satır, Total >100K token → Durdur

Eğer varsa şu dosyaları oku:
- `docs/tech_stack.md` - Technology stack and principles
- `.agent/skills/component-architecture/SKILL.md` - DRY, composition patterns
- `.agent/skills/code-review/SKILL.md` - Kalite kontrol standartları

**Dosyalar yoksa:** Built-in best practices kullan (SOLID, DRY, KISS, YAGNI)

---

## 2. Kontrol Matrisi

| Kategori | Arama Kriterleri | P0 Tetikleyicileri |
|----------|------------------|-------------------|
| **Yama/Patch** | TODO, FIXME, HACK yorumları; magic number/string | Production code'da TODO, Hardcoded critical value |
| **Katman Tutarlılığı** | Controller→Service→Repo akışı; DI kullanımı | Controller'da DB query, Circular dependency |
| **DRY İhlali** | Duplicate code (>10 satır); copy-paste pattern | 3+ yerde aynı logic, No abstraction |
| **Performans** | N+1 query, eager load, pagination eksikliği | Loop içinde query, No lazy loading |
| **Security** | Hardcoded secret, auth bypass, SQL concatenation, CORS config | Şifre plaintext, No authentication |
| **Error Handling** | Try-catch tutarlılığı, global error handler, logging | Hata yutulmuş (empty catch), No error log |

---

## 3. P0/P1/P2 Risk Tanımları

### P0 (Kritik - İmmediate Action)
- Güvenlik açığı (secret leak, SQL injection)
- Circular dependency (sistem çalışmaz)
- Production blocker (critical path hatası)

### P1 (Önemli - Sprint İçinde)
- DRY ihlali (3+ yerde duplicate)
- Performans darboğazı (N+1 query)
- Katman ihlali (Controller'da business logic)

### P2 (İyileştirme - Backlog)
- Magic number/string
- TODO yorumu
- Naming convention ihlali

---

## 4. Her Bulgu İçin Format

**Kanıt Formatı:**
- Dosya tam: `UserController.php:45`
- Truncate: `LargeService.php:1200 [TRUNCATED]`
- Pattern-based: `Multiple files (3+): auth/*.php`

```markdown
### [Bulgu Adı]
- **Konum**: [Dosya:Satır]
- **Sorun**: [Açıklama]
- **Etki**: [Neden P0/P1/P2]
- **Refactor Planı**: [Adımlar]
```

---

## 5. Sonuç Raporu (Ultrathink Uyumlu)

```markdown
# 🏗️ Architecture Check Raporu v2.0

**Scope:** [X dosya, Y satır]
**Token Kullanımı:** [~XXK]

---

## 📊 Mimari Bütünlük Skoru: X/10

**Hesaplama:**
- Başlangıç: 10 puan
- P0 bulguları: -2 puan × [sayı] = -X
- P1 bulguları: -1 puan × [sayı] = -Y
- P2 bulguları: -0.5 puan × [sayı] = -Z
- **Final:** 10 - X - Y - Z = [SKOR]

**Değerlendirme:**
- 9-10: Mükemmel
- 7-8: İyi, minor iyileştirmeler
- 5-6: Orta, refactor gerekli
- 3-4: Zayıf, acil müdahale
- 0-2: Kritik durum

---

## 🚨 P0 - Kritik Bulgular
| Kategori | Bulgu | Konum | Refactor Planı |
|----------|-------|-------|----------------|
| [Security/Mimari] | ... | [Dosya:Satır] | ... |

*Yoksa:* ✅ P0 bulgu yok.

---

## ⚠️ P1 - Önemli Bulgular
- **[Kategori]**: [Bulgu] @ [Konum] → [Öneri]

*Yoksa:* ✅ P1 bulgu yok.

---

## 💡 P2 - İyileştirme Önerileri
- ...

*Yoksa:* ✅ P2 bulgu yok.

---

## 🗺️ Refactor Roadmap
1. **Acil (P0):** [Öncelik sırası]
2. **Sprint İçi (P1):** ...
3. **Backlog (P2):** ...
```

---

## 6. Örnek Rapor (Referans)

```markdown
# 🏗️ Architecture Check Raporu v2.0

**Scope:** 45 dosya, 8.5K satır
**Token Kullanımı:** ~35K

---

## 📊 Mimari Bütünlük Skoru: 7/10

**Hesaplama:**
- Başlangıç: 10 puan
- P0: 1 bulgu × -2 = -2
- P1: 1 bulgu × -1 = -1
- P2: 0 bulgu × -0.5 = 0
- **Final:** 7/10

**Değerlendirme:** İyi, minor refactor'lar yapılabilir.

---

## 🚨 P0 - Kritik Bulgular
| Kategori | Bulgu | Konum | Refactor Planı |
|----------|-------|-------|----------------|
| Security | Hardcoded DB password | `config/database.php:12` | Move to .env, use getenv() |

---

## ⚠️ P1 - Önemli Bulgular
- **DRY İhlali**: User validation logic 3 yerde duplicate @ `UserController.php:45, ProfileController.php:89, AdminController.php:102` → Extract to `UserValidator` service

---

## 💡 P2 - İyileştirme Önerileri
✅ P2 bulgu yok.

---

## 🗺️ Refactor Roadmap
1. **Acil (P0):** DB password .env'e taşı
2. **Sprint İçi (P1):** UserValidator service oluştur
```

---

> **SON NOT:** Bu workflow token-aware, scope-safe ve objektif skor sistemine sahiptir. Production kullanımı için hazırdır.
