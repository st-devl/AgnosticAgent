# 🏛️ SYSTEM.md - Otorite & Bağlantı Noktası

> **BU DOSYA ÖZET OTORİTEDİR.**
> Detaylı kurallar (Machine-Readable) için bkz: `.agent/config/rules.yaml`

---

## 1. Otorite Zinciri

1. **`.agent/config/rules.yaml`**: MUTLAK OTORİTE (Permissions, Routing, Logging)
2. **`gatekeeper.md`**: ONAY OTORİTESİ (Human-in-the-loop)
3. **`.agent/rules/project_context.md`**: PROJE BAĞLAMI (Domain Kuralları)

---

## 2. Değiştirilemez İlkeler

### A. Gatekeeper Kuralı
Her `WRITE` (yazma) işlemi öncesinde **kullanıcı onayı** şarttır.
*İstisna:* `// turbo` annotasyonu.

### B. Single Source of Truth (SSOT)
Çelişki durumunda teknik kararlar için `docs/tech_stack.md` esastır.

### C. Antigravity Garantisi
Agent, `.agent/config/rules.yaml` ve `gatekeeper.md` kurallarını asla bypass edemez.

---

## 3. Evrensel Kurallar

### ⚠️ Yasaklar (Tüm Modüllerde Geçerli)
- ❌ Hardcoded credentials
- ❌ Onaysız dosya yazma
- ❌ SSOT hiyerarşisini ihlal
- ❌ Log'lara hassas veri yazma
- ❌ Rollback imkanı olmadan değişiklik

### ✅ Zorunluluklar (Tüm Modüllerde Geçerli)
- ✅ Gatekeeper onayı (write işlemleri)
- ✅ Action logging
- ✅ Error handling
- ✅ Dry-run desteği (mümkünse)

---

> 📌 **NOT:** Detaylı yetki matrisi artık `.agent/config/rules.yaml` içindedir.
