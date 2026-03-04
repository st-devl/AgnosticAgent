# Data Privacy & Security Matrix

## 1. Hassas Veriler
Bu projede saklanacak kritik veriler neler?
- [ ] Kullanıcı Şifreleri (Hashli)
- [ ] Kredi Kartı Tokenları (Asla ham veri saklama!)
- [ ] Kişisel Veriler (TCKN, Telefon vb.)

## 2. Credential Yönetimi
Şifreler ve API anahtarları nerede tutulacak?
- [x] `.env` dosyası (Local)
- [ ] CI/CD Secrets (Production)
- [ ] Vault / Secret Manager

## 3. Compliance (Uyumluluk)
Gereken yasal zorunluluklar:
- [ ] KVKK / GDPR
- [ ] Sözleşme Onayları (Checkbox)
- [ ] Çerez Politikası

## 4. Erişim Kontrolü (ACL)
Kim neyi görebilir?
- Admin: Tam yetki
- User: Sadece kendi verisi
- Guest: Public sayfalar
