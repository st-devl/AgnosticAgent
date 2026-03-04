---
trigger: always_on
description: Antigravity Agent için proje bağlamı ve kaynak hiyerarşisi
---

# 📌 Project Context

> Bu dosya, Antigravity Agent'ın "hafızası" ve "karar destek" mekanizmasıdır.
> Kurallar için bkz: `.agent/rules/SYSTEM.md`

---

## 🔝 1. SSOT Hiyerarşisi (Tek Doğruluk Kaynakları)

Birden fazla dosya çelişirse, aşağıdaki hiyerarşi geçerlidir:

1.  **Teknoloji:** `docs/tech_stack.md` (Değiştirilemez teknoloji kararları)
2.  **Mimari:** `docs/architecture.md` (Değiştirilemez inşa kuralları)
3.  **Ürün/PRD:** `docs/prd.md` (Değiştirilemez ürün mantığı)
4.  **Hafıza:** `docs/memory.md` (Geçmiş kararlar ve bağlam)

---

## 📑 2. Görev Bazlı Referans Tablosu

Ajan, ilgili görevde yanındaki dosyaları okumadan işleme başlayamaz:

| Görev / Durum | Okunacak Dosyalar (Zorunlu) |
|---------------|-----------------------------|
| **Kod Yazma (Genel)** | `tech_stack.md` + `registry.md` + `architecture.md` + `gatekeeper.md` + `memory.md` |
| **Frontend / UI Geliştirme** | `component-architecture` (Skill) + `architecture.md` |
| **Backend / API / DB** | `performance` (Skill) + `database-architecture` (Skill) |
| **API / Dış Servis / Env** | `tech_stack.md` + `secret_policy.md` |
| **Hata / Debugging** | `deep_bug_hunt.md` + `memory.md` + `debugging` (Skill) |
| **Planlama / Mimari / Audit** | `project_brief.md` + `prd.md` + `architecture.md` + `memory.md` |
| **Güvenlik / Yetki İşlemi** | `enterprise-security` (Skill) + `secret_policy.md` + `rules.yaml` |
| **Full-Stack / Entegrasyon** | `fullstack-integration` (Skill) + `.agent/config/rules.yaml` |

---

## 🛡️ 3. Güvenlik ve Onay Denetimi (Safety Check)

Ajan, parmağını kıpırdatmadan önce şu dosyaları kontrol ettiğinden emin olmalıdır:
-   **`gatekeeper.md`**: Kullanıcı onayı var mı? (Onay yoksa `WRITE` yasak!)
-   **`.agent/config/rules.yaml`**: Mevcut skill/workflow bu işlemi yapmaya yetkili mi? (skills bölümü)

---

## 🤖 4. Registry Otomasyon Kuralları (Auto-Update)

Aşağıdaki durumlarda `docs/registry.md` dosyasını **ANINDA** güncelle:

| Tetikleyici (Trigger) | Aksiyon (Action) |
|-----------------------|------------------|
| **Yeni Model/Entity** | Backend Modules tablosuna ekle |
| **Yeni UI Component** | Frontend Components tablosuna ekle |
| **Yeni Controller/Route** | API Endpoints tablosuna ekle |
| **Yeni DB Migration** | Model açıklamasını/ilişkisini güncelle |

---

## 🏁 5. İşlem Sonu Kontrolü (Post-Op)

Her kod değişikliği veya dosya oluşturma işlemi bittiğinde şunları kontrol et:
- `docs/registry.md` güncel mi?
- Değişiklik `/CHANGELOG.md`'ye eklendi mi?
- Lint/test hataları var mı?

---
## 🔗 6. Backend ↔ Frontend Entegrasyon Disiplini

> ⚠️ Her backend/frontend kod yazımında geçerlidir.
> Detaylı kurallar: `.agent/skills/fullstack-integration/SKILL.md`

### Kritik İlkeler
- Backend + Frontend = **TEK SİSTEM** (asla bağımsız düşünme)
- Varsayım **YOK** → Eksik bilgi varsa **SOR**
- Kod yazmadan ÖNCE → **KONTRAT**

### Backend Yazarken
```
🔗 ENTEGRASYON KONTRATI (zorunlu):
İşlem: [ne yapıyor]
Girdi: [alan | tip | zorunlu/opsiyonel]
Çıktı: [başarı + hata yapısı]
Frontend: [hangi UI parçası kullanacak]
```

### Frontend Yazarken
```
🔗 BACKEND BAĞLANTISI (zorunlu):
Kontrat: [operation@version]
State: [nereden → nereye → nasıl]
```

### Büyük İşlerde Sıra
Kontrat → Backend → Frontend → Doğrulama
*(Detaylı workflow: `.agent/workflows/new-feature.md`)*

### Kırmızı Çizgiler
❌ Kontrat olmadan kod  
❌ Kopya yapı üretme  
❌ Backend/Frontend ayrı düşünme  

---

## 💡 7. Genel Notlar

-   **Context İsrafı:** Eğer bir dosya boşsa (`...`) veya sadece tablo başlığından ibaretse, o dosyayı atla ve kullanıcıya doldurmasını öner.
-   **Varsayım Yasak:** Herhangi bir belirsizlikte `architecture.md` veya `prd.md` dosyalarına bak, orada da yoksa kullanıcıya sor.
-   **Skill Discovery:** Ajan, `.agent/skills/` içindeki dökümlere göre uzmanlık yükler.

> **ANTIGRAVITY GARANTİSİ:** "Hafızamda olmayan hiçbir şeyi doğru kabul etmem."