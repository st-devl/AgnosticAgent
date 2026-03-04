# Security Checklist

> **Tekrar Eden Kontroller:** Bu dosya tüm güvenlik işlemlerinde referans alınır.

## 🔒 Temel Kontroller
- [ ] Hardcoded anahtar/şifre var mı?
- [ ] `.env` dosyası git ignore edilmiş mi?
- [ ] API key'ler environment variable olarak mı saklanıyor?
- [ ] `debug=true` production'da kapalı mı?

## 🔑 Auth & Permission
- [ ] Yetkisiz erişim testi yapıldı mı? (IDOR)
- [ ] Role-based access control (RBAC) tüm endpoint'lerde var mı?
- [ ] Rate limiting aktif mi?
- [ ] Şifreler hashlenmiş mi (Argon2/Bcrypt)?

## 🛡️ Veri Güvenliği
- [ ] Hassas veriler loglara yazılmıyor değil mi?
- [ ] SQL Injection koruması (ORM kullanımı) var mı?
- [ ] XSS koruması (Output escaping) var mı?
- [ ] CSRF token kontrolü aktif mi?

## 📦 Dependency & Config
- [ ] `npm audit` / `composer audit` çalıştırıldı mı?
- [ ] Kullanılmayan paketler temizlendi mi?
- [ ] Config dosyalarında hassas veri var mı?
