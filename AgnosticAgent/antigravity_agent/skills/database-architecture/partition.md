# Partition Stratejisi

## Ne Zaman Partition?

| Durum | Partition Tipi |
|-------|----------------|
| Tablo > 10M satır | Range (tarih bazlı) |
| Tarih bazlı query | Range (monthly/yearly) |
| Tenant izolasyonu | List (tenant_id) |
| Uniform dağılım | Hash |

## Range Partition Örneği

```sql
-- Aylık partition
CREATE TABLE orders (
    id BIGINT,
    tenant_id BIGINT,
    created_at TIMESTAMP,
    ...
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2024_01 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

## Data Archiving

| Veri Tipi | Retention | Archive Yöntemi |
|-----------|-----------|-----------------| 
| Transaction logs | 90 gün | Cold storage'a taşı |
| Audit logs | 1 yıl | Ayrı tablo/DB |
| Soft deleted | 30 gün | Hard delete |
| Analytics | 2 yıl | Aggregated tabloya |

## Partition Checklist

- [ ] Tablo boyutu partition gerektiriyor mu?
- [ ] Partition key doğru seçildi mi?
- [ ] Eski partition'lar archive ediliyor mu?
- [ ] Query'ler partition'dan faydalanıyor mu?
