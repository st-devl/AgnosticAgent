---
trigger: always_on
---

# Entegrasyon Doğrulama Checklist

> Her backend-frontend entegrasyonu bu checklist'i geçmeli.

## 📋 Kontrat Seviyesi

- [ ] Kontrat tanımlandı (`contracts/[domain]/[entity]/v[version]/contract.json`)
- [ ] Version semver formatında
- [ ] Breaking change analizi yapıldı
- [ ] Standartlara uygun (Bkz: `.agent/rules/contract-standards.md`)
- [ ] Error format standart (Bkz: `.agent/rules/error-handling.md`)

## ⚙️ Backend Seviyesi

- [ ] Input validation kontrata uygun
- [ ] Output serialization kontrata uygun
- [ ] Error handling standart formatta
- [ ] Auth requirement kontratla match ediyor
- [ ] Permission checks tanımlı
- [ ] Idempotency (gerekiyorsa) sağlanıyor
- [ ] Rate limiting (gerekiyorsa) uygulanıyor

## 🎨 Frontend Seviyesi

- [ ] Generated types kullanılıyor (any/unknown yok)
- [ ] Input transform kontrata uygun
- [ ] Output parse kontrata uygun
- [ ] Error handling standart formata uygun
- [ ] Field errors UI'da gösteriliyor
- [ ] Loading states tanımlı
- [ ] Auth token gönderiliyor
- [ ] 401/403 handling var

## 🔗 Entegrasyon Seviyesi

- [ ] Backend endpoint → Frontend hook/service mapping açık
- [ ] State flow dokümante edildi
- [ ] Request/Response tipi match ediyor
- [ ] Error codes frontend'de handle ediliyor
- [ ] Retry logic tanımlı (gerekiyorsa)
- [ ] Optimistic update (kullanılıyorsa) kontrata uygun

## 🧪 Test Seviyesi

- [ ] Happy path senaryosu tanımlı
- [ ] Validation error senaryoları tanımlı
- [ ] Auth error senaryoları tanımlı
- [ ] Business logic error senaryoları tanımlı
- [ ] Edge case'ler tanımlı
- [ ] Mock data kontrata uygun

## 📚 Dokümantasyon Seviyesi

- [ ] `contracts/registry.json` güncellendi
- [ ] `docs/registry.md` endpoint eklendi (varsa)
- [ ] CHANGELOG.md güncellendi (breaking change varsa)
- [ ] Migration guide yazıldı (breaking change varsa)
- [ ] Component/hook usage example eklendi

## ✅ Kullanım

Her entegrasyon tamamlandığında:
1. Bu checklist'i gözden geçir
2. Eksik maddeleri tamamla
3. Tamamlanamayanları not al ve neden tamamlanamadığını açıkla