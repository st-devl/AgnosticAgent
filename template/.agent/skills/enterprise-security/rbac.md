# RBAC - Role-Based Access Control

## Rol Hiyerarşisi

```
Super Admin (Platform)
    │
    ├─ Tenant Admin
    │     │
    │     ├─ Manager
    │     │     │
    │     │     └─ User
    │     │
    │     └─ Viewer (Read-only)
    │
    └─ Support (Cross-tenant, limited)
```

## Permission Yapısı

```
// Resource-based permissions
{resource}.{action}

Örnekler:
orders.view
orders.create
orders.edit
orders.delete

// Tenant-scoped
tenant.settings.edit
tenant.users.manage
tenant.billing.view
```

## Permission Check

```
✅ DOĞRU: Tenant + Resource + Action
if (user.can('{action}') AND resource.tenant_id == current_tenant.id) {
    // İzin ver
}

❌ YANLIŞ: Sadece permission
if (user.can('{action}')) {
    // Tenant kontrolü yok!
}
```

## RBAC Checklist

- [ ] Her endpoint'te permission kontrolü var mı?
- [ ] Tenant ownership kontrolü var mı?
- [ ] Role assignment audit loglanıyor mu?
- [ ] Permission cache tenant-aware mı?
