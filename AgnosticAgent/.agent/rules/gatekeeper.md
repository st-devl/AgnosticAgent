---
description: Kesin kullanıcı onayı zorunluluğu ve işlem durdurma kuralı
---

# 🛡️ GATEKEEPER (Onay Muhafızı)

> ⚠️ **MUTLAK OTORİTE:** Bu dosya sistemin EN ÜST düzey kuralıdır.
> Her workflow bu dosyayı okumak ve uygulamak ZORUNDADIR.
> Bu kural geçersiz kılınamaz.

---

## 🚨 ZORUNLU KONTROL (Her Write Öncesi)

Aşağıdaki araçları çağırmadan **ÖNCE** bu kontrolleri yap:

1. `write_to_file`
2. `replace_file_content`
3. `multi_replace_file_content`
4. `run_command` (dosya değiştiren)

### Kontrol Listesi:
- [ ] Kullanıcı bu işlemi onayladı mı? ("evet", "yap", "onay", "devam")
- [ ] Onay mevcut turdaysa veya bir önceki turdaysa → **İZİN VER**
- [ ] Onay yoksa → **DUR, notify_user çağır, bekle**

---

## 🔐 ZİNCİR KANITI (Chain of Approval)

Her write işleminden önce şunu internal olarak doğrula:

```
IF (user_approval_exists_in_current_or_previous_turn):
    → PROCEED with write
ELSE:
    → STOP
    → Call notify_user with BlockedOnUser: true
    → WAIT for approval
```

---

## 🚫 BYPASS YASAK

Aşağıdaki bahaneler geçersizdir:
- ❌ "Kullanıcı acele ediyor"
- ❌ "Küçük bir değişiklik"
- ❌ "Sadece düzeltme"
- ❌ "Önceki onay yeterli"

**Her yeni write işlemi = Yeni onay gereksinimi**

---

## ✅ İstisna Durumlar (Onay Gerektirmeyen)

- Dosya okuma (`view_file`, `list_dir` vb.)
- Soru cevaplama
- Analiz raporu hazırlama (Artifact)
- `// turbo` annotasyonlu komutlar

---

## 🔗 Workflow Entegrasyonu

Her workflow şu satırla başlamalı:
```
> ⚠️ **GATEKEEPER BAĞLANTISI:** [Açıklama]. Bkz: `.agent/rules/gatekeeper.md`
```

Bu satır olmayan workflow **çalıştırılmamalı**.

---

> **ANTIGRAVITY GARANTİSİ:** "Onay almadan tek bir karakter bile değiştirmeyeceğim."

