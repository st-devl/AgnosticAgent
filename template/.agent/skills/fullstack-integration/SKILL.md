---
name: fullstack-integration
version: "2.0.0"
requires: []
conflicts_with: []
description: |
  Use when: Building features that span both backend and frontend,
  creating APIs that will be consumed by UI, or implementing forms/modals.
  Keywords: API, endpoint, form, modal, entegrasyon, contract, sözleşme
allowed-tools: Read, Glob, Grep, Edit, Write (Subject to Gatekeeper)
---

# Backend ↔ Frontend Entegrasyon Skill

## 🎯 Amaç
Backend ve frontend'in kontrat-bazlı, kusursuz entegrasyonu.

---

## 🔒 Temel Prensipler

### 1. Kontrat-First Yaklaşım
- **ASLA** kontrat olmadan kod yazma
- Backend yazılmadan önce → kontrat
- Frontend yazılmadan önce → kontrat referansı

### 2. Zero Assumption
- Bilgi eksikse → **SOR**
- Belirsiz kısım varsa → **NETLEŞTİR**

### 3. Agnostic Approach
- Framework/dil belirtme
- `tech_stack.md`'ye atıf yap

---

## 📋 İşlem Sırası

### 1. KONTRAT VAR MI?
├─ **Evet** → 3'e git  
└─ **Hayır** → 2'ye git

---

### 2. KONTRAT OLUŞTUR (Adım Adım)

#### A) ŞABLON SEÇ:
- **CRUD operasyonu** → `.agent/skills/fullstack-integration/examples/crud-example.json`
- **Liste operasyonu** → `.agent/skills/fullstack-integration/examples/list-example.json`
- **Auth operasyonu** → `.agent/skills/fullstack-integration/examples/auth-example.json`

#### B) DOLDUR:
Şablon formatını kullanarak kontrat oluştur:
````json
{
  "operation": "[verb]_[entity]",  // Örn: create_donation
  "version": "1.0.0",
  "description": "[ne yapar - Türkçe]",
  "input": {
    "fields": [
      {
        "name": "[field_name]",
        "type": "string|number|boolean|object|array",
        "required": true/false,
        "validation": {
          "rules": {},
          "error_message": "[Türkçe mesaj]"
        },
        "description": "[açıklama]",
        "example": "[örnek değer]"
      }
    ]
  },
  "output": {
    "success": { "schema": {}, "example": {} },
    "errors": "Bkz: .agent/rules/error-handling.md"
  },
  "metadata": {
    "auth_required": true/false,
    "permissions": ["[permission:action]"],
    "idempotent": true/false,
    "cacheable": true/false,
    "http": {
      "method": "GET|POST|PUT|PATCH|DELETE",
      "path": "/api/v1/[resource]"
    }
  }
}
````

#### C) DOĞRULA:
- ✓ Naming & versioning: `.agent/rules/contract-standards.md`
- ✓ Error format: `.agent/rules/error-handling.md`
- ✓ Breaking change kontrolü (mevcut kontratla karşılaştır)

#### D) KAYDET:
- **Dosya yolu**: `contracts/[domain]/[entity]/v[version]/contract.json`
- Kullanıcıya göster ve onayla
- `contracts/registry.json` güncelle

---

### 3. KOD YAZ
- **Backend**: Kontrata sadık kal
- **Frontend**: Generated types kullan
- **Referans**: `.agent/rules/integration-checklist.md`

---

### 4. DOĞRULA
- **Checklist**: `.agent/rules/integration-checklist.md`

---

## 🚀 Büyük Feature İçin

Eğer feature **karmaşık/büyükse**:
````
🎯 Manuel workflow tetikle:
.agent/workflows/new-feature.md
````

Kullanıcıya şunu söyle:
> "Bu büyük bir feature. Adım adım ilerlemek için  
> `.agent/workflows/new-feature.md` workflow'unu kullanmamı ister misiniz?"

---

## 📚 İlgili Dosyalar

- **Kontrat şablonları**: `.agent/skills/fullstack-integration/contract-template.md`
- **Kontrat standartları**: `.agent/rules/contract-standards.md`
- **Error handling**: `.agent/rules/error-handling.md`
- **Doğrulama checklist**: `.agent/rules/integration-checklist.md`
- **Büyük feature workflow**: `.agent/workflows/new-feature.md`
- **Kontrat güncelleme workflow**: `.agent/workflows/contract-update.md`
- **Breaking change workflow**: `.agent/workflows/breaking-change.md`

---

## ⚡ Hızlı Kontrol

Her yanıtta kendinle şunu yap:
````
✓ Kontrat referansı var mı?
✓ Backend ↔ Frontend mapping açık mı?
✓ Error handling standart mı?
✓ Test senaryosu tanımlı mı?
````

Eksik varsa → ilgili rule/template dosyasını oku ve tamamla.