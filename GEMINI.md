# GEMINI – GLOBAL ENGINEERING PRINCIPLES

Tüm projelerde geçerli değişmez yazılım mühendisliği kuralları.  
**Çıktılar her zaman Türkçe.**

---

## 🎯 Temel İlkeler

### 1. Clean Code
- Okunabilir, yalın, açık niyetli
- Gereksiz soyutlama yasak
- "Çalışıyor" ≠ yeterli → anlaşılır + sürdürülebilir olmalı

### 2. System Load
- Tekrar eden yapı yasak
- Benzer çözümler → tek yapı + parametre
- Her çözüm test: *"Bu sistem yükü/karmaşıklık oluşturur mu?"*

### 3. Data Layer
- Her veri yapısı → net amaç
- Performans + ölçeklenebilirlik öncelik
- Gereksiz index/alan yasak, "ileride lazım" yaklaşımı yasak

### 4. Standards
- Dilin standartlarına %100 uyum
- Formatlanmış, tutarlı, lint/type hatasız kod

### 5. Architecture
- Geçici çözüm yasak
- Mimariyi bozan bug-fix/feature yasak
- Soru: *"Bu 1 yıl sonra hâlâ doğru mu?"*

### 6. Atomic System
- Üstten alta kesintisiz bağlantı
- Başına buyruk component/servis yasak
- Her parça bir katmana ait

---

## ⚡ Execution Rules

### 7. Planning
- Kod öncesi kısa plan
- Riskli alanlar belirt
- Belirsizlik → varsayım yapma, **SOR**

### 8. Safety
- Terminal komutları otomatik çalıştırma yasak
- Silme/deploy/migration → ekstra uyarı
- Asla sessizce işlem yapma

### 9. Error & Rollback
- Her değişiklik öncesi mevcut durum not
- Hata durumunda rollback adımları raporla
- DB migration → `down()` zorunlu

### 10. Git
- Format: `type(scope): description`
- Types: `feat|fix|refactor|docs|test|chore`
- Branch: `feature/xxx`, `fix/xxx`, `refactor/xxx`

### 11. Dependencies
- Yeni paket → gerekliliği sorgula
- Güncel olmayan paket = güvenlik riski
- Lock dosyası commit'e dahil

---

## 🔒 Secure Mode (v1.14.2+)

Şu durumlarda kullanıcı onayı **zorunlu**:
- Production işlemleri
- Credential/secret işlemleri
- Bulk silme/güncelleme
- External API çağrıları

**Otonom exploit çalıştırma yasak.**

---

## 🛠️ Agent Skills & Context

### 12. Skills Kullanımı
- `.agent/skills/` varsa ilgili skill'leri kullan
- Antigravity skill'leri otomatik keşfeder
- Skill formatı: YAML frontmatter + markdown

### 13. Context Yönetimi
- Uzun görevler → `task.md` artifact kullan
- Önceki konuşmaya güvenme, önemli bilgileri kaydet:
  - `docs/project_info.md` → Credentials/URL
  - `docs/registry.md` → Component listesi
- Context dolmadan kritik bilgileri docs'a taşı

---

## 🏆 Final Principle

> Yazılan her kod parçası, bütün sistemin kalitesini temsil eder.  
> **Disiplinden asla taviz verilmez.**

---