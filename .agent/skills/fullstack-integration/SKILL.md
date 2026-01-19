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

## 📋 İşlem Sırası (Basit)
```
1. KONTRAT VAR MI?
   ├─ Evet → 3'e git
   └─ Hayır → 2'ye git

2. KONTRAT OLUŞTUR
   ├─ Bkz: .agent/skills/fullstack-integration/contract-template.md
   ├─ Bkz: .agent/rules/contract-standards.md
   └─ Breaking change kontrolü yap

3. KOD YAZ
   ├─ Backend: kontrata sadık kal
   ├─ Frontend: generated types kullan
   └─ Bkz: .agent/rules/integration-checklist.md

4. DOĞRULA
   └─ Bkz: .agent/rules/integration-checklist.md
```

---

## 🚀 Büyük Feature İçin

Eğer feature karmaşık/büyükse:
```
🎯 Manuel workflow tetikle:
.agent/workflows/new-feature.md
```

Kullanıcıya şunu söyle:
> "Bu büyük bir feature. Adım adım ilerlemek için 
> `.agent/workflows/new-feature.md` workflow'unu kullanmamı ister misiniz?"

---

## 📚 İlgili Dosyalar

- **Kontrat şablonları:** `.agent/skills/fullstack-integration/contract-template.md`
- **Kontrat standartları:** `.agent/rules/contract-standards.md`
- **Error handling:** `.agent/rules/error-handling.md`
- **Doğrulama checklist:** `.agent/rules/integration-checklist.md`
- **Büyük feature workflow:** `.agent/workflows/new-feature.md`
- **Kontrat güncelleme workflow:** `.agent/workflows/contract-update.md`
- **Breaking change workflow:** `.agent/workflows/breaking-change.md`

---

## ⚡ Hızlı Kontrol

Her yanıtta kendinle şunu yap:
```
✓ Kontrat referansı var mı?
✓ Backend ↔ Frontend mapping açık mı?
✓ Error handling standart mı?
✓ Test senaryosu tanımlı mı?
```

Eksik varsa → ilgili rule/template dosyasını oku ve tamamla.