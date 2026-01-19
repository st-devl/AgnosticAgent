---
trigger: always_on
---

# Error Handling Standartları

> Tüm error response'ları bu formata uymalı.

## 🚨 Standart Error Format
```json
{
  "error": {
    "code": "ERROR_CODE_CONSTANT",
    "message": "Human-readable error message",
    "field_errors": [
      {
        "field": "field.path.name",
        "error": "error_type",
        "message": "Field-specific error message"
      }
    ],
    "metadata": {
      "request_id": "uuid-v4",
      "timestamp": "ISO 8601 datetime",
      "docs_url": "https://docs.example.com/errors/ERROR_CODE"
    }
  }
}
```

## 📋 Error Code Kategorileri

### VALIDATION_* (400)
```
VALIDATION_REQUIRED_FIELD
VALIDATION_INVALID_TYPE
VALIDATION_OUT_OF_RANGE
VALIDATION_INVALID_FORMAT
VALIDATION_INVALID_ENUM
```

### AUTH_* (401)
```
AUTH_TOKEN_MISSING
AUTH_TOKEN_INVALID
AUTH_TOKEN_EXPIRED
AUTH_CREDENTIALS_INVALID
```

### PERMISSION_* (403)
```
PERMISSION_DENIED
PERMISSION_INSUFFICIENT_ROLE
PERMISSION_RESOURCE_FORBIDDEN
```

### RESOURCE_* (404)
```
RESOURCE_NOT_FOUND
RESOURCE_DELETED
```

### CONFLICT_* (409)
```
CONFLICT_DUPLICATE
CONFLICT_STATE_INVALID
CONFLICT_VERSION_MISMATCH
```

### BUSINESS_* (422)
```
BUSINESS_RULE_VIOLATED
BUSINESS_QUOTA_EXCEEDED
BUSINESS_OPERATION_INVALID
```

### SERVER_* (500)
```
SERVER_INTERNAL_ERROR
SERVER_SERVICE_UNAVAILABLE
SERVER_TIMEOUT
```

## 🎯 Error Response Örnekleri

### Validation Error (400)
```json
{
  "error": {
    "code": "VALIDATION_REQUIRED_FIELD",
    "message": "Validation failed for required fields",
    "field_errors": [
      {
        "field": "email",
        "error": "required",
        "message": "Email is required"
      },
      {
        "field": "amount",
        "error": "out_of_range",
        "message": "Amount must be between 10 and 10000"
      }
    ],
    "metadata": {
      "request_id": "550e8400-e29b-41d4-a716-446655440000",
      "timestamp": "2026-01-18T12:00:00Z"
    }
  }
}
```

### Auth Error (401)
```json
{
  "error": {
    "code": "AUTH_TOKEN_EXPIRED",
    "message": "Your session has expired. Please log in again.",
    "field_errors": [],
    "metadata": {
      "request_id": "550e8400-e29b-41d4-a716-446655440000",
      "timestamp": "2026-01-18T12:00:00Z",
      "docs_url": "https://docs.example.com/errors/AUTH_TOKEN_EXPIRED"
    }
  }
}
```

### Business Logic Error (422)
```json
{
  "error": {
    "code": "BUSINESS_QUOTA_EXCEEDED",
    "message": "You have reached your monthly donation limit",
    "field_errors": [],
    "metadata": {
      "request_id": "550e8400-e29b-41d4-a716-446655440000",
      "timestamp": "2026-01-18T12:00:00Z",
      "current_quota": 5000,
      "max_quota": 5000
    }
  }
}
```

## ✅ Frontend Error Handling Checklist

Frontend'de error handling yaparken:
```
✓ Error code'a göre categorize et
✓ field_errors'ı form field'larına map et
✓ message'ı kullanıcıya göster
✓ Retry stratejisi belirle (error type'a göre)
✓ request_id'yi log'la (support için)
✓ docs_url varsa kullanıcıya sun
```

## 🔄 Error State Management
```
Error state pattern:
{
  hasError: boolean,
  error: {
    code: string,
    message: string,
    fieldErrors: Map<fieldName, errorMessage>,
    metadata: object
  } | null
}

Clear error when:
- User edits field (clear that field's error)
- User retries operation (clear all errors)
- Success response received (clear all errors)
```

## 🚫 Yapılmaması Gerekenler

❌ Generic "Error occurred" mesajları
❌ Stack trace'i kullanıcıya gösterme
❌ Internal error detaylarını expose etme
❌ Farklı error formatları kullanma
❌ Error code olmadan error dönme
❌ field_errors'ı ignore etme