---
name: multi-tenancy
version: "1.0.0"
requires: [database-architecture]
conflicts_with: []
description: |
  Use when: Building multi-tenant SaaS, implementing tenant isolation, managing tenant lifecycle,
  or ensuring cross-tenant security.
  Keywords: tenant, multi-tenant, saas, tenant_id, izolasyon, multi-database
allowed-tools: Read, Glob, Grep, Edit (Subject to Gatekeeper)
---

# Multi-Tenancy Skill

## Amaç
Büyük çaplı SaaS projelerinde tenant izolasyonu, güvenlik ve performansı sağlamak.

---

## 🏗️ Tenant İzolasyon Stratejileri

### Strateji Seçim Tablosu

| Strateji | Ne Zaman Kullan | Avantaj | Dezavantaj |
|----------|-----------------|---------|------------|
| **Database per Tenant** | Yüksek izolasyon gerekli, az tenant | Tam izolasyon, kolay backup | Yönetim karmaşık, maliyet yüksek |
| **Schema per Tenant** | Orta izolasyon, orta tenant sayısı | İyi izolasyon, tek DB | Migration karmaşık |
| **Row-Level (tenant_id)** | Çok tenant, düşük maliyet | Basit, ölçeklenebilir | Query'lerde dikkat gerekli |

### Karar Ağacı

```
Tenant sayısı > 100?
    │
    ├─ EVET → Row-Level (tenant_id)
    │
    └─ HAYIR → Compliance gerekli mi?
                 │
                 ├─ EVET → Database per Tenant
                 │
                 └─ HAYIR → Schema per Tenant
```

---

## 🔒 Tenant İzolasyon Kuralları

### Zorunlu Kurallar

1. **Her tabloda `tenant_id`**
```sql
-- DOĞRU
CREATE TABLE orders (
    id BIGINT PRIMARY KEY,
    tenant_id BIGINT NOT NULL,  -- ZORUNLU
    ...
    INDEX idx_tenant_created (tenant_id, created_at)
);
```

2. **Global Scope YASAK**
```php
// ❌ YANLIŞ - Tüm tenant verileri
Order::all();

// ✅ DOĞRU - Sadece mevcut tenant
Order::where('tenant_id', tenant()->id)->get();

// ✅ EN İYİ - Otomatik scope
Order::all(); // Global scope tenant_id ekler
```

3. **Tenant Context Middleware**
```
Her request'te:
1. Tenant belirleme (subdomain, header, path)
2. Context'e tenant_id set etme
3. Database connection seçme (multi-db ise)
```

---

## 🛡️ Cross-Tenant Güvenlik

### Kontrol Listesi

- [ ] Tüm query'lerde tenant_id filtresi var mı?
- [ ] Route'larda tenant ownership kontrolü var mı?
- [ ] File upload'larda tenant path ayrımı var mı?
- [ ] Cache key'lerde tenant prefix var mı?
- [ ] Queue job'larında tenant context var mı?
- [ ] API response'larda tenant verisi sızmıyor mu?

### Cache Key Formatı

```
// ❌ YANLIŞ
cache()->get('user_123');

// ✅ DOĞRU
cache()->get("tenant_{$tenantId}_user_123");
```

### Queue Job Formatı

```php
class ProcessOrder implements ShouldQueue
{
    public $tenantId; // ZORUNLU

    public function handle()
    {
        tenancy()->initialize($this->tenantId);
        // İşlem...
    }
}
```

---

## 📊 Tenant Lifecycle

### Create Tenant

```
1. Tenant kaydı oluştur (central DB)
2. Tenant database/schema oluştur (multi-db ise)
3. Migration çalıştır
4. Seed data ekle (roller, ayarlar)
5. Admin kullanıcı oluştur
6. Domain/subdomain ayarla
```

### Suspend Tenant

```
1. Tenant status = suspended
2. Tüm session'ları sonlandır
3. Scheduled job'ları durdur
4. API erişimini kapat
5. Admin'e bildirim
```

### Delete Tenant (Dikkatli!)

```
1. Soft delete: status = deleted, 30 gün bekle
2. Data export (GDPR)
3. Hard delete: Tüm veriyi sil
4. File storage temizle
5. Cache temizle
6. Audit log tut
```

---

## 🚀 Performans Kuralları

### Index Stratejisi

```sql
-- Tenant-aware composite index (ZORUNLU)
INDEX idx_tenant_status_created (tenant_id, status, created_at)

-- Partial index (büyük tablolar için)
INDEX idx_active_orders ON orders (tenant_id, created_at)
    WHERE status = 'active'
```

### Query Kuralları

| Kural | Açıklama |
|-------|----------|
| `tenant_id` ilk sırada | WHERE clause'da ilk filtre |
| LIMIT zorunlu | Büyük sonuç setleri engelle |
| SELECT * yasak | Sadece gerekli kolonlar |
| Subquery dikkat | Cross-tenant risk |

---

## 🔧 Tenant Bazlı Özellikler

### Feature Flags

```php
if (tenant()->hasFeature('advanced_reporting')) {
    // Premium özellik
}
```

### Plan Limitleri

```php
if (tenant()->plan->maxUsers <= tenant()->users()->count()) {
    throw new PlanLimitExceeded();
}
```

### Tenant Config

```php
// Tenant-specific ayarlar
config(['mail.from.name' => tenant()->settings->company_name]);
```

---

## ✅ Checklist: Yeni Özellik Geliştirme

Her yeni özellikte kontrol et:

- [ ] Tenant_id tüm tablolarda var mı?
- [ ] Global scope tanımlı mı?
- [ ] Cache key'de tenant var mı?
- [ ] Queue job'da tenant context var mı?
- [ ] Test: Cross-tenant erişim engelli mi?
- [ ] Migration: Tüm tenant'lar için çalışıyor mu?
