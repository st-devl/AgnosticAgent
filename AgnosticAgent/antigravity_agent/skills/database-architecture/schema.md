# Schema Design

## İsimlendirme Kuralları

```
-- Tablo: snake_case, çoğul
users, order_items, payment_transactions

-- Kolon: snake_case
first_name, created_at, tenant_id

-- Foreign Key: singular_table_id
user_id, order_id, payment_id

-- Index: idx_table_columns
idx_orders_tenant_status
idx_users_email
```

## İlişki Tipleri

| Tip | Örnek | FK Location |
|-----|-------|-------------|
| One-to-Many | User → Orders | orders.user_id |
| Many-to-Many | User ↔ Role | pivot table |
| One-to-One | User → Profile | profiles.user_id |

## Normalizasyon

| Form | Kural | Örnek |
|------|-------|-------|
| 1NF | Atomik değerler | Adres → street, city, zip |
| 2NF | Full functional dependency | |
| 3NF | No transitive dependency | |

> Denormalize sadece kanıtlanmış performans sorunu varsa!

## Schema Checklist

- [ ] Tablo isimleri çoğul mu?
- [ ] Kolon isimleri snake_case mi?
- [ ] FK'lar doğru isimlendi mi?
- [ ] NULL vs DEFAULT belirlendi mi?
- [ ] ON DELETE davranışı tanımlı mı?
