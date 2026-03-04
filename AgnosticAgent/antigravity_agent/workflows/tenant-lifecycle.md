---
description: tenant-lifecycle - Yeni kiracı ekleme, güncelleme ve silme süreçleri
---

# 🏢 Tenant Lifecycle Workflow

> ⚠️ **GATEKEEPER:** Bu workflow kritik veri işlemleri içerir. Onay zorunlu.

> Bu workflow multi-tenant sistemlerde kiracı (tenant) yaşam döngüsünü yönetir.
> Framework-agnostik prensipler içerir.

---

## 📋 Tenant Oluşturma Checklist

### 1. Temel Bilgiler
- [ ] Tenant adı (unique)
- [ ] Subdomain veya domain
- [ ] Admin kullanıcı bilgileri
- [ ] Plan/paket seçimi

### 2. Database
- [ ] Tenant ID oluşturuldu
- [ ] Gerekli tablolar tenant_id ile ilişkilendirildi
- [ ] Seed data (varsayılan ayarlar) yüklendi

### 3. Branding
- [ ] Logo yüklendi
- [ ] Renk şeması ayarlandı
- [ ] Favicon oluşturuldu

### 4. Konfigürasyon
- [ ] Ödeme gateway ayarları
- [ ] E-posta ayarları
- [ ] Dil/locale ayarları

---

## 🔄 Tenant Güncelleme

### Güncellenebilir Alanlar
- Branding (logo, renkler)
- Plan/paket
- Domain/subdomain
- Admin kullanıcıları

### Dikkat Edilmesi Gerekenler
- Domain değişikliği DNS propagation gerektirir
- Plan downgrade'de veri kaybı riski

---

## 🗑️ Tenant Silme (Tehlikeli)

### Pre-Deletion Checklist
- [ ] Tüm aktif abonelikler iptal edildi
- [ ] Son 30 gün verisi yedeklendi
- [ ] Admin'e son uyarı e-postası gönderildi
- [ ] Legal retention süresi kontrol edildi

### Silme Süreci
1. Soft delete (is_active = false)
2. 30 gün bekleme süresi
3. Hard delete (veriler tamamen siliniyor)
4. Yedek arşive taşıma

---

## 🔐 Tenant İzolasyonu Prensipleri

### Veri İzolasyonu
- Her query `tenant_id` filtresi içermeli
- Global scope veya middleware ile otomatik filtreleme
- Cross-tenant erişim **imkansız** olmalı

### Kaynak İzolasyonu
- File storage tenant bazlı klasörleme
- Cache key'leri tenant prefix içermeli
- Queue job'ları tenant context taşımalı

---

## ✅ Doğrulama Noktaları

| Kontrol | Ne Zaman | Nasıl |
|---------|----------|-------|
| Tenant exists | Her request | Middleware |
| Tenant active | Her request | Middleware |
| Tenant owns resource | CRUD işlemlerinde | Policy/Guard |
| Cross-tenant leak | Code review | Manuel/Automated |

---

> **NOT:** Framework-spesifik implementasyon detayları proje dokümantasyonunda tanımlanır.
