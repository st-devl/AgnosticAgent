# Data Encryption

## At Rest Encryption

| Veri Tipi | Encryption | Key Management |
|-----------|------------|----------------|
| Database | AES-256 | KMS / Vault |
| Files | AES-256 | Per-tenant key |
| Backups | AES-256 | Separate key |

## In Transit Encryption

- TLS 1.3 zorunlu
- HTTP → HTTPS redirect
- HSTS enabled
- Certificate pinning (mobile)

## Sensitive Data Handling

```
❌ Plain text
user.ssn = '123-45-6789'

✅ Encrypted
user.ssn = encrypt('123-45-6789')

✅ Hashed (one-way)
user.password = hash('password')
```

## Key Management

| Tip | Rotation | Storage |
|-----|----------|---------|
| Encryption keys | 1 yıl | HSM/KMS |
| API keys | 90 gün | Encrypted vault |
| Session secrets | Her deploy | Environment |

## Encryption Checklist

- [ ] Sensitive data encrypted at rest mi?
- [ ] TLS 1.2+ kullanılıyor mu?
- [ ] Key rotation policy var mı?
- [ ] Encryption key'ler güvenli mi?
