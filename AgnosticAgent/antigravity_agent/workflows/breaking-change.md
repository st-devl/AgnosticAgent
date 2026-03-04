---
description: breaking-change - Breaking change yönetimi, migration guide ve deprecation planı
---

> ⚠️ **GATEKEEPER BAĞLANTISI:** Tüm write işlemleri kullanıcı onayı gerektirir. Bkz: `.agent/rules/gatekeeper.md`

# Breaking Change Yönetimi Workflow

> Bu workflow **MANUEL** tetiklenir.
> Kullanım: Breaking change gerektiğinde güvenli migration.

## ⚠️ Ne Zaman Kullan

- Field silme/değiştirme
- Response structure değişikliği
- Validation kuralı sıkılaştırma
- Required field ekleme

## 🚨 Kritik Uyarı

Breaking change **SON ÇARE** olmalı.
Önce backward compatible çözüm ara:
- Yeni field ekle, eski field'ı deprecate et
- Validation kuralı gevşet
- Response'a yeni field ekle (eski field'ları koru)

Eğer gerçekten breaking change gerekiyorsa → devam et.

---

## 📋 Workflow Adımları

### ADIM 1: Etki Analizi
````
🔍 BREAKING CHANGE ETKİ ANALİZİ:

Kontrat: [operation_name@current_version]

Yapılacak değişiklik:
- [detaylı açıklama]

Neden breaking?:
- [gerekçe]

Etkilenecek yerler:
Backend:
- [dosya/modül listesi]

Frontend:
- [component/hook listesi]

Users:
- [kaç kullanıcı etkilenir?]
- [kullanım sıklığı?]

Alternatifleri değerlendirdin mi?:
- [ ] Backward compatible çözüm aradım
- [ ] Deprecation yoluyla geçiş mümkün mü?
- [ ] Versiyonlama ile iki endpoint'i paralel tutabilir miyim?
````

Kullanıcıya göster ve onay al. Eğer alternatif varsa → önce onu dene.

---

### ADIM 2: Yeni Versiyon Oluşturma
````
1. Version calculation:
   - Current: v[major].[minor].[patch]
   - New: v[major+1].0.0

2. Yeni klasör oluştur:
   contracts/[domain]/[entity]/v[new_major].0.0/

3. Yeni kontrat dosyası oluştur (değişikliklerle)
````

---

### ADIM 3: Migration Guide Yazma

Detaylı migration guide oluştur:
````markdown
# Migration Guide: [operation_name] v[old] → v[new]

## ⚠️ Breaking Changes

### 1. [Değişiklik Başlığı]

**What changed:**
- [ne değişti]

**Why:**
- [neden]

**Before (v[old]):**
```json
{
  "old_field": "value"
}
```

**After (v[new]):**
```json
{
  "new_field": "value"
}
```

**Impact:**
- [kim etkilenir]
- [ne yapması gerekir]

---

## 🔄 Migration Steps

### Backend Migration

#### Step 1: [başlık]
````
[detaylı adımlar]
````

#### Step 2: [başlık]
````
[detaylı adımlar]
````

### Frontend Migration

#### Step 1: [başlık]
````
[detaylı adımlar]
````

#### Step 2: [başlık]
````
[detaylı adımlar]
````

---

## 📅 Timeline

- **v[old] End of Life:** [date] (örn: 3 ay sonra)
- **v[new] Available:** [date] (örn: şimdi)
- **Migration Deadline:** [date] (örn: 2.5 ay sonra)

---

## ✅ Migration Checklist

Backend:
- [ ] [adım 1]
- [ ] [adım 2]

Frontend:
- [ ] [adım 1]
- [ ] [adım 2]

Testing:
- [ ] [adım 1]
- [ ] [adım 2]

---

## 🆘 Support

Sorun yaşarsan:
- [support email/link]
- [documentation link]
````

---

### ADIM 4: Parallel Support Planı
````
🔀 PARALLEL SUPPORT STRATEGY:

v[old]:
- Status: DEPRECATED
- Supported until: [date]
- Warning messages: [uyarı metni]

v[new]:
- Status: STABLE
- Available from: [date]
- Default version: [date]'den itibaren

Transition period: [X] months
````

---

### ADIM 5: Deprecation Warning Ekleme

Eski versiyona deprecation warning ekle:
````
Backend (v[old]):
- Response header ekle: X-Deprecated: true
- Response header ekle: X-Deprecated-Version: v[old]
- Response header ekle: X-New-Version: v[new]
- Response header ekle: X-Sunset: [date]
- Warning log ekle

Frontend (v[old] kullanan):
- Console warning göster
- UI'da deprecation banner (optional)
````

---

### ADIM 6: Yeni Versiyon Kodu

1. Backend: v[new] endpoint/handler yaz
2. Frontend: v[new] kullan (yeni component/hook)
3. Test: her iki versiyonu test et

---

### ADIM 7: Dokümantasyon

1. CHANGELOG.md:
````markdown
## [v[new_major].0.0] - [date]

### ⚠️ BREAKING CHANGES

- [değişiklik 1]
- [değişiklik 2]

### Migration

See MIGRATION_v[old]_to_v[new].md
````

2. Migration guide dosyası: `MIGRATION_v[old]_to_v[new].md`

3. contracts/registry.json güncelle:
````json
{
  "[operation_name]": {
    "versions": {
      "v[old]": {
        "status": "deprecated",
        "sunset_date": "[date]"
      },
      "v[new]": {
        "status": "stable"
      }
    }
  }
}
````

---

### ADIM 8: Communication Plan

Kullanıcılara duyuru:
````
📢 BREAKING CHANGE ANNOUNCEMENT

Subject: [operation_name] API v[new] Released

Dear users,

We've released v[new] of [operation_name] API with breaking changes.

**What's changing:**
- [summary of changes]

**Timeline:**
- v[old]: Supported until [date]
- v[new]: Available now

**Action required:**
- Migrate before [date]
- See migration guide: [link]

**Support:**
- Questions: [link]
- Issues: [link]

Thank you for your cooperation.
````

---

### ADIM 9: Özet Raporu
````
✅ BREAKING CHANGE UYGULAND I

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 KONTRAT BİLGİSİ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Operation: [operation_name]
- Old Version: v[old] (DEPRECATED)
- New Version: v[new] (STABLE)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ BREAKING CHANGES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- [change 1]
- [change 2]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 TIMELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- v[old] EOL: [date]
- Migration deadline: [date]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 DOKÜMANTASYON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Migration guide: MIGRATION_v[old]_to_v[new].md ✓
- CHANGELOG.md ✓
- contracts/registry.json ✓
- Deprecation warnings ✓
- User announcement ✓

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Announce to users
2. Monitor migration progress
3. Support users during transition
4. Remove v[old] on [date]
````
````
