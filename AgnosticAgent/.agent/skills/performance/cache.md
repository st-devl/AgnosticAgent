# Cache Stratejisi

## Cache Katmanları

```
┌─────────────────────┐
│ Application Cache   │ ← In-memory (fastest)
├─────────────────────┤
│ Distributed Cache   │ ← Redis/Memcached
├─────────────────────┤
│ CDN Cache          │ ← Static assets
├─────────────────────┤
│ Database           │ ← Son başvuru
└─────────────────────┘
```

## Cache Pattern'leri

| Pattern | Ne Zaman | Örnek |
|---------|----------|-------|
| **Cache-Aside** | Read-heavy | User profile |
| **Write-Through** | Consistency önemli | Settings |
| **Write-Behind** | High write throughput | Analytics |
| **Cache Stampede Prevention** | Popular keys | Homepage data |

## Cache Key Formatı

```
{prefix}:{tenant}:{entity}:{id}:{version}

Örnekler:
app:tenant_123:user:456:v1
app:tenant_123:order_list:page_1:v2
```

## Cache Invalidation

```
✅ DOĞRU: Event-driven invalidation
OrderCreated → Cache::forget('orders_*')

❌ YANLIŞ: Her yerde manuel
$order = Order::create($data);
Cache::forget('orders'); // Unutulabilir
```

## TTL Stratejisi

| Veri Tipi | TTL | Neden |
|-----------|-----|-------|
| User session | 30 dakika | Güvenlik |
| Config/Settings | 1 saat | Nadiren değişir |
| Dashboard stats | 5 dakika | Fresh olmalı |
| Product catalog | 15 dakika | Orta değişim |
| Static content | 24 saat | Çok nadiren |
