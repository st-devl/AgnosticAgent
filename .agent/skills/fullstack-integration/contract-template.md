# Kontrat Şablonları

> Bu dosya referans amaçlıdır. SKILL.md'den yönlendirilir.

---

## 🚀 HIZLI BAŞLANGIÇ (Kontrat Nasıl Oluşturulur?)

### Adım 1: İşlem Tipini Belirle ve Şablon Seç

| İşlem Tipi | Kullanılacak Şablon |
|------------|---------------------|
| **CRUD** (Create/Read/Update/Delete) | [Temel Kontrat Şablonu](#📋-temel-kontrat-şablonu) ↓ |
| **Liste/Filtreleme** | [Liste Operasyonu Şablonu](#📊-liste-operasyonu-şablonu) ↓ |
| **Authentication** | [Auth Example](examples/auth-example.json) |

**Detaylı örnekler:**
- CRUD: `examples/crud-example.json`
- Liste: `examples/list-example.json`
- Auth: `examples/auth-example.json`

---

### Adım 2: Şablonu Doldur

**Değiştirmen gerekenler:**
```json
{
  "operation": "[verb]_[entity]",  // ← snake_case: create_donation, list_campaigns
  "version": "1.0.0",              // ← İlk versiyon her zaman 1.0.0
  "description": "[ne yapar]",     // ← Türkçe açıklama
  
  "input": {
    "fields": [
      {
        "name": "[field_name]",    // ← snake_case: user_email, campaign_id
        "type": "string|number|boolean|object|array",
        "required": true/false,
        "validation": {
          "rules": {},             // ← min, max, pattern, enum vb.
          "error_message": "[Türkçe mesaj]"
        },
        "description": "[açıklama]",
        "example": "[örnek değer]"
      }
    ]
  },
  
  "output": {
    "success": {
      "type": "object|array",
      "schema": {},
      "example": {}
    },
    "errors": "Bkz: .agent/rules/error-handling.md"
  },
  
  "metadata": {
    "auth_required": true/false,
    "permissions": ["resource:action"],  // ← Örn: donation:create
    "idempotent": true/false,
    "cacheable": true/false,
    "http": {
      "method": "GET|POST|PUT|PATCH|DELETE",
      "path": "/api/v1/[resource]"
    }
  }
}
```

---

### Adım 3: Doğrula

Kontratı oluşturduktan sonra kontrol et:
```
✓ Naming convention → snake_case mi?
✓ Error format → .agent/rules/error-handling.md'ye uygun mu?
✓ Validation rules → açık ve net mi?
✓ Breaking change → mevcut kontratla çakışıyor mu?
```

**Referanslar:**
- Naming & Version: `.agent/rules/contract-standards.md`
- Error format: `.agent/rules/error-handling.md`

---

### Adım 4: Kaydet

Kontratı şu yapıda kaydet:
```
contracts/
└── [domain]/              # Örn: donations, campaigns, users
    └── [entity]/          # Örn: donation, campaign, user
        └── v[version]/    # Örn: v1.0.0
            └── contract.json
```

**Örnek:**
```
contracts/donations/donation/v1.0.0/contract.json
```

**Son adım:**
- `contracts/registry.json` dosyasını güncelle
- Kullanıcıya kontratı göster ve onayla

---

## 📋 Temel Kontrat Şablonu
```json
{
  "operation": "[operation_name]",
  "version": "1.0.0",
  "description": "[ne yapar - Türkçe]",
  
  "input": {
    "fields": [
      {
        "name": "[field_name]",
        "type": "string|number|boolean|object|array",
        "required": true,
        "validation": {
          "rules": {
            "min_length": 3,
            "max_length": 100,
            "pattern": "^[a-zA-Z0-9\\s-_]+$"
          },
          "error_message": "[Türkçe mesaj]"
        },
        "description": "[açıklama]",
        "example": "[örnek değer]"
      }
    ]
  },
  
  "output": {
    "success": {
      "type": "object",
      "schema": {
        "id": {
          "type": "string",
          "description": "[açıklama]",
          "example": "resource_abc123"
        },
        "created_at": {
          "type": "string",
          "format": "iso8601",
          "example": "2026-01-19T12:00:00Z"
        }
      },
      "description": "Başarılı yanıt"
    },
    "errors": {
      "validation": "Bkz: .agent/rules/error-handling.md",
      "auth": "Bkz: .agent/rules/error-handling.md",
      "business": "Bkz: .agent/rules/error-handling.md"
    }
  },
  
  "metadata": {
    "auth_required": true,
    "permissions": ["resource:create"],
    "rate_limit": "100/hour",
    "idempotent": true,
    "cacheable": false,
    "http": {
      "method": "POST",
      "path": "/api/v1/resources",
      "headers": {
        "required": ["Authorization", "Content-Type"],
        "optional": ["X-Idempotency-Key"]
      }
    }
  }
}
```

---

## 🔗 HTTP API Şablonu
```
Method: [GET|POST|PUT|PATCH|DELETE]
Path: /api/v1/[resource]/{id}

Headers:
  Required:
    - Authorization: Bearer {token}
    - Content-Type: application/json
  Optional:
    - X-Request-ID: {uuid}

Query Parameters: (GET/filtering için)
  - page: number (default: 1)
  - limit: number (default: 20, max: 100)
  - sort_by: string
  - sort_order: asc|desc

Request Body:
  {input schema reference}

Response Codes:
  200/201: {success schema}
  400: validation error (Bkz: error-handling.md)
  401: auth error (Bkz: error-handling.md)
  403: permission error (Bkz: error-handling.md)
  404: not found
  409: conflict
  422: business logic error
  500: server error
```

---

## 📊 Liste Operasyonu Şablonu
```json
{
  "operation": "list_[entities]",
  "version": "1.0.0",
  "description": "[Entities] listeler",
  
  "input": {
    "fields": [
      {
        "name": "page",
        "type": "number",
        "required": false,
        "validation": {
          "rules": { "min": 1, "integer": true },
          "error_message": "Sayfa numarası 1'den büyük olmalı"
        },
        "default": 1
      },
      {
        "name": "limit",
        "type": "number",
        "required": false,
        "validation": {
          "rules": { "min": 1, "max": 100, "integer": true },
          "error_message": "Limit 1-100 arası olmalı"
        },
        "default": 20
      },
      {
        "name": "sort_by",
        "type": "string",
        "required": false,
        "validation": {
          "rules": { "enum": ["created_at", "name", "updated_at"] }
        },
        "default": "created_at"
      },
      {
        "name": "sort_order",
        "type": "string",
        "required": false,
        "validation": {
          "rules": { "enum": ["asc", "desc"] }
        },
        "default": "desc"
      }
    ]
  },
  
  "output": {
    "success": {
      "type": "object",
      "schema": {
        "data": {
          "type": "array",
          "description": "Liste verileri"
        },
        "pagination": {
          "total": "number - Toplam kayıt",
          "page": "number - Mevcut sayfa",
          "limit": "number - Sayfa başı kayıt",
          "total_pages": "number - Toplam sayfa"
        },
        "meta": {
          "applied_filters": "object",
          "applied_sort": "object"
        }
      }
    }
  },
  
  "metadata": {
    "auth_required": true,
    "permissions": ["resource:list"],
    "cacheable": true,
    "http": {
      "method": "GET",
      "path": "/api/v1/resources"
    }
  }
}
```

---

## 📁 Kontrat Dosya Yolu

Kontratlar şu yapıda saklanır:
```
contracts/
  └── [domain]/
      └── [entity]/
          └── v[version]/
              ├── contract.json
              ├── types.generated.*
              ├── validators.generated.*
              └── mocks.generated.*
```

---

## 🔍 Örnekler

Detaylı örnekler için:
- `.agent/skills/fullstack-integration/examples/crud-example.json`
- `.agent/skills/fullstack-integration/examples/list-example.json`
- `.agent/skills/fullstack-integration/examples/auth-example.json`