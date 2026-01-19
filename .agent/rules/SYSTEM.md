# 🏛️ SYSTEM.md - Otorite & Bağlantı Noktası

> **BU DOSYA ÖZET OTORİTEDİR.**
> Detaylı kurallar (Machine-Readable) için bkz: `rules.yaml`

---

## 1. Otorite Zinciri

1. **`rules.yaml`**: MUTLAK OTORİTE (Permissions, Routing, Logging)
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
Agent, `rules.yaml` ve `gatekeeper.md` kurallarını asla bypass edemez.

---

> 📌 **NOT:** Detaylı yetki matrisi artık `rules.yaml` içindedir.


