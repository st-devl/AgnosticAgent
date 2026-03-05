---
description: db_audit - Database modeli, ilişkiler, index, gereksiz query, cache/redis doğrulama
---

# Database Audit Workflow

## Amaç
Veritabanı yapısını, performansını ve cache stratejisini denetlemek.

## İlgili Skill'ler
- `database-architecture/` - Schema, index, migration kuralları
- `performance/cache.md` - Cache stratejisi

## Adımlar

### 0. Otomatik Şema Analizi (Hibrit Güç)
// turbo
İlk olarak aşağıdaki scripti çalıştır:
```bash
python3 .agent/skills/database-architecture/scripts/schema_inspector.py
```
JSON çıktısını incele ve veritabanı yapısını anla.

### 1. Tarama Kapsamı
- Migration dosyaları
- Model dosyaları
- Repository/Service katmanları
- Cache/Redis kullanımları

### 2. Kontrol Listesi

#### Tablo Sorumlulukları
- [ ] Her tablo tek bir sorumluluk taşıyor mu?
- [ ] Gereksiz/tekrar eden tablo var mı?
- [ ] Tablo isimlendirmesi tutarlı mı?

#### İlişkiler (FK)
- [ ] Foreign key'ler doğru tanımlı mı?
- [ ] Cascade kuralları uygun mu?
- [ ] Orphan kayıt riski var mı?

#### Index Kontrolü
- [ ] Sık sorgulanan alanlarda index var mı?
- [ ] Gereksiz index var mı?
- [ ] Composite index gerekli mi?

#### Query Performansı
- [ ] N+1 sorunu var mı?
- [ ] Gereksiz SELECT * kullanımı var mı?
- [ ] Eager loading uygun kullanılıyor mu?

#### Cache Stratejisi
- [ ] Cache key yapısı tutarlı mı?
- [ ] TTL değerleri uygun mu?
- [ ] Cache invalidation stratejisi var mı?

### 3. Sonuç Raporu

```markdown
## Özet
[1-2 cümle]

## Bulgular
| Kategori | Seviye | Açıklama |
|----------|--------|----------|

## Performans Riskleri
- ...

## Optimizasyon Önerileri
- ...

## Hemen Yapılacaklar
- [ ] ...
```
