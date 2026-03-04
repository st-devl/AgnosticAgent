---
description: deep_bug_hunt - Hata kök neden analizi + tekrarını engelleme planı
---

# Deep Bug Hunt Workflow

## Amaç
Karmaşık hataları kök nedenine inerek çözmek ve tekrarını engellemek.

## İlgili Skill'ler
- `debugging` (Skill) - Debug stratejisi ve checklist

## Adımlar

### 1. Hata Tanımlama
- **Semptom**: Ne oluyor?
- **Nerede**: Hangi sayfa/endpoint/fonksiyon?
- **Ne zaman**: Sürekli mi, aralıklı mı?
- **Reproducible mı**: Adımlar neler?

### 2. Veri Toplama
- [ ] Log dosyaları
- [ ] Stack trace
- [ ] İlgili config dosyaları
- [ ] Son değişiklikler (git log)

### 3. Kök Neden Analizi

#### Soru Listesi
1. Hangi değişiklik tetikledi?
2. Hangi koşullarda oluyor?
3. Hangi koşullarda olmuyor?
4. Bağımlılık değişti mi?
5. Environment farkı var mı?

#### 5 Whys Tekniği
```
Neden 1: ...
  └─ Neden 2: ...
       └─ Neden 3: ...
            └─ Neden 4: ...
                 └─ Neden 5: [KÖK NEDEN]
```

### 4. Çözüm Planı

| Tip | Açıklama |
|-----|----------|
| **Minimal Fix** | Hemen uygulanacak geçici çözüm |
| **Kalıcı Fix** | Mimari/test/guard ile kalıcı çözüm |

### 5. Test Planı
- [ ] Bu hatayı yakalayacak unit test
- [ ] Regression test senaryoları
- [ ] Edge case'ler

### 6. Sonuç Raporu

```markdown
## Özet
[Hata ve çözüm özeti]

## Kök Neden
[Net açıklama]

## Çözüm
[Uygulanan fix]

## Tekrarlamama Garantisi
- [ ] Test eklendi
- [ ] Guard eklendi
- [ ] Dokümantasyon güncellendi
```
