---
trigger: always_on
---

# Kontrat Standartları

> Bu kurallar TÜM kontratlar için geçerlidir.

## 🔒 Zorunlu Kurallar

### 1. Versiyonlama
```
Format: MAJOR.MINOR.PATCH

MAJOR: Breaking change
MINOR: Yeni özellik (backward compatible)
PATCH: Bug fix

Örnek: 1.2.3
```

### 2. İsimlendirme Konvansiyonları

**Operation names:**
- Format: `[verb]_[entity]`
- Örnekler: `create_donation`, `list_campaigns`, `update_user`
- Kullanma: camelCase ❌, PascalCase ❌
- Kullan: snake_case ✅

**Field names:**
- Backend: snake_case (`user_id`, `created_at`)
- Frontend: tech_stack.md'ye göre (genelde camelCase)
- Transformation: otomatik mapping ile

**Error codes:**
- Format: `[CATEGORY]_[SPECIFIC]`
- Örnekler: `VALIDATION_REQUIRED_FIELD`, `AUTH_TOKEN_EXPIRED`
- Tümü UPPER_SNAKE_CASE

### 3. Required Fields (Her Kontrat)

Minimum zorunlular:
```json
{
  "operation": "string (zorunlu)",
  "version": "string (zorunlu, semver)",
  "description": "string (zorunlu)",
  "input": "object (zorunlu)",
  "output": "object (zorunlu)",
  "metadata": "object (zorunlu)"
}
```

### 4. Metadata Zorunlulukları
```json
{
  "metadata": {
    "auth_required": "boolean (zorunlu)",
    "permissions": "array (auth_required=true ise zorunlu)",
    "idempotent": "boolean (POST/PUT/PATCH için zorunlu)",
    "cacheable": "boolean (GET için zorunlu)"
  }
}
```

### 5. Type System

Allowed primitive types:
- `string`
- `number`
- `boolean`
- `object`
- `array`
- `null`

Complex types:
- `object`: nested schema tanımla
- `array`: item type belirt (`array<string>`)

**Yasak:**
- `any`, `unknown`, `mixed` gibi belirsiz tipler
- Platform-specific tipler (`int32`, `float64` → `number` kullan)

### 6. Validation Rules Format
```json
{
  "validation": {
    "rules": {
      "min": "number",
      "max": "number",
      "pattern": "regex string",
      "enum": ["allowed", "values"],
      "custom": "function reference (tech_stack.md'de tanımlı)"
    },
    "error_message": "string (kullanıcı dostu)"
  }
}
```

## 🔄 Breaking Change Tanımı

**Breaking changes:**
- ❌ Field silme
- ❌ Field tipini değiştirme
- ❌ Required field ekleme
- ❌ Enum value silme
- ❌ Response structure değişikliği
- ❌ Error format değişikliği

**Non-breaking changes:**
- ✅ Optional field ekleme
- ✅ Enum value ekleme
- ✅ Response field ekleme (backward compatible)
- ✅ Validation kuralı gevşetme
- ✅ Documentation güncelleme

## 📋 Breaking Change Checklist

Breaking change yapıyorsan:
- [ ] MAJOR version bump
- [ ] CHANGELOG.md'ye ekle
- [ ] Migration guide yaz
- [ ] Deprecation timeline belirt
- [ ] Etkilenen yerleri tespit et
- [ ] Backward compatibility plan (mümkünse)

## 🎯 Tech Stack Referansı

Kontratlar agnostic olmalı AMA implementation details için:
```
Tech-specific detaylar için:
- Validation library: tech_stack.md → validator
- Type generation: tech_stack.md → type_generator
- Serialization: tech_stack.md → serializer
```

## ✅ Kontrat Doğrulama

Her kontrat yazıldığında kontrol et:
```
✓ Version semver formatında mı?
✓ Operation name snake_case mi?
✓ Required fields eksik mi?
✓ Error handling standart mı? (Bkz: error-handling.md)
✓ Validation rules tanımlı mı?
✓ Metadata complete mi?
✓ Breaking change analizi yapıldı mı?
✓ Type safety korunuyor mu?
```

Eksik varsa → hemen düzelt veya sor.