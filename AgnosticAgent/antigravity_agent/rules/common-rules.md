---
description: Tüm skill'lerin paylaştığı ortak mühendislik disiplini kuralları
---

# 📏 Ortak Kurallar (Common Rules)

> Bu dosya tüm skill'ler tarafından referans edilen ortak prensipleri içerir.
> Referans: `component-architecture`, `database-architecture`, `performance`

---

## 🎯 1. DRY (Don't Repeat Yourself)

- Aynı yapı 2+ yerde varsa → tek kaynak + parametre
- Copy-paste yerine abstraction kullan
- Her tekrar → potansiyel tutarsızlık kaynağı

## 🧱 2. SSOT (Single Source of Truth)

- Her veri, ayar veya konfigürasyon **tek bir yerde** tanımlı olmalı
- Çelişki durumunda `docs/tech_stack.md` > `docs/architecture.md` > `docs/prd.md`
- Detaylı hiyerarşi: `.agent/config/rules.yaml` → `ssot.priority`

## 📐 3. Naming Conventions

| Dil | Stil | Örnek |
|-----|------|-------|
| Python | snake_case | `user_service.py` |
| JavaScript/TypeScript | camelCase | `userService.ts` |
| PHP | PascalCase (class) | `UserController.php` |
| Database | snake_case | `user_profiles` |
| API Operations | snake_case | `create_donation` |
| Error Codes | UPPER_SNAKE_CASE | `VALIDATION_REQUIRED_FIELD` |

## 🏗️ 4. Katmanlı Mimari

```
Controller/Handler  → İş akışı yönlendirme (ince)
Service Layer       → İş mantığı (kalın)
Repository/Model    → Veri erişimi
```

- Controller'da iş mantığı **YASAK**
- Model'de HTTP mantığı **YASAK**
- Her katman sadece alt katmanını çağırır

## ⚡ 5. Performans Farkındalığı

Her yapıda şu soruyu sor:
> "Bu 1000 kayıtta nasıl davranır? 100.000'de?"

- N+1 query → eager loading / batch
- Tekrarlayan hesaplama → cache
- Ağır iş → queue/async

## 🔒 6. Güvenlik Temelleri

- Input **asla** güvenilmez → validation zorunlu
- SQL parametreleri **asla** string concat → prepared statement
- Hassas veri **asla** log'a yazılmaz
- Detaylı kurallar: `.agent/skills/enterprise-security/SKILL.md`

## 📋 7. Kod Yazma Ritüeli

Her dosya oluşturma/düzenleme öncesinde:
1. `docs/registry.md` güncel mi? → değilse güncelle
2. Mevcut yapıya benzer pattern var mı? → varsa aynı pattern'ı takip et
3. Test/validation gerekli mi? → gerekliyse planla

---

> **KURAL:** Bu dosyada tanımlanan prensipler tüm skill'lerde geçerlidir. Çelişki durumunda skill-spesifik kurallar önceliklidir.
