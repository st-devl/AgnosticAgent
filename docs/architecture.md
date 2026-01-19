# 🏗️ System Architecture (SSOT #2)

> ⚠️ **KİLİTLİ DOSYA:** Bu dosya mimari kararların tek kaynağıdır.
> Değişiklik için `/ultrathink` ile analiz + kullanıcı onayı gereklidir.

---

## Multi-Tenancy Model

### Karar: **Shared Database + tenant_id**

```
┌─────────────────────────────────────┐
│          Single Database            │
├─────────────────────────────────────┤
│  tenants (id, name, domain...)      │
│  users (id, tenant_id, ...)         │
│  donations (id, tenant_id, ...)     │
│  donation_types (id, tenant_id, ...)│
└─────────────────────────────────────┘
```

**Neden:**
- 10-50 tenant için optimal
- Migration basit
- Backup kolay
- Index ile performans

---

## Payment Architecture

### Karar: **Provider Plugin Pattern**

```php
interface PaymentProviderInterface {
    public function createPayment(PaymentRequest $req): PaymentResult;
    public function handleWebhook(array $payload): void;
    public function supportsRecurring(): bool;
    public function getCapabilities(): array;
}
```

**Provider'lar:**
- Payfast (primary)
- Stripe, Iyzico (gelecek)

**Kural:** Yeni provider = Interface implement + config ekle (1 gün max)

---

## Donation Types

| Tip | Açıklama | Recurring? |
|-----|----------|------------|
| **Fixed** | Sabit tutar bağış | ❌ |
| **Subscription** | 12 ay abonelik | ✅ |
| **Custom** | Serbest tutar | ❌ |
| **Collective** | Progress bar'lı ortak | ❌ |

---

## Locale & Currency Management

### Karar: **Session-Based Global State**

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Request   │ -> │   Session   │ -> │   Redis     │
│ (locale,    │    │ (locale,    │    │ tenant:*    │
│  currency)  │    │  currency)  │    │ :settings   │
└─────────────┘    └─────────────┘    └─────────────┘
```

**Diller:** TR, EN
**Para Birimleri:** USD (base), EUR, TRY, PKR, GBP
**Cache TTL:** 1 saat

---

## 48-Hour Donation Link

### Karar: **Signed Token + Single Use**

```
Token: {uuid}.{hmac_signature}
Expire: created_at + 48h
Single-use: used_at IS NOT NULL → rejected
Rate limit: 5 link/saat/IP
Audit: donations_links tablosu
```

**Güvenlik:** Link'te sadece token, diğer bilgiler DB'de.

---

## PCI-DSS Compliance

### Karar: **Kart Bilgisi ASLA Tutulmaz**

```
❌ card_number
❌ cvv
❌ expiry_date

✅ payment_token (provider'dan)
✅ last_4_digits (görüntüleme için)
✅ card_brand (Visa, Mastercard)
```

---

## Feature Flags (Per Tenant)

### Karar: **Kapabilite Tablosu**

```sql
CREATE TABLE tenant_capabilities (
    tenant_id BIGINT,
    capability VARCHAR(50),  -- 'recurring_payments', 'export_excel'
    enabled BOOLEAN,
    provider VARCHAR(50)     -- NULL or 'stripe', 'payfast'
);
```

**Kullanım:**
```php
if ($tenant->hasCapability('recurring_payments')) {
    // Show subscription option
}
```

---

## Export & Background Jobs

### Karar: **Laravel Queue + Horizon**

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Request   │ -> │   Redis     │ -> │   Horizon   │
│ (export)    │    │   Queue     │    │   Worker    │
└─────────────┘    └─────────────┘    └─────────────┘
                                            │
                                      ┌─────▼─────┐
                                      │  Storage  │
                                      │  (S3/DO)  │
                                      └───────────┘
```

**Retry:** 3 deneme, exponential backoff
**Chunk:** 1000 satır/batch

---

> **Son Güncelleme:** 2026-01-17
> **Karar Gerekçesi:** Bkz. `docs/decision_log.md`
