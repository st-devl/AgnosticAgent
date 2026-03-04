---
description: start - Yeni Proje Başlatma Protokolü (Röportaj -> Analiz -> Roadmap)
---

# 🚀 Project Kickoff Workflow (/start)

> ⚠️ **GATEKEEPER BAĞLANTISI:** Bu workflow dosya oluşturur. Her yazma işlemi öncesinde kullanıcı onayı ZORUNLUDUR. Bkz: `.agent/rules/gatekeeper.md`

> 🧠 **HAFIZA ENTEGRASYONU:** Workflow başında ve sonunda checkpoint kaydedilir.
> ```bash
> # Workflow başında
> python3 .agent/scripts/core/memory_controller.py set-task "Project Kickoff"
> # Workflow sonunda
> python3 .agent/scripts/core/memory_controller.py checkpoint "Project Kickoff completed"
> python3 .agent/scripts/core/memory_controller.py complete-task
> ```

Bu workflow, yeni bir projeye başlarken Agent'ın "Proje Yöneticisi" şapkasını takmasını sağlar. Süreç, kullanıcıyla yapılan detaylı bir röportajla başlar, dokümantasyonla devam eder ve stratejik bir yol haritasıyla son bulur.

---

## 🛑 Ön Hazırlık

Eğer `docs/` klasörü yoksa oluştur.
Şu şablonların varlığını kontrol et (yoksa kullanıcıyı uyar):
- `docs/templates/project_brief_template.md`
- `docs/templates/tech_stack_template.md`
- `docs/templates/design_brief_template.md`
- `docs/templates/data_privacy_template.md`

---

## AŞAMA 1: RÖPORTAJ (Veri Toplama)

Kullanıcıya tek seferde tüm soruları sorma. Sırayla ve sohbet havasında ilerle.

### Adım 1.1: Proje Tanımı
Kullanıcıya sor:
> "Merhaba! Yeni projeniz hayırlı olsun. Başlamadan önce projeyi tanıyalım.
> Projenin adı, temel amacı ve hedef kitlesinden bahsedebilir misiniz?
> MVP (Olmazsa olmaz) özellikler nelerdir?"

**Eylem:** Cevapları `docs/templates/project_brief_template.md` formatında düzenleyip `docs/project_brief.md` dosyasına yaz.

### Adım 1.2: Teknoloji Tercihleri
Kullanıcıya sor:
> "Harika. Peki hangi teknolojileri kullanacağız?
> Dil, Framework, Veritabanı, Docker vb. tercihleriniz var mı?
> Yoksa benim en uygun stack'i önermemi mi istersiniz?"

**Eylem:** Cevapları (veya onaylanan önerileri) `docs/templates/tech_stack_template.md` formatında `docs/tech_stack.md` dosyasına yaz.

### Adım 1.3: Tasarım ve UX
Kullanıcıya sor:
> "Tasarım tarafında nasıl bir his istiyoruz?
> Minimalist mi, Kurumsal mı?
> Beğendiğiniz örnek siteler var mı?"

**Eylem:** Cevapları `docs/templates/design_brief_template.md` formatında `docs/design_brief.md` dosyasına yaz.

### Adım 1.4: Veri ve Güvenlik
Kullanıcıya sor:
> "Son olarak, projede saklanacak kritik veriler var mı?
> Şifre, TCKN, Kredi Kartı gibi?
> Credential yönetimini nasıl yapalım (.env, vault)?"

**Eylem:** Cevapları `docs/templates/data_privacy_template.md` formatında `docs/data_privacy.md` dosyasına yaz.

---

## AŞAMA 2: DERİN ANALİZ (The Mental Pause)

Tüm dosyalar oluşturulduktan sonra **DUR VE DÜŞÜN**.

1.  Tüm `docs/*.md` dosyalarını oku.
2.  Aşağıdaki analizleri yap:
    *   **Tutarlılık:** Teknolojiler projeye uygun mu? (Örn: Basit blog için Microservice mi istenmiş?)
    *   **Eksiklik:** MVP listesinde login var ama Auth teknolojisi seçilmemiş mi?
    *   **Risk:** Hassas veri var ama şifreleme konuşulmamış mı?
    *   **Performans:** Trafik beklentisi ile altyapı uyumlu mu?

**ÇIKTI (Notify User):**
Kullanıcıya detaylı bir "Analiz Raporu" sun.
*   ✅ Onaylanan Kısımlar
*   ⚠️ Riskler ve Uyarılar
*   💡 İyileştirme Önerileri

> "Analizimi tamamladım. Raporu inceleyip onaylarsanız Yol Haritasını (Roadmap) çıkaracağım."

---

## AŞAMA 2.5: TAMAMLANMA KONTROLÜ (Fallback)

Roadmap oluşturmadan önce aşağıdaki dosyaların varlığını kontrol et:

| Dosya | Durum |
|-------|-------|
| `docs/project_brief.md` | ☐ |
| `docs/tech_stack.md` | ☐ |
| `docs/design_brief.md` | ☐ |
| `docs/data_privacy.md` | ☐ |

> ⚠️ **Eksik varsa:** Kullanıcıya eksik dosyayı bildir ve ilgili röportaj adımına geri dön.
> ✅ **Hepsi tamam:** Devam et.

---

## AŞAMA 3: ROADMAP OLUŞTURMA (Strateji)

Kullanıcı onay verdikten sonra:

1.  `architecture.md` dosyasını kontrol et (yoksa standart bir yapı oluştur).
2.  Projenin büyüklüğüne göre `task.md` dosyasını oluştur.

**Roadmap Kuralı:** Adımlar "Check-point" mantığında olmalı.
Örnek yapı:
*   [ ] 🏗️ Faz 1: Altyapı ve Veritabanı
*   [ ] 📦 Faz 2: Backend Core (Auth, User vb.)
*   [ ] 🎨 Faz 3: Frontend & UI
*   [ ] 🚀 Faz 4: Deploy & Test

**Eylem:** `task.md` dosyasını oluştur ve kullanıcıya "Hazırız! İlk maddeye başlayalım mı?" diye sor.
