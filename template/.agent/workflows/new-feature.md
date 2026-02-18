---
description: new-feature - Büyük, çok adımlı feature geliştirme süreci (CRUD + endpoint + UI)
---

> ⚠️ **GATEKEEPER BAĞLANTISI:** Tüm write işlemleri kullanıcı onayı gerektirir. Bkz: `.agent/rules/gatekeeper.md`

# Yeni Feature Workflow

> Bu workflow **MANUEL** tetiklenir.
> Kullanım: Karmaşık, çok adımlı feature'lar için.

## 🎯 Ne Zaman Kullan

- Feature birden çok endpoint içeriyor
- Backend + Frontend + State + Test gerekiyor
- Kontrat karmaşık veya çok katmanlı

## 📋 Adım Adım Süreç

### ADIM 1: Bağlam Toplama

Kullanıcıya sor:
```
🔍 FEATURE BAĞLAMI:

1. Domain/Modül: [hangi iş alanı]
2. Feature açıklaması: [ne yapacak]
3. Kullanıcı senaryosu: [kullanıcı ne yapacak]
4. Backend gereksinimleri:
   - CRUD operasyonları: [liste]
   - İş kuralları: [liste]
   - Auth/permission: [gereksinimler]
5. Frontend gereksinimleri:
   - UI parçaları: [sayfa/component liste]
   - User interactions: [form, button, vb.]
   - State yönetimi: [lokal/global]
6. Mevcut benzer feature'lar: [varsa]
```

Cevapları topla. Eksik varsa → sor.

---

### ADIM 2: Feature Planlama

Toplanan bilgilerle plan oluştur:
```
📦 FEATURE PLANI: [Feature Adı]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. KONTRATLAR (önce bunlar)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   1.1 [operation_1@v1.0.0]
       - Input: [özet]
       - Output: [özet]
       - Dosya: contracts/[domain]/[entity]/v1.0.0/

   1.2 [operation_2@v1.0.0]
       ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. BACKEND (kontratlar sonrası)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   2.1 [handler/controller name]
       - Kontrat: [operation_1@v1.0.0]
       - Sorumluluk: [ne yapar]

   2.2 [handler/controller name]
       ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. FRONTEND (backend sonrası)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   3.1 [component/page name]
       - Kontrat bağlantısı: [operation@version]
       - UI sorumluluk: [ne gösterir]

   3.2 [component/page name]
       ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. ENTEGRASYON & TEST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   4.1 Test senaryoları
   4.2 Mock data
   4.3 Integration tests

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TAHMİNİ SÜREÇ: [kaç adım, kaç mesaj]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Kullanıcıya göster ve onayla.

---

### ADIM 3: Kontrat Oluşturma (Sırayla)

Her kontrat için:

1. Şablonu kullan: `.agent/skills/fullstack-integration/contract-template.md`
2. Standartları kontrol et: `.agent/rules/contract-standards.md`
3. Error format kontrol: `.agent/rules/error-handling.md`
4. Breaking change kontrolü yap
5. Kontratı göster ve onayla
6. Dosyaya kaydet: `contracts/[domain]/[entity]/v[version]/contract.json`

**Kural:** Bir kontrat onaylanmadan bir sonrakine geçme.

---

### ADIM 4: Backend Kodlama (Sırayla)

Her backend parçası için:

1. İlgili kontratı oku
2. Kontrata sadık kod yaz
3. Kontrat uyum notları ekle
4. Validation/serialization kontrol et
5. Kodu göster ve onayla

**Kural:** Bir parça onaylanmadan bir sonrakine geçme.

---

### ADIM 5: Frontend Kodlama (Sırayla)

Her frontend parçası için:

1. İlgili kontratı oku
2. Generated types kullan (eğer varsa, yoksa type safety sağla)
3. Backend bağlantısını açıkça belirt
4. State mapping yap
5. Error handling ekle
6. Kodu göster ve onayla

**Kural:** Bir parça onaylanmadan bir sonrakine geçme.

---

### ADIM 6: Entegrasyon Doğrulama

Tüm parçalar tamamlandıktan sonra:

1. Checklist'i çalıştır: `.agent/rules/integration-checklist.md`
2. Eksik maddeleri tespit et
3. Eksikleri tamamla
4. Test senaryolarını tanımla

---

### ADIM 7: Dokümantasyon

1. `contracts/registry.json` güncelle
2. `docs/registry.md` güncelle (varsa)
3. CHANGELOG.md'ye ekle (breaking change varsa)
4. Usage example ekle

---

### ADIM 8: Özet Raporu

Workflow sonunda kullanıcıya özet sun:

> 📌 Rapor şablonu: `.agent/templates/reports/feature_report.md`

Raporu oluşturmak için script kullan (opsiyonel):
```bash
python3 .agent/scripts/auto/gen_report.py --type feature
```

## ⚡ Hızlı İpuçları

- Her adımı kullanıcıyla onaylayarak ilerle
- Bir adım başarısız → durma, düzelt, devam et
- Eksik bilgi → hemen sor, tahmin etme
- Büyük kod blokları → artifact kullan