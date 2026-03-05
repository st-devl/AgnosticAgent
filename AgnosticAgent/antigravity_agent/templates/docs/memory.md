# 🧠 Proje Hafızası (Memory)

> Bu dosya projenin "yaşayan hafızası"dır.
> Agent her oturumda bu dosyayı okuyarak bağlamı yeniden yükler.

---

## 📍 Mevcut Durum

**Son Güncelleme:** _Otomatik güncellenir_

| Bilgi | Değer |
|-------|-------|
| **Aktif Görev** | - |
| **İlerleme** | 0% |
| **Son Checkpoint** | - |

> 💡 Güncel durum için: `python3 .agent/scripts/core/memory_controller.py summary`

---

## 📋 Kritik Bağlam

### Teknoloji Kararları
- Bkz: `docs/tech_stack.md`

### Mimari Kararlar
- Bkz: `docs/architecture.md`

### Alınan Kararlar
- Bkz: `docs/decision_log.md`

---

## 🔖 Önemli Checkpoint'ler

| # | Tarih | Açıklama |
|---|-------|----------|
| 1 | 2026-01-17 | Memory system initialized |

> 💡 Tüm checkpoint'ler için: `.agent/state/checkpoints.json`

---

## ⚠️ Dikkat Edilmesi Gerekenler

- Onaysız yazma yasak (Bkz: `gatekeeper.md`)
- SSOT hiyerarşisi: tech_stack > architecture > prd
- Her write işlemi loglanır

---

## 🔗 İlgili Dosyalar

| Dosya | Amaç |
|-------|------|
| `.agent/state/progress.json` | İlerleme durumu |
| `.agent/state/checkpoints.json` | Kayıt noktaları |
| `.agent/state/context.json` | Mevcut bağlam |
| `docs/decision_log.md` | Karar kayıtları |

---

> **NOT:** Bu dosya insan tarafından okunur, makine state'i `.agent/state/` klasöründedir.
