# Migration Best Practices

## Güvenli Migration Kuralları

| Kural | Açıklama |
|-------|----------|
| **Backward compatible** | Eski kod çalışmaya devam etmeli |
| **down() zorunlu** | Rollback her zaman mümkün |
| **Küçük adımlar** | Büyük değişiklik = çok migration |
| **Lock-free** | ALTER TABLE dikkat (büyük tablolar) |

## Riskli Operasyonlar

```
⚠️ DİKKAT: Büyük tabloda uzun sürer, lock oluşturur
- ALTER TABLE ... ADD INDEX
- ALTER TABLE ... MODIFY COLUMN

✅ Alternatif: CONCURRENT index (database destekliyorsa)
CREATE INDEX CONCURRENTLY idx_status ON orders(status)
```

## Zero-Downtime Migration

```
1. Yeni kolon ekle (nullable)
2. Kodu güncelle (hem eski hem yeni kolon)
3. Data migration (arka planda)
4. Eski kolonu kaldır (ayrı deployment)
```

## Migration Checklist

- [ ] down() metodu var mı?
- [ ] Staging'de test edildi mi?
- [ ] Lock süresi kabul edilebilir mi?
- [ ] Rollback planı var mı?
- [ ] Backup alındı mı?
