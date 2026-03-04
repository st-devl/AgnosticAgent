# Product Requirements Document (PRD)

> Bu belge, sistemin **ürün mantığını, önceliklerini ve değişmez kurallarını** tanımlar.
> Antigravity Agent bu dokümanı **ana referans** olarak almak zorundadır.
> Bu belgede tanımlanan kararlar **proje boyunca değiştirilemez**.

---

## ⚖️ 1. Sistem Dengesi (Core Focus)

Bu proje hangi tarafın operasyonu üzerine yoğunlaşıyor?

- **Odak Noktası:** Admin-centric (Balanced yaklaşım destekli)

- **Açıklama:**
  Bu sistemin ana operasyonel yükü **admin paneli** üzerindedir.
  İçerik üretimi, veri yönetimi, yapılandırma, yetkilendirme ve iş akışlarının tamamı
  admin paneli üzerinden yürütülür.

  Son kullanıcı (frontend) tarafı:
  - Yüksek performanslı
  - Minimum state
  - Okuma / sınırlı etkileşim odaklı
  olacak şekilde tasarlanır.

  **Öncelik sırası değiştirilemez:**
  1. Sistem performansı
  2. Admin operasyon verimliliği
  3. Kod sürdürülebilirliği
  4. Son kullanıcı deneyimi

---

## 🛣️ 2. Ürün Yol Haritası (Roadmap)

Bu roadmap **bağlayıcıdır**.  
Agent geliştirme sırasında **yeni feature icat edemez**, sırayı değiştiremez.

### 🐣 MVP (Minimum Viable Product)

MVP hedefi:  
➡️ **Yüksek performanslı, temiz, şişmeyen bir çekirdek sistem**

- [ ] Temel veri modeli (normalize edilmiş, genişlemeye hazır)
- [ ] Rol & yetki sistemi (RBAC)
- [ ] Admin panel temel modülleri
- [ ] Ortak component altyapısı (UI + backend)
- [ ] Loglama & hata yönetimi altyapısı
- [ ] Cache stratejisi (read-heavy senaryolar için)
- [ ] API / işlem sürelerinin ölçümlenmesi

❗ MVP aşamasında:
- Gereksiz opsiyon
- Deneysel özellik
- “Belki lazım olur” kodu
kesinlikle yazılmaz.

---

### 🚀 v2 (Full Ürün / Ölçeklenme)

v2 hedefi:  
➡️ **Aynı mimariyi bozmadan ölçeklenme**

- [ ] Queue & async işlemler
- [ ] Gelişmiş raporlama
- [ ] Modül bazlı feature aç/kapat
- [ ] Yatay büyümeye uygun DB indeksleri
- [ ] Trafik artışında performans düşmeden çalışma
- [ ] Feature toggle sistemi

---

## ⚡ 3. Fonksiyonel Detaylar & Özellikler

| Özellik | Açıklama | Öncelik |
|-------|---------|---------|
| Admin Panel | Tüm sistem buradan yönetilir | P0 |
| Component Sistemi | Tek yerden yönetilen tekrar edilebilir yapılar | P0 |
| Cache Katmanı | Okuma ağırlıklı veriler için zorunlu | P0 |
| Rol & Yetki | Granüler, genişleyebilir yapı | P0 |
| Loglama | Tüm kritik işlemler kayıt altına alınır | P0 |
| Queue Sistemi | Uzun süren işlemler async çalışır | P1 |
| Raporlama | Sadece gerçekten ihtiyaç olan metrikler | P1 |

---

## 🌀 4. Uç Durumlar (Edge Cases) & Hata Yönetimi

Bu bölüm **performans ve sistem güvenliği için zorunludur**.

### Veri Yokluğu
- Boş liste durumlarında:
  - DB sorgusu minimumda tutulur
  - UI tarafında fallback component kullanılır
  - Ek sorgu tetiklenmez

### Bağlantı / Sistem Hataları
- Kritik işlemlerde:
  - Transaction zorunlu
  - Hata durumunda **tam rollback**
  - Yarım veri yazımı kesinlikle yasak

### Sıradışı Girdiler
- Tüm kullanıcı girdileri:
  - Sunucu tarafında validate edilir
  - Maksimum uzunluklar kesin tanımlıdır
  - UI taşması engellenir

### Yetkisiz Erişim
- Yetkisiz erişim denemeleri:
  - İşlem durdurulur
  - Güvenlik loguna yazılır
  - Kullanıcıya sistem detayı sızdırılmaz

---

## 👥 5. Kullanıcı Rolleri & Matris

| Rol | Yetki Seviyesi | Kritik Sorumluluk |
|----|---------------|------------------|
| Super Admin | Tam yetki | Sistem mimarisi ve yapılandırma |
| Admin | Geniş | İçerik, kullanıcı ve veri yönetimi |
| Editor | Sınırlı | İçerik üretimi |
| User | Minimum | Okuma / sınırlı etkileşim |

Rol sistemi:
- Hard-coded değil
- Genişleyebilir
- Performans dostu olmak zorundadır

---

## 📊 6. Kritik Başarı Metrikleri (KPI)

### 1. Teknik Başarı
- API yanıt süresi: **< 200ms**
- Gereksiz DB sorgusu: **0**
- N+1 sorgu: **0 tolerans**
- Cache hit oranı: **yüksek**

### 2. Mimari Başarı
- Tekrar eden kod oranı: **minimum**
- Component dışı tekrar: **yasak**
- DB şişmesi: **önceden engellenmiş**

### 3. Operasyonel Başarı
- Admin panel üzerinden tüm işlemler yapılabilir
- Manuel müdahale gerektirmez
- Sistem büyüdükçe yavaşlamaz

---

## 📝 Notlar (Değişmez Kurallar)

- Performans her zaman özellikten önce gelir
- Kod okunabilirliği uzun vadede hızdan önce gelir
- Tekrar eden her yapı component olmak zorundadır
- Veritabanı büyümesi **kontrollü ve öngörülü** olmalıdır
- “Sonradan düzeltiriz” yaklaşımı kesinlikle yasaktır

> Antigravity Agent bu belgeye aykırı karar alamaz.
