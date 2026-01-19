# Audit Logging

## Log Edilecek Olaylar

| Kategori | Olaylar |
|----------|---------|
| **Auth** | Login, logout, failed login, password change |
| **Data** | Create, update, delete (sensitive data) |
| **Admin** | Role change, permission grant, user invite |
| **Billing** | Subscription change, payment |
| **Security** | Settings change, API key create |

## Audit Log Yapısı

```json
{
  "id": "uuid",
  "tenant_id": "...",
  "user_id": "...",
  "action": "order.created",
  "resource_type": "Order",
  "resource_id": "...",
  "old_values": {},
  "new_values": {"status": "pending"},
  "ip_address": "1.2.3.4",
  "user_agent": "...",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Retention Policy

| Log Tipi | Retention | Storage |
|----------|-----------|---------|
| Security events | 2 yıl | Cold storage |
| Data changes | 1 yıl | Archive |
| Access logs | 90 gün | Hot storage |

## Audit Checklist

- [ ] Tüm sensitive operasyonlar loglanıyor mu?
- [ ] Log'lar immutable mı?
- [ ] Retention policy uygulanıyor mu?
- [ ] Log'lar encrypted mı?
