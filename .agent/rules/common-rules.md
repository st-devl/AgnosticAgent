# 📋 Ortak Kurallar (Common Rules)

> Bu dosya tüm skill ve workflow'larda geçerli olan ortak kuralları içerir.
> Tekrarı önlemek için tek kaynakta toplanmıştır.

---

## ⚠️ Evrensel Yasaklar

Tüm modüllerde geçerli:

- ❌ Hardcoded credentials
- ❌ Onaysız dosya yazma
- ❌ SSOT hiyerarşisini ihlal
- ❌ Log'lara hassas veri yazma
- ❌ Rollback imkanı olmadan değişiklik

---

## ✅ Evrensel Gereklilikler

Tüm modüllerde zorunlu:

- ✅ Gatekeeper onayı (write işlemleri)
- ✅ Action logging
- ✅ Error handling
- ✅ Dry-run desteği (mümkünse)

---

## 🔗 Referans

Detaylı kurallar için:
- `.agent/rules/SYSTEM.md` - Otorite zinciri
- `gatekeeper.md` - Onay kuralları
- `rules.yaml` - Machine-readable config
