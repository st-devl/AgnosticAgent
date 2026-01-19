# Index Stratejisi

## Index Tipleri ve Kullanımı

| Tip | Ne Zaman | Örnek |
|-----|----------|-------|
| **B-Tree (default)** | Equality, range | `WHERE status = 'active'` |
| **Composite** | Çoklu kolon | `WHERE tenant_id = ? AND status = ?` |
| **Partial** | Koşullu veri | `WHERE deleted_at IS NULL` |
| **Covering** | Select optimizasyonu | Tüm kolonlar index'te |
| **Full-text** | Metin arama | `MATCH(title) AGAINST(?)` |

## Composite Index Sıralaması (KRİTİK)

```sql
-- ✅ DOĞRU SIRA: Selectivity yüksek → düşük
INDEX idx_orders (tenant_id, status, created_at)
-- tenant_id: çok seçici
-- status: orta seçici  
-- created_at: range query için son

-- ❌ YANLIŞ SIRA
INDEX idx_orders (created_at, status, tenant_id)
```

## Gereksiz Index Tespiti

```sql
-- Kullanılmayan index'leri bul
SELECT indexrelname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0;
```

## Index Checklist

- [ ] Sık kullanılan WHERE kolonları indexli mi?
- [ ] Composite index sırası doğru mu?
- [ ] Kullanılmayan index var mı?
- [ ] FK'lar indexli mi?
- [ ] Unique constraint'ler var mı?
