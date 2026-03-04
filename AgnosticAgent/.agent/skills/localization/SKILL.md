---
name: localization
version: "1.0.0"
requires: []
conflicts_with: []
description: |
  Use when: Implementing multi-language support, translation management,
  RTL layouts, or currency/date formatting.
  Keywords: i18n, l10n, translation, çeviri, multi-language, RTL, locale
allowed-tools: Read, Glob, Grep, Edit
---

# 🌍 Localization Skill

> Bu skill çok dilli uygulama geliştirme için **agnostik** prensipler sağlar.
> Herhangi bir framework veya çeviri sistemi için geçerlidir.

---

## 📋 Temel Prensipler

### 1. Çeviri Dosya Yapısı
```
lang/
├── tr.json    # Türkçe
├── en.json    # İngilizce
├── ar.json    # Arapça
└── de.json    # Almanca
```

### 2. Key Naming Convention
```json
{
  "common.save": "Kaydet",
  "common.cancel": "İptal",
  "donation.amount": "Bağış Miktarı",
  "donation.confirm": "Bağışı Onayla"
}
```

**Kurallar:**
- Dot notation (`section.key`)
- Snake_case veya camelCase (tutarlı ol)
- Açıklayıcı isimler

### 3. Fallback Mekanizması
```
ar → en → tr (default)
```
Çeviri bulunamazsa fallback dile geç.

---

## 🔄 RTL (Right-to-Left) Desteği

### RTL Diller
- Arapça (ar)
- İbranice (he)
- Farsça (fa)

### RTL Kuralları
- `dir="rtl"` attribute
- CSS: `text-align: start` (left/right yerine)
- Flexbox: `flex-direction` otomatik döner
- Icon'lar mirror olabilir (ok işaretleri)

---

## 💰 Para Birimi Formatı

### Locale-Aware Formatting
```
en-US: $1,234.56
de-DE: 1.234,56 €
tr-TR: ₺1.234,56
ar-SA: ١٬٢٣٤٫٥٦ ر.س
```

### Kurallar
- Para birimi sembolü locale'e göre
- Ondalık ayırıcı locale'e göre
- Binlik ayırıcı locale'e göre

---

## 📅 Tarih Formatı

| Locale | Format | Örnek |
|--------|--------|-------|
| en-US | MM/DD/YYYY | 01/17/2026 |
| de-DE | DD.MM.YYYY | 17.01.2026 |
| tr-TR | DD.MM.YYYY | 17.01.2026 |
| ja-JP | YYYY/MM/DD | 2026/01/17 |

---

## ✅ Kontrol Listesi

Çok dilli uygulama yaparken:

- [ ] Hardcoded string var mı?
- [ ] Tüm UI metinleri key ile mi çağrılıyor?
- [ ] Fallback dil tanımlı mı?
- [ ] RTL layout test edildi mi?
- [ ] Para birimi locale-aware mı?
- [ ] Tarih formatı locale-aware mı?
- [ ] Pluralization destekleniyor mu?

---

## ⚠️ Yasaklar

- ❌ Hardcoded metin kullanma
- ❌ String concatenation ile cümle oluşturma
- ❌ Sabit tarih/para formatı kullanma
- ❌ RTL'i görmezden gelme

---

> **NOT:** Spesifik framework implementasyonları (Laravel, React-i18n vb.) proje dokümantasyonunda tanımlanır.
