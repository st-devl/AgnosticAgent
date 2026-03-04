---
name: component-architecture
version: "1.0.0"
requires: []
conflicts_with: []
description: |
  Use when: Designing reusable components, implementing database-driven configs,
  creating dynamic forms/modals, or applying DRY patterns.
  Keywords: component, modal, kart, form, reusable, props, DRY, composition pattern
allowed-tools: Read, Glob, Grep, Edit, Write (Subject to Gatekeeper)
---

# Component Architecture Skill

> 📌 Ortak kurallar için: `.agent/rules/common-rules.md`

## Amaç
Tekrar eden yapıları DRY prensibine uygun, merkezi yönetimli, performanslı componentlere dönüştürmek.

---

## 🎯 Temel Karar: Ne Zaman Component?

| Soru | Evet → | Hayır → |
|------|--------|---------|
| 2+ yerde kullanılıyor mu? | Component yap | Inline bırak |
| Varyasyonları var mı? | Props/Config ekle | Basit tut |
| Merkezi yönetim gerekli mi? | Database-driven | Hardcoded |
| Mantık karmaşık mı? | Composition pattern | Single component |

---

## 📊 Component Pattern Seçimi

### Pattern 1: Simple Props (Basit varyasyonlar)

**Ne zaman:** 5'ten az varyasyon, sadece görsel fark

```blade
<x-button variant="primary|secondary|danger" size="sm|md|lg">
    Kaydet
</x-button>
```

### Pattern 2: Database-Driven Config (Merkezi yönetim)

**Ne zaman:** Admin panelden yönetilecek, çok sayıda instance

```
Database (tek kaynak)
    │
    ├─ types tablosu
    │     ├─ id, type (enum)
    │     ├─ config (JSON)
    │     └─ is_active
    │
    ▼
Component (tek component, tüm varyasyonlar)
    │
    └─ <x-card :item="$item" />
```

**Database şeması:**
```php
Schema::create('card_types', function ($table) {
    $table->id();
    $table->string('type');           // Tip kategorisi
    $table->json('title');            // Çoklu dil
    $table->json('config');           // Tip'e özel ayarlar
    $table->json('form_fields');      // Dinamik form alanları
    $table->boolean('is_active');
    $table->integer('sort_order');
    $table->timestamps();
});
```

### Pattern 3: Composition (Karmaşık yapılar)

**Ne zaman:** 10+ prop gerekli, layout değişken

```blade
<x-card>
    <x-card.header>
        <x-card.title>{{ $title }}</x-card.title>
        <x-card.badge v-if="$badge">{{ $badge }}</x-card.badge>
    </x-card.header>
    <x-card.body>
        {{ $slot }}
    </x-card.body>
    <x-card.footer>
        <x-card.actions :actions="$actions" />
    </x-card.footer>
</x-card>
```

### Pattern 4: Dynamic Form Fields (Form varyasyonları)

**Ne zaman:** Aynı modal, farklı form alanları

```json
// Database: form_fields JSON
{
  "fields": [
    {"name": "email", "type": "email", "required": true, "label": "E-posta"},
    {"name": "amount", "type": "amount_selector", "required": true},
    {"name": "period", "type": "select", "options": ["weekly", "monthly"]}
  ]
}
```

```blade
{{-- Component: Dinamik render --}}
@foreach($formFields as $field)
    <x-dynamic-field :field="$field" />
@endforeach
```

---

## 🏗️ Merkezi Yönetim Mimarisi

### Yapı

```
┌─────────────────────────────────────────────────┐
│                  DATABASE                        │
│  (Tek kaynak - SSOT)                            │
│  ├─ Config, ayarlar, içerik                     │
│  └─ Cache ile optimize                          │
└───────────────────────┬─────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│               SERVICE LAYER                      │
│  - Cache yönetimi                               │
│  - Config parsing                               │
│  - Validation                                   │
└───────────────────────┬─────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│              COMPONENT LAYER                     │
│  - TEK component, tüm varyasyonlar              │
│  - Config'e göre render                         │
│  - Tip'e göre conditional logic                 │
└─────────────────────────────────────────────────┘
```

### Cache Stratejisi

> 📌 Detaylı cache kuralları için: `performance` (Skill) → `cache.md`

**Temel pattern:** `Cache::remember()` + invalidation on update

---

## 🔄 Modal + Dynamic Form Pattern

### Tek Modal, Dinamik Form

```blade
{{-- Layout'ta 1 kez --}}
<x-dynamic-modal />
```

```javascript
// Alpine.js
function dynamicModal() {
    return {
        isOpen: false,
        config: null,
        formFields: [],
        
        open(config) {
            this.config = config;
            this.formFields = config.form_fields || [];
            this.isOpen = true;
        },
        
        getComponent(fieldType) {
            const components = {
                'text': 'input-text',
                'email': 'input-email',
                'amount_selector': 'amount-selector',
                'period_selector': 'period-selector',
                'select': 'select-field'
            };
            return components[fieldType] || 'input-text';
        }
    }
}
```

---

## ✅ Component Checklist

### Yeni Component Oluştururken

- [ ] 2+ yerde kullanılacak mı? (Yoksa component yapma)
- [ ] Merkezi yönetim gerekli mi? (Evet → Database-driven)
- [ ] Prop sayısı < 10 mu? (Hayır → Composition)
- [ ] Form varyasyonu var mı? (Evet → Dynamic fields)
- [ ] Cache stratejisi belirlendi mi?
- [ ] `docs/registry.md`'ye eklendi mi?

### Anti-Patterns (YAPMA)

| ❌ Yapma | ✅ Yap |
|----------|--------|
| Her varyasyon için ayrı component | Tek component + config |
| Hardcoded içerik | Database'den çek |
| 15+ prop | Composition veya slots |
| if/else cehennemi | Strategy pattern |
| Her sayfada ayrı modal | Tek global modal |

---

## 📋 Config JSON Şablonları

> 📁 Detaylı şablonlar için: `docs/templates/component_config.md`

