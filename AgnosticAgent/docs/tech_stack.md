# 🔧 Technology Stack (SSOT #1)

> ⚠️ **KİLİTLİ DOSYA:** Bu dosya teknoloji kararlarının tek kaynağıdır.
> Değişiklik için `/ultrathink` ile analiz + kullanıcı onayı gereklidir.

> [!CAUTION]
> **📌 ÖRNEK VERİ:** Aşağıdaki içerik referans amaçlı örnek veridir.
> Yeni proje başlatırken `/start` komutu ile `docs/templates/tech_stack_template.md`
> şablonu kullanılarak bu dosyanın üzerine yazılmalıdır.
---

## Backend Framework
- **Laravel 11** (PHP 8.3+)
- **Livewire 3** (reaktif UI)

## Admin Panel
- **Filament 3** (Laravel admin panel)

## Multi-Tenancy
- **stancl/tenancy** (Shared DB + tenant_id mode)

## Database
- **MySQL 8.0+** (production)
- **SQLite** (local development)

## Cache & Queue
- **Redis** (cache driver, 1 saat TTL)
- **Laravel Queue + Horizon** (job management)

## Authentication
- **Laravel Sanctum** (API tokens)
- **Spatie Permission** (RBAC)

## Media & Storage
- **Spatie Media Library** (file uploads)
- **AWS S3 / DigitalOcean Spaces** (production storage)

## Payment Gateway
- **PaymentProviderInterface** (plugin architecture)
- **Payfast** (primary - South Africa)
- Diğer provider'lar interface ile eklenebilir

## Localization
- **spatie/laravel-translatable** (model translations)
- **Session-based locale/currency** (TR, EN / USD, EUR, TRY, PKR, GBP)

## Frontend
- **Blade + Alpine.js** (server-rendered)
- **Tailwind CSS** (styling)

---

## 📦 Paket Listesi (Özet)

| Kategori | Paket |
|----------|-------|
| Tenancy | stancl/tenancy |
| Admin | filament/filament |
| Auth | laravel/sanctum, spatie/laravel-permission |
| Media | spatie/laravel-media-library |
| Translation | spatie/laravel-translatable |
| Queue | laravel/horizon |

---

> **Son Güncelleme:** 2026-01-17
> **Karar Gerekçesi:** Bkz. `docs/decision_log.md`
