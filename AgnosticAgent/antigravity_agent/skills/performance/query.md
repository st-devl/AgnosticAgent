# Query Optimizasyonu

## Lazy vs Eager Loading

```
// Lazy Loading - Sadece tek kayıt
$order = Order::find($id);
// İlişki gerektiğinde yüklenir

// Eager Loading - Liste/Döngü
$orders = Order::with(['user', 'items']).get();
// Tüm ilişkiler önceden yüklenir

// Lazy Eager Loading - Koşullu
$orders = Order::all();
if (includeUsers) {
    $orders.load('user');
}
```

## N+1 Problem Tespiti

```
❌ N+1 Problem
orders = Order.all()
for order in orders:
    print(order.user.name)  # Her order için ayrı query

✅ Eager Loading
orders = Order.with('user').get()
for order in orders:
    print(order.user.name)  # Tek query
```

## Query Complexity Kuralları

| Kural | Limit |
|-------|-------|
| Max JOIN | 4 tablo |
| Max subquery depth | 2 |
| Max result set | 1000 row (pagination zorunlu) |
| Max execution time | 5 saniye (timeout) |

## Slow Query Tespit

```sql
-- Log slow queries (> 1 saniye)
-- Database'e göre konfigürasyon değişir
```

## Query Checklist

- [ ] EXPLAIN çalıştırıldı mı?
- [ ] Index kullanılıyor mu?
- [ ] N+1 problemi yok mu?
- [ ] Pagination var mı?
- [ ] SELECT * yerine spesifik kolonlar mı?
