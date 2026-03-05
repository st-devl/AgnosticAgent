---
description: analyze_override - Ezilen (etkisiz kalan) kodun kök neden analizi ve kalıcı çözümü
---

# Ezilen Kod & Override Kök-Neden Analiz Workflow

> ⚠️ **GATEKEEPER BAĞLANTISI:** Bu workflow yazma işlemi içerebilir. Bkz: `.agent/rules/gatekeeper.md`

## Amaç
Etkisiz kalan (ezilen) kodu yamayla değil, baskın sistemi anlayarak kökten çözmek.

## Ne Zaman Kullanılır?
- Yazılan kod çalışmıyor ama hata da vermiyor
- Değişiklik yapılıyor ama sonuç değişmiyor
- Bir şey sürekli eski haline dönüyor
- "Kod doğru ama çalışmıyor" durumu

## İlgili Skill'ler
- `.agent/skills/debugging/SKILL.md`
- `.agent/skills/fullstack-integration/SKILL.md`

---

## 0. Temel Kural (ÇOK KRİTİK)

| ❌ YASAK | ✅ ZORUNLU |
|----------|-----------|
| Yeni kod ekleyip deneme | Önce sebebi %100 netleştir |
| Yama, geçici fix | Çözümü baskın sistemin İÇİNDE yap |
| Üstüne yazma | Tek kaynak prensibini uygula |

---

## 1. Sorun Tanımı (Netleştir)

Önce aşağıdakileri açıkça belirt:

```
📋 SORUN TANIMI:
- Beklenen davranış: [ne olmalıydı]
- Gerçek davranış: [ne oluyor]
- Etkisiz kalan kod: [hangi dosya/satır/parça]
- Sorunun katmanı: [ ] UI  [ ] State  [ ] Veri  [ ] Görsel  [ ] Lifecycle
```

**Bunlar netleşmeden analiz yapma.**

---

## 2. "Kim Eziyor?" Analizi (Zorunlu)

Aşağıdaki sorulara TEK TEK cevap ver:

| # | Soru | Cevap |
|---|------|-------|
| 1 | **Kod Kaynağı:** Bu davranışın TEK KAYNAĞI neresi? | state / layout / lifecycle / global kural |
| 2 | **Zamanlama:** Etkisiz kalan kod NE ZAMAN çalışıyor? | İlk yükleme / Sonradan reset / User action sonrası |
| 3 | **Veri Kaynağı:** DB, Cache veya API yanıtı kodu eziyor mu? | Evet (hangi?) / Hayır |
| 4 | **Hiyerarşi:** Daha baskın global kural veya parent var mı? | Evet (hangisi?) / Hayır |

**Varsayım YOK. Somut neden yaz.**

---

## 3. Ezilme Türünü Sınıflandır

Sorunu aşağıdakilerden **BİRİNE** yerleştir:

| Tür | Açıklama | Örnek |
|-----|----------|-------|
| **Kontrol Çakışması** | Aynı şeyi iki yer yönetiyor | Component + Parent aynı state'i set ediyor |
| **Öncelik Çakışması** | Biri her seferinde tekrar yazıyor | CSS specificity, late initialization |
| **Yaşam Döngüsü Çakışması** | Sonradan resetleniyor | mount sonrası parent re-render |
| **Kaynak Çakışması** | DB/Cache verisi baskın | API response hardcoded değeri eziyor |
| **Görsel Çakışma** | Stacking/visibility sorunu | z-index, overflow:hidden, opacity:0 |

Birden fazla ise → hangisi **baskın**, açıkla.

---

## 4. Çözüm Stratejisi (Sadece 2 Yol)

### A) Ezilen Kod GEREKSİZ ise
```
→ KALDIR
→ Tek kaynak sistemine bağla
→ Neden kaldırıldığını açıkla
```

### B) Ezilen Kod GEREKLİ ise
```
→ Çözümü baskın olan katmana TAŞI
→ Aynı seviyede çöz
→ Kontrolü tek yerde topla
```

**❌ "Üstüne bir şey daha ekleyelim" YOK.**

---

## 5. Uygulama Kuralı

- Değişiklik **SAYISI** minimum olacak
- Değişiklik **YERİ** net olacak
- Davranışı yöneten **TEK nokta** kalacak

Her değişiklik için belirt:
- Neden burada yapıldı
- Neyi ortadan kaldırdı
- Ne artık tekrar ezilmeyecek

---

## 6. Doğrulama (Kanıt)

Çözümden sonra mutlaka yaz:

```
✅ DOĞRULAMA:
- Önce neden çalışmıyordu: [kök neden]
- Şimdi neden kalıcı çalışır: [çözüm mekanizması]
- Tekrar bozulmasını engelleyen: [guard/yapı]
```

**"Kod eklendi ve çalıştı" açıklaması YETERSİZ.**

---

## 7. Yasaklar

| ❌ YASAK | Neden? |
|----------|--------|
| Deneme–yanıl | Spagetti kod üretir |
| Üstüne yazma | Sorunu gizler, çözmez |
| Aynı sorunu başka yerde çözme | Kaynak çakışması yaratır |
| Sorunu gizleyen çözümler | İleride daha büyük sorun |
| Neden açıklamadan kod | Anlaşılmaz, sürdürülemez |

---

## 8. Hedef

Sonuçta ulaşılacak durum:

- ✅ Ezilmeyen
- ✅ Tek merkezden kontrol edilen
- ✅ Kendini tekrar bozmayan
- ✅ Kalıcı çözüm

---

## Çıktı Şablonu

```markdown
## Override Analiz Raporu

### Sorun Özeti
[Beklenen vs Gerçek davranış]

### Kök Neden
[Kim eziyor + Ezilme türü]

### Çözüm
[A veya B stratejisi + Uygulama detayı]

### Doğrulama
[Önce/Sonra + Kalıcılık garantisi]
```
