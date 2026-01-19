---
name: payment-systems
version: "1.0.0"
requires: [enterprise-security]
conflicts_with: []
description: |
  Use when: Implementing payment gateways, handling transactions, webhook security,
  or ensuring PCI-DSS compliance.
  Keywords: payment, ödeme, transaction, webhook, PCI, gateway, recurring, subscription
allowed-tools: Read, Glob, Grep (Subject to Gatekeeper)
---

# 💳 Payment Systems Skill

> Bu skill ödeme sistemleri entegrasyonu için **agnostik** prensipler sağlar.
> Herhangi bir ödeme sağlayıcısı (Stripe, PayPal, Iyzico vb.) için geçerlidir.

---

## 🔐 Güvenlik Prensipleri

### 1. PCI-DSS Uyumu
- Kredi kartı numaraları **asla** sunucuda saklanmaz
- Kart bilgisi sadece tokenize edilmiş halde tutulur
- Log dosyalarında kart bilgisi **asla** görünmez

### 2. Webhook Güvenliği
- Her webhook isteği **imza doğrulaması** gerektirir
- Replay attack önleme (timestamp kontrolü)
- IP whitelist (mümkünse)

### 3. Idempotency
- Her ödeme işlemi **tekil ID** ile işaretlenir
- Aynı ID tekrar gelirse işlem tekrarlanmaz
- Database'de unique constraint zorunlu

---

## 📋 Ödeme Akışı Prensipleri

### 1. İşlem Durumları
```
pending → processing → completed
                    → failed
                    → refunded
```

### 2. Hata Yönetimi
- Network hatası → Retry (max 3)
- Gateway hatası → Log + Alert
- Validation hatası → Kullanıcıya bildir

### 3. Audit Trail
- Her işlem için tam log
- Kim, ne zaman, ne kadar, hangi sonuç
- Minimum 7 yıl saklama (yasal gereklilik)

---

## ✅ Kontrol Listesi

Ödeme entegrasyonu yaparken:

- [ ] Tokenization kullanılıyor mu?
- [ ] Webhook imza doğrulaması var mı?
- [ ] Idempotency key kullanılıyor mu?
- [ ] Hassas veri loglanmıyor mu?
- [ ] Error handling kapsamlı mı?
- [ ] Refund akışı tanımlı mı?
- [ ] Test ortamı ayrı mı?

---

## ⚠️ Yasaklar

- ❌ Kart numarasını database'e kaydetme
- ❌ CVV'yi herhangi bir yerde saklama
- ❌ Ödeme detaylarını log'a yazma
- ❌ HTTP (HTTPS olmadan) kullanma
- ❌ Webhook'u doğrulamadan işleme

---

> **NOT:** Spesifik gateway implementasyonları (Stripe, Iyzico vb.) proje dokümantasyonunda tanımlanır.
