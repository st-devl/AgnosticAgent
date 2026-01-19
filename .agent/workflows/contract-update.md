---
description: contract-update - Mevcut kontrat güncelleme ve breaking change analizi
---

> ⚠️ **GATEKEEPER BAĞLANTISI:** Tüm write işlemleri kullanıcı onayı gerektirir. Bkz: `.agent/rules/gatekeeper.md`

# Kontrat Güncelleme Workflow

> Bu workflow **MANUEL** tetiklenir.
> Kullanım: Mevcut kontratı güncelleme gerektiğinde.

## 🎯 Ne Zaman Kullan

- Mevcut endpoint'e yeni field ekleme
- Validation kuralı değiştirme
- Error handling iyileştirme
- Business logic değişikliği

## 📋 Workflow Adımları

### ADIM 1: Mevcut Kontratı Oku
````
1. Hangi kontrat?: [operation_name@current_version]
2. Kontrat dosyasını oku: contracts/[domain]/[entity]/v[current_version]/
3. Mevcut şemayı göster kullanıcıya
````

---

### ADIM 2: Değişiklik Talebi Topla

Kullanıcıya sor:
````
🔄 KONTRAT DEĞİŞİKLİĞİ:

1. Ne değişecek?: [açıklama]
2. Neden değişiyor?: [sebep]
3. Etkilenen yerler?: [backend/frontend dosyaları]
````

---

### ADIM 3: Breaking Change Analizi

Değişiklikleri analiz et:
````
🔍 BREAKING CHANGE ANALİZİ:

Yapılacak değişiklikler:
- [değişiklik 1]: [BREAKING / NON-BREAKING]
- [değişiklik 2]: [BREAKING / NON-BREAKING]

Sonuç:
[ ] NON-BREAKING → MINOR/PATCH bump
[ ] BREAKING → MAJOR bump

Eğer BREAKING:
  ⚠️ Breaking change tespit edildi!
  - Migration gerekecek
  - Yeni versiyon oluşturulacak
  - Eski versiyon deprecate edilecek
````

Kullanıcıya göster ve onay al.

---

### ADIM 4A: Non-Breaking Update (Kolay Yol)

Eğer NON-BREAKING:

1. Version bump (MINOR veya PATCH)
2. Mevcut kontratı güncelle
3. CHANGELOG.md'ye ekle
4. Backend/frontend kodu güncelle (gerekirse)
5. Test senaryoları güncelle

---

### ADIM 4B: Breaking Update (Dikkatli Yol)

Eğer BREAKING:

1. Yeni versiyon oluştur: v[MAJOR+1].0.0
2. Yeni klasör: `contracts/[domain]/[entity]/v[new_version]/`
3. Yeni kontrat dosyası oluştur
4. Migration guide yaz:
````markdown
# Migration Guide: v[old] → v[new]

## Breaking Changes

1. [değişiklik 1]
   - **Was:** [eski hali]
   - **Now:** [yeni hali]
   - **Action:** [ne yapmalı]

2. [değişiklik 2]
   ...

## Migration Steps

Backend:
1. [adım 1]
2. [adım 2]

Frontend:
1. [adım 1]
2. [adım 2]

## Deprecation Timeline

- v[old]: Supported until [date]
- v[new]: Available from [date]
````

5. Eski versiyonu deprecate et (README ekle)
6. CHANGELOG.md'ye MAJOR change ekle

---

### ADIM 5: Kod Güncelleme

1. Backend kodu güncelle (kontrata uygun)
2. Frontend kodu güncelle (yeni types kullan)
3. Test senaryoları güncelle

---

### ADIM 6: Doğrulama

Checklist çalıştır: `.agent/rules/integration-checklist.md`

---

### ADIM 7: Özet
````
✅ KONTRAT GÜNCELLENDİ

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 KONTRAT BİLGİSİ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Operation: [operation_name]
- Old Version: v[old]
- New Version: v[new]
- Change Type: [BREAKING / NON-BREAKING]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 DEĞİŞİKLİKLER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- [değişiklik 1]
- [değişiklik 2]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ ETKİLENEN YERLER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Backend:
- [file_1]
- [file_2]

Frontend:
- [file_1]
- [file_2]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 DOKÜMANTASYON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- CHANGELOG.md ✓
- Migration guide ✓ (eğer breaking)
- contracts/registry.json ✓
````