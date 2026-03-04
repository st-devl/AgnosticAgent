# Decision Log

> Bu dosya önemli mimari ve teknik kararların kaydını tutar.
> Her karar gerekçesiyle birlikte belgelenir.

---

## Format

```
### [Tarih] Karar Başlığı
**Durum:** Kabul Edildi / Reddedildi / Beklemede
**Karar:** [Ne kararlaştırıldı]
**Gerekçe:** [Neden bu karar alındı]
**Alternatifler:** [Diğer seçenekler]
**Riskler:** [Olası riskler]
```

---

## Kararlar

### [2026-01-17] Hibrit Mimari Seçimi
**Durum:** Kabul Edildi
**Karar:** Markdown (orchestration) + Python (execution) hibrit model kullanılacak.
**Gerekçe:** Markdown insan okunabilirliği sağlar, Python otomasyon gücü verir.
**Alternatifler:** Pure YAML, Pure Python, DSL
**Riskler:** İki dil arasında tutarsızlık riski

### [2026-01-17] SSOT Hiyerarşisi
**Durum:** Kabul Edildi
**Karar:** tech_stack.md > architecture.md > prd.md öncelik sırası.
**Gerekçe:** Teknoloji kararları diğer tüm kararları etkiler.
**Alternatifler:** Flat yapı (öncelik yok)
**Riskler:** Hiyerarşi yanlış uygulanabilir

### [2026-01-17] Gatekeeper Zorunluluğu
**Durum:** Kabul Edildi
**Karar:** Her write işlemi öncesi kullanıcı onayı zorunlu.
**Gerekçe:** Otonom agent güvenlik riski oluşturabilir.
**Alternatifler:** Fully autonomous, Whitelist-based
**Riskler:** İş akışını yavaşlatabilir

---

> **NOT:** Yeni kararlar bu dosyanın sonuna eklenir.
