---
name: debugging
version: "1.0.0"
requires: []
conflicts_with: []
description: |
  Use when: Fixing bugs, tracing errors, analyzing stack traces, finding root causes,
  or debugging hard-to-find issues in the application.
  Keywords: bug, hata, çalışmıyor, error, exception, trace, debug, sorun, neden
allowed-tools: Read, Glob, Grep
---

# Debugging Skill

## Amaç
Zor hataları sistematik olarak bulmak ve kök nedeni tespit etmek.

> **Teknoloji Agnostik:** Bu skill tüm diller ve framework'ler için geçerlidir.
> Framework-specific komutlar için `tech_stack.md` referans alın.

## 🔗 İlgili Workflow
- `/deep_bug_hunt` - Kapsamlı hata analizi için bu workflow'u kullan

---

## 🔍 4 Aşamalı Debug Stratejisi

### Aşama 1: Hatayı Anla
```
1. Hata mesajını tam oku
2. Stack trace'in ilk satırına odaklan
3. Hangi dosya/satırda?
4. Ne zaman oluyor? (Her zaman mı, bazen mi?)
5. Son değişiklik ne?
```

### Aşama 2: Yeniden Üret
```
1. Hatayı tutarlı şekilde üret
2. Minimum adımları belirle
3. Hangi koşullarda oluyor?
4. %100 tekrarlanabilir mi?
```

### Aşama 3: İzole Et
```
1. Şüpheli kodu daralt
2. Binary search: Kodun yarısını devre dışı bırak
3. Sorunu en küçük parçaya indir
4. Tek değişken kaldığında durumu analiz et
```

### Aşama 4: Düzelt & Doğrula
```
1. Kök nedeni hedefle (semptom değil)
2. Düzeltmeyi uygula
3. Orijinal hatayı tekrar dene
4. Regression testi yap
5. Benzer yerleri kontrol et
```

---

## 🐛 Evrensel Hata Kategorileri

### Runtime Hataları

| Hata Tipi | Olası Neden | Çözüm Yöntemi |
|-----------|-------------|---------------|
| Null/Undefined | Değer atanmamış | Null check, optional chaining |
| Type Error | Yanlış tip | Type guard, validation |
| Index Out of Range | Dizi sınırı aşıldı | Sınır kontrolü |
| Division by Zero | Sıfıra bölme | Guard condition |
| Stack Overflow | Sonsuz recursion | Base case kontrolü |

### Bağlantı Hataları

| Hata Tipi | Olası Neden | Çözüm Yöntemi |
|-----------|-------------|---------------|
| Connection Refused | Servis çalışmıyor | Port/host kontrol |
| Timeout | Yavaş yanıt | Timeout artır, optimize et |
| SSL Error | Sertifika sorunu | Sertifika yenile |
| CORS | Cross-origin | Backend CORS config |

### Database Hataları

| Hata Tipi | Olası Neden | Çözüm Yöntemi |
|-----------|-------------|---------------|
| Table Not Found | Migration eksik | Migration çalıştır |
| Constraint Violation | FK/Unique ihlali | Veri bütünlüğü kontrol |
| Lock Timeout | Deadlock | Query optimize |
| Connection Pool | Bağlantı bitmiş | Pool size artır |

---

## 🔧 Debug Teknikleri (Dil Bağımsız)

### 1. Print/Log Debugging
```
Stratejik noktalara log ekle:
- Fonksiyon girişi
- Kritik değişken değerleri
- Koşullu dallanmalar
- Döngü iterasyonları
```

### 2. Binary Search Debugging
```
Şüpheli kod bloğu:
├─ Yarısını devre dışı bırak
├─ Hata devam ediyor mu?
│   ├─ EVET → O yarıda
│   └─ HAYIR → Diğer yarıda
└─ Tek satıra inene kadar tekrarla
```

### 3. Rubber Duck Debugging
```
Sorunu sesli olarak açıkla:
1. "Bu kod ne yapmalı?"
2. "Şu an ne yapıyor?"
3. "Fark nerede?"
```

### 4. Time Travel / State Inspection
```
Her adımda state'i logla:
- Input → ne geldi?
- Process → ne oldu?
- Output → ne çıktı?
```

---

## 📋 Debug Checklist

### Hata Alındığında

- [ ] Error message tam okundu mu?
- [ ] Stack trace'in ilk (en alttaki) satırı nerede?
- [ ] Son değişiklik ne? (git diff)
- [ ] Başka ortamda çalışıyor mu?
- [ ] Cache/build temizlendi mi?

### Hata Bulunamıyorsa

- [ ] Log dosyaları kontrol edildi mi?
- [ ] Network istekleri kontrol edildi mi?
- [ ] Database sorguları kontrol edildi mi?
- [ ] Environment değişkenleri doğru mu?
- [ ] Dependency versiyonları doğru mu?

### Düzeltme Sonrası

- [ ] Hata tekrar test edildi mi?
- [ ] Yan etkiler kontrol edildi mi?
- [ ] Benzer yerlerde aynı sorun var mı?
- [ ] Regression testi yazıldı mı?
- [ ] Dokümantasyon güncellendi mi?

---

## 🚨 Evrensel Debug Komutları

### Version Control (Git)
```bash
# Son değişiklikler
git log --oneline -10
git diff HEAD~5

# Belirli dosya geçmişi
git log -p -- <dosya>

# Kimin yaptığını bul
git blame <dosya>
```

### Process / Port
```bash
# Port kullanan process
lsof -i :<port>       # Linux/Mac
netstat -ano | findstr :<port>  # Windows

# Çalışan processler
ps aux | grep <name>  # Linux/Mac
tasklist | findstr <name>  # Windows
```

### Disk / Memory
```bash
# Disk kullanımı
df -h                 # Linux/Mac
dir                   # Windows

# Memory kullanımı
free -m               # Linux
```

---

## 📝 Hata Raporu Formatı

```markdown
## Hata Özeti
[Kısa, net açıklama]

## Yeniden Üretme Adımları
1. ...
2. ...
3. ...

## Beklenen Davranış
[Ne olmalıydı]

## Gerçekleşen Davranış
[Ne oldu + error message]

## Ortam Bilgisi
- OS: 
- Runtime/Framework version:
- Browser (frontend ise):

## Araştırma Notları
- Denenen çözümler
- Şüphelenilen kök neden

## Ek Bilgi
- Stack trace
- Log çıktısı
- Screenshot
```

---

## ❌ Anti-Patterns

| YAPMA | YAP |
|-------|-----|
| Rastgele değişiklik yap | Önce anla, sonra düzelt |
| Kanıtları görmezden gel | Kanıtları takip et |
| Varsayımla başla | Kanıtla başla |
| Yeniden üretmeden düzelt | Önce reproduce et |
| Semptomu düzelt | Kök nedeni bul |
| "Bende çalışıyor" de | Farkı bul |
