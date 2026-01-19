# Changelog

Tüm önemli değişiklikler bu dosyada dokümante edilir.

Format [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) standardına uygundur,
ve bu proje [Semantic Versioning](https://semver.org/spec/v2.0.0.html) kullanır.

---

## [Unreleased]

### Eklenen
- Backend-Frontend entegrasyon sistemi kuruldu
- Kontrat-bazlı geliştirme akışı oluşturuldu
- `.agent/skills/fullstack-integration/` skill'i eklendi
- `.agent/rules/` altında entegrasyon kuralları eklendi
- `.agent/workflows/` altında manuel workflow'lar eklendi

---

## [1.0.0] - 2026-01-19

### Eklenen
- İlk proje kurulumu
- Temel backend yapısı
- Temel frontend yapısı

---

## Nasıl Kullanılır?

### Yeni Feature Eklerken
```markdown
## [Unreleased]

### Eklenen
- [Feature adı]: [Kısa açıklama]
- API Endpoint: `POST /api/v1/...` - [Açıklama]

### Değiştirilen
- [Değişiklik]: [Açıklama]

### Düzeltilen
- [Bug]: [Açıklama]
```

### Breaking Change Eklerken
```markdown
## [2.0.0] - 2026-XX-XX

### ⚠️ BREAKING CHANGES

- **[Değişiklik adı]**: [Detaylı açıklama]
  - **Eski davranış**: ...
  - **Yeni davranış**: ...
  - **Migration**: Bkz: `MIGRATION_v1_to_v2.md`

### Eklenen
- [Yeni feature]

### Kaldırılan
- [Deprecated feature]
```

---

## Versiyon Kategorileri

- **[Unreleased]**: Henüz release edilmemiş değişiklikler
- **[X.Y.Z]**: Release edilmiş versiyonlar (en yeni üstte)

## Değişiklik Tipleri

- **Eklenen**: Yeni feature'lar
- **Değiştirilen**: Mevcut fonksiyonalitede değişiklikler
- **Deprecated**: Yakında kaldırılacak feature'lar
- **Kaldırılan**: Kaldırılan feature'lar
- **Düzeltilen**: Bug fix'ler
- **Güvenlik**: Güvenlik yamalarısı
- **⚠️ BREAKING CHANGES**: Geriye uyumsuz değişiklikler