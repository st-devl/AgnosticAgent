# Compliance

## GDPR Gereksinimleri

| Gereksinim | Implementasyon |
|------------|----------------|
| Right to access | Data export API |
| Right to erasure | Hard delete + audit |
| Data portability | JSON/CSV export |
| Consent | Explicit opt-in |
| Breach notification | 72 saat içinde |

## Data Residency

```
// Tenant bazlı DB location
if (tenant.region === 'eu') {
    database = 'db_eu';
} else {
    database = 'db_us';
}
```

## SOC 2 Checklist

- [ ] Access control policies
- [ ] Change management
- [ ] Risk assessment
- [ ] Incident response
- [ ] Vendor management
- [ ] Security awareness training

## PCI-DSS (Ödeme sistemleri için)

- [ ] Cardholder data encrypted
- [ ] No storage of CVV
- [ ] Secure transmission
- [ ] Access logging
- [ ] Regular testing
