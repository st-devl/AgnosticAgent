# Background Jobs

## Job Öncelikleri

| Queue | İçerik | Workers |
|-------|--------|---------|
| `high` | Payment, Auth | 10 |
| `default` | Email, Notification | 5 |
| `low` | Reports, Analytics | 2 |
| `tenant_{id}` | Tenant-specific | Dynamic |

## Tenant-Fair Scheduling

```
❌ Tek tenant queue'yu bloklar
dispatch(HeavyJob()).onQueue('default')

✅ Tenant-specific queue
dispatch(HeavyJob()).onQueue('tenant_' + tenant_id)

✅ Rate limiting per tenant
RateLimiter.for('jobs', lambda job:
    Limit.perMinute(100).by(job.tenant_id)
)
```

## Job Retry Stratejisi

```
class ProcessPayment:
    tries = 3
    backoff = [10, 60, 300]  # 10s, 1m, 5m
    timeout = 30
    
    def failed(self, exception):
        # Alert gönder
```

## Job Checklist

- [ ] Retry strategy belirlendi mi?
- [ ] Timeout ayarlandı mı?
- [ ] Failed handler var mı?
- [ ] Tenant-aware queue var mı?
- [ ] Rate limiting var mı?
