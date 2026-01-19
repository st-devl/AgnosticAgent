---
description: scalability_check - Ölçeklenebilirlik hazırlığı ve horizontal scaling analizi
---

# Scalability Check Workflow

## Amaç
Uygulamanın yatay ölçeklenmeye hazır olup olmadığını analiz etmek.

## İlgili Skill'ler
- `performance/` - Cache, query, memory kuralları
- `database-architecture/partition.md` - Partition stratejisi

## Adımlar

### 1. Stateless Kontrolü

Her instance bağımsız çalışabilmeli:

| Kontrol | Durum | Aksiyon |
|---------|-------|---------|
| Session storage | Redis/DB mi? | File-based yasak |
| File uploads | Shared storage mi? | S3/GCS kullan |
| Cache | Distributed mi? | Redis zorunlu |
| Logs | Centralized mi? | ELK/CloudWatch |

### 2. Database Bottleneck

- [ ] Read replica kullanılabilir mi?
- [ ] Connection pooling ayarlı mı?
- [ ] Query'ler partition-friendly mi?
- [ ] N+1 problemi yok mu?

### 3. Cache Hit Ratio

```
Cache Hit Ratio = (Cache Hits / Total Requests) × 100

Hedef: > 90%
Kritik: < 80%
```

### 4. External Dependencies

| Servis | Risk | Çözüm |
|--------|------|-------|
| Payment Gateway | Rate limit | Queue + retry |
| Email Service | Slow | Async job |
| 3rd Party API | Downtime | Circuit breaker |

### 5. Load Test Gereksinimleri

| Metrik | Beklenen | Test Senaryosu |
|--------|----------|----------------|
| Concurrent users | 10x normal | Login storm |
| RPS | 5x normal | API flood |
| Response time | < 500ms | Under load |
| Error rate | < 1% | Peak traffic |

---

## Sonuç Raporu

```markdown
## Scalability Analiz Raporu

### Stateless Durumu
| Bileşen | Stateless | Aksiyon |
|---------|-----------|---------|

### Bottleneck Riskleri
1. ...

### Öneriler
- [ ] ...

### Scalability Skoru: X/10
```
