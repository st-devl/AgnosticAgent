# API Security

## Authentication Methods

| Yöntem | Kullanım |
|--------|----------|
| JWT | Web/Mobile apps |
| API Key | Server-to-server |
| OAuth 2.0 | 3rd party integrations |

## API Key Management

```json
{
  "key": "ak_live_xxxxx",
  "tenant_id": "...",
  "permissions": ["orders.read", "orders.write"],
  "expires_at": "2025-01-01",
  "last_used_at": "2024-06-15"
}
```

## Request Validation

```
// Input sanitization
- required fields check
- type validation
- length limits
- regex patterns

// Rate limiting
- Per IP: 60/min
- Per API Key: 1000/min
- Per Tenant: 10000/min
```

## Security Headers

```
Content-Security-Policy: default-src 'self'
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000
X-XSS-Protection: 1; mode=block
```

## API Security Checklist

- [ ] Authentication required?
- [ ] Authorization checked?
- [ ] Input validated?
- [ ] Rate limiting enabled?
- [ ] Security headers set?
- [ ] Errors don't leak info?
