# API Performansı

## Response Optimizasyonu

```
✅ Sadece gerekli alanlar
return user.only(['id', 'name', 'email'])

✅ Pagination zorunlu
return Order.paginate(20)

✅ Resource transformation
return UserResource.collection(users)
```

## Rate Limiting

```
// Tenant-aware rate limit
RateLimiter.for('api', lambda request:
    [
        Limit.perMinute(60).by(request.ip),
        Limit.perMinute(1000).by(request.tenant.id),
    ]
)
```

## Response Guidelines

| Metrik | Hedef |
|--------|-------|
| JSON size | < 100 KB |
| Items per page | 20-50 |
| Nested depth | Max 3 |
| Fields per object | Max 20 |

## API Checklist

- [ ] Pagination var mı?
- [ ] Rate limiting var mı?
- [ ] Response size optimize mi?
- [ ] N+1 query yok mu?
- [ ] Gzip/compression aktif mi?
