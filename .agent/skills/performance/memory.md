# Memory Yönetimi

## Memory Leak Önleme

```
❌ Static array birikimi
class Service:
    cache = []  # Her istekte büyür

❌ Unbounded collection
results = []
for item in huge_dataset:
    results.append(process(item))  # Memory 💥

✅ Generator kullan
def process_items(items):
    for item in items:
        yield process(item)
```

## Memory Limitleri

| Context | Limit | Aksiyon |
|---------|-------|---------| 
| Web request | 128MB | Optimize et |
| Queue job | 256MB | Chunking |
| CLI command | 512MB | Generator |

## Batch Processing

```
❌ Memory killer
users = User.all()  # 1M kayıt = 💥

✅ Chunking
User.chunk(1000, lambda users:
    for user in users:
        # Process
)

✅ Lazy Collection
for user in User.lazy():
    # Tek tek işle, memory yok
```

## Memory Checklist

- [ ] Large collection'lar chunk ediliyor mu?
- [ ] Static değişkenlerde birikim var mı?
- [ ] Unbounded array'ler var mı?
- [ ] File processing stream kullanıyor mu?
