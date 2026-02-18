---
description: Görevi derinlemesine analiz et, riskleri belirle ve en iyi uygulama planını oluştur.
---

# Think Protocol

⚠️ Bu protokol aktif olduğunda: Kullanıcı onayı OLMADAN kod yazma, dosya değiştirme veya işlem yapma.
İlk adım: Analiz → Plan → Onay.

---

## FAZI: KAPSAMLI ANALİZ

Aşağıdaki tüm maddeleri değerlendir:

### 1. Gereksinim & Kapsam
- Kullanıcı tam olarak ne istiyor? (iş hedefi, beklenen çıktı)
- Varsayılan ama belirtilmemiş noktalar var mı?
- Netleştirme gereken kritik sorular neler?

### 2. Mimari Etki & SSOT Uyumu
- Mevcut sistem mimarisi nasıl etkilenir?
- SSOT (Single Source of Truth) yapısına uyumlu mu?
- Yeni SSOT tanımı mı, mevcut genişletme mi?
- Tekrar eden kod/yapı riski var mı?

### 3. Dependency & Side Effect Analizi
- Değişiklik hangi dosyaları/modülleri etkiler? (dependency map)
- Upstream/downstream etkileri neler?
- Beklenmeyen yan etkiler oluşur mu?

### 4. Performans & Ölçeklenebilirlik
- Yük altında darboğaz riski var mı?
- Cache, async, batch, pagination ihtiyacı var mı?
- Token/API call/resource optimizasyonu gerekir mi?

### 5. Veri & Schema Etkisi
- Yeni tablo/kolon gerekir mi? İlişkiler doğru mu?
- Index, constraint, migration stratejisi nedir?
- Veri şişmesi veya tutarsızlık riski var mı?

### 6. Güvenlik & Hata Yönetimi
- Güvenlik açığı, yetkisiz erişim riski var mı?
- Edge case'ler ve hata senaryoları neler?
- Logging, error handling stratejisi nasıl olmalı?

### 7. İdempotency & Determinizm
- Aynı input her zaman aynı output'u verir mi?
- State yönetimi tutarlı mı?
- Rollback/retry mekanizması gerekir mi?

### 8. Observability & Testing
- Logging, monitoring, tracing ihtiyacı var mı?
- Debug edilebilirlik nasıl sağlanır?
- Hangi testler yazılmalı? (unit, integration, edge case)

### 9. Alternatif Çözümler
- Daha sade/hızlı/güvenli bir yaklaşım var mı?
- Trade-off'lar neler? (complexity vs simplicity, speed vs safety)
- Technical debt oluşur mu, azalır mı?

### 10. Rollback & Disaster Recovery
- Geri alma planı nedir?
- Kritik hata durumunda toparlanma stratejisi var mı?

---

## FAZ II: ONAY NOKTASI

Analiz tamamlandığında `notify_user` çağır. İlet:
- **Özet Analiz:** Gereksinim + riskler + SSOT uyumu
- **Önerilen Yaklaşım:** Mimari tercih + alternatifler
- **Etki Haritası:** Değişecek dosyalar + dependency'ler
- **Uygulama Planı:** High-level adımlar
- **Eksik Bilgiler:** Netleşmesi gereken sorular

Parametreler: `BlockedOnUser: true`, `PathsToReview: [ilgili dosyalar]`

> Onay almadan TEK BİR SATIR kod yazılmaz.

---

## FAZ III: UYGULAMA (Sadece Onay Sonrası)

Onay alındıktan sonra:
- Plandan sapma
- Temiz, okunabilir, DRY kod
- Performans + güvenlik öncelikli
- Gereksiz abstraction'dan kaçın
- Test + örnek kullanım ekle (gerekirse)
- Determinizm ve idempotency garanti et

---

## FAZ IV: TESLİMAT & GERİ BİLDİRİM

- Yapılanların özeti
- Değişen dosyalar + SSOT güncellemeleri
- Monitoring/logging notları
- İyileştirme alanları
- Sonraki adım önerileri