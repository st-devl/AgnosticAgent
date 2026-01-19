# Kontrat Şablonları

> Bu dosya referans amaçlıdır. SKILL.md'den yönlendirilir.

## 📋 Örnek Kontratlar (Full JSON)

Detaylı örnekleri aşağıdaki dosyalarda bulabilirsiniz:

- **CRUD (Create)**: `.agent/examples/contracts/crud-example.json`
- **List & Pagination**: `.agent/examples/contracts/list-example.json`
- **Authentication**: `.agent/examples/contracts/auth-example.json`

## 🔗 Temel Şema (İskelet)

```json
{
  "operation": "[verb]_[entity]",
  "version": "1.0.0",
  "description": "",
  "input": {
    "fields": []
  },
  "output": {
    "success": {},
    "errors": {
      "validation": "Bkz: .agent/rules/error-handling.md"
    }
  },
  "metadata": {
    "auth_required": true,
    "idempotent": false
  }
}
```

## 📂 Dosya Yolu Standardı

`contracts/[domain]/[entity]/v[version]/contract.json`