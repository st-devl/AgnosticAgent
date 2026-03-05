# Project Registry

> Bu dosya projedeki tüm component'ları, API endpoint'leri ve kontratları takip eder.
> Yeni component/endpoint eklemeden önce burayı kontrol edin (duplicate önleme).

---

## 📋 İçindekiler

- [Frontend Components](#frontend-components)
- [Backend Modules](#backend-modules)
- [API Endpoints](#api-endpoints)
- [API Contracts](#api-contracts)
- [Layouts / Templates](#layouts--templates)
- [Shared Utilities](#shared-utilities)
- [Component Kuralları](#component-kuralları)

---

## Frontend Components

| Component | Dosya | Props/Params | Amaç | Kontrat Bağlantısı |
|-----------|-------|--------------|------|--------------------|
| ... | ... | ... | ... | ... |

---

## Backend Modules

| Modül | Dosya | Amaç | İlgili Kontratlar |
|-------|-------|------|-------------------|
| ... | ... | ... | ... |

---

## API Endpoints

> **Not**: Detaylı kontratlar için `contracts/` klasörüne veya [API Contracts](#api-contracts) bölümüne bakın.

| Endpoint | Method | Kontrat | Auth | Permissions | Dosya | Amaç |
|----------|--------|---------|------|-------------|-------|------|
| ... | GET/POST/... | [`operation@version`](../contracts/...) | ✅/❌ | `permission:action` | ... | ... |

### Örnek Satır:
```markdown
| `/api/v1/donations` | POST | [`create_donation@v1.0.0`](../contracts/donations/donation/v1.0.0/contract.json) | ✅ | `donation:create` | `app/Controllers/DonationController.php` | Yeni bağış oluşturur |
```

---

## API Contracts

> Tüm API kontratları `contracts/` klasöründe versiyonlanarak saklanır.
> Bu tablo hızlı referans içindir. Detaylı kontrat bilgisi için dosya linklerine tıklayın.

### Aktif Kontratlar

| Operation | Domain | Latest Stable | Latest Beta | Status | Kontrat Dosyası |
|-----------|--------|---------------|-------------|--------|-----------------|
| ... | ... | v1.0.0 | - | ✅ Stable | [contract.json](../contracts/...) |

### Örnek Satır:
```markdown
| `create_donation` | donations | v1.0.0 | v2.0.0 | ✅ Stable | [v1.0.0](../contracts/donations/donation/v1.0.0/contract.json) |
```

### Deprecated Kontratlar

| Operation | Deprecated Version | Sunset Date | Replacement | Migration Guide |
|-----------|-------------------|-------------|-------------|-----------------|
| ... | v1.0.0 | 2026-06-01 | v2.0.0 | [MIGRATION.md](../MIGRATION_v1_to_v2.md) |

---

## Layouts / Templates

| Layout | Dosya | Amaç |
|--------|-------|------|
| ... | ... | ... |

---

## Shared Utilities

| Utility | Dosya | Amaç |
|---------|-------|------|
| ... | ... | ... |

---

## Component Kuralları

### 1. DRY (Don't Repeat Yourself)
- Aynı işi yapan iki component olamaz
- Yeni component eklemeden önce mevcut olanları kontrol et
- Benzer işlevsellik varsa extend et, yeniden yazma

### 2. Tek Sorumluluk
- Her component/modül tek bir iş yapar
- Component adı işlevi açıkça belirtmeli

### 3. Kayıt Zorunluluğu
- **Yeni component** = bu dosyaya kayıt
- **Yeni API endpoint** = bu dosyaya kayıt + kontrat oluştur
- **Kontrat değişikliği** = bu dosyayı güncelle

### 4. İsimlendirme
- Projenin naming convention'ına uygun (kebab-case, PascalCase, vb.)
- API endpoint'leri: RESTful convention (`/api/v1/resources`)
- Kontratlar: snake_case operation adları (`create_resource`)

### 5. Kontrat-First Yaklaşım (API için)
- Yeni API endpoint'i eklemeden **ÖNCE** kontrat oluştur
- Kontrat `contracts/` klasörüne kaydet
- Bu dosyaya kontrat linki ile kaydet

### 6. Versiyonlama (API için)
- Tüm API kontratları versiyonlanır (semver: MAJOR.MINOR.PATCH)
- Breaking change = MAJOR version bump
- Deprecated endpoint'leri bu dosyada işaretle
- Sunset date ve migration guide belirt

---

## Teknolojiye Özel Bölümler

> Projenizin kullandığı teknolojilere göre aşağıdaki bölümleri ekleyin/kaldırın.

### React/Vue/Angular Projeleri İçin

#### UI Components
| Component | Path | Props | State | Kontrat Bağlantısı |
|-----------|------|-------|-------|-------------------|
| ... | ... | ... | ... | ... |

#### Hooks / Composables
| Hook/Composable | Path | Amaç | Kullandığı API |
|-----------------|------|------|----------------|
| ... | ... | ... | [`operation@version`](../contracts/...) |

---

### Laravel/PHP Projeleri İçin

#### Controllers
| Controller | Path | Methods | İlgili Kontratlar |
|------------|------|---------|-------------------|
| ... | ... | ... | ... |

#### Livewire Components
| Component | Path | Amaç | İlgili API |
|-----------|------|------|-----------|
| ... | ... | ... | ... |

---

### Python/FastAPI Projeleri İçin

#### Routers
| Router | Path | Endpoints | İlgili Kontratlar |
|--------|------|-----------|-------------------|
| ... | ... | ... | ... |

#### Schemas (Pydantic)
| Schema | Path | Kontrat Referansı |
|--------|------|-------------------|
| ... | ... | [`operation@version`](../contracts/...) |

---

### Node.js/Express Projeleri İçin

#### Routes
| Route File | Path | Endpoints | İlgili Kontratlar |
|------------|------|-----------|-------------------|
| ... | ... | ... | ... |

#### Controllers
| Controller | Path | Methods | İlgili Kontratlar |
|------------|------|---------|-------------------|
| ... | ... | ... | ... |

---

## Nasıl Kullanılır?

### Yeni Component Eklerken

1. **Önce burayı kontrol et** (benzer component var mı?)
2. Component'i oluştur
3. Bu dosyaya kaydet:
```markdown
   | ComponentName | path/to/component | Props | Açıklama | - |
```

### Yeni API Endpoint Eklerken

1. **Önce kontrat oluştur**: `contracts/{domain}/{entity}/v{version}/contract.json`
2. **Backend'i yaz** (kontrata uygun)
3. **Frontend'i yaz** (kontratı referans al)
4. **Bu dosyaya kaydet**:
```markdown
   | `/api/v1/resource` | POST | [`create_resource@v1.0.0`](../contracts/...) | ✅ | `resource:create` | path/to/controller | Açıklama |
```

### Kontrat Güncellerken

1. **Breaking change mi?** → Yeni versiyon oluştur
2. **Non-breaking mi?** → Mevcut versiyonu güncelle
3. **Bu dosyayı güncelle**:
   - Deprecated kontratları "Deprecated Kontratlar" tablosuna taşı
   - Yeni versiyonu "Aktif Kontratlar" tablosuna ekle

---

## Referanslar

- **Kontrat Registry**: [`contracts/registry.json`](../contracts/registry.json) - Merkezi kontrat indeksi
- **Kontrat Şablonları**: [`.agent/skills/fullstack-integration/contract-template.md`](../.agent/skills/fullstack-integration/contract-template.md)
- **Entegrasyon Kuralları**: [`.agent/rules/integration-checklist.md`](../.agent/rules/integration-checklist.md)
- **Changelog**: [`CHANGELOG.md`](../CHANGELOG.md) - Tüm değişiklik geçmişi

---

## Otomatik Güncellemeler

Bu dosya şu durumlarda **manuel** güncellenir:
- ✅ Yeni component oluşturulduğunda
- ✅ Yeni API endpoint eklendiğinde
- ✅ Kontrat versiyonu değiştiğinde
- ✅ Endpoint deprecated edildiğinde

> **İpucu**: Bu dosyayı güncel tutmak için her PR'da gözden geçirin.