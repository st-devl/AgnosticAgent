# GEMINI – GLOBAL ENGINEERING PRINCIPLES

Bu dosya tüm projelerde geçerli olan değişmez yazılım mühendisliği kurallarını tanımlar.
Çıktılar her zaman **Türkçe** verilir.

---

## 1. Clean & Minimal Code
- Kod okunabilir, yalın ve açık niyetlidir
- Gereksiz soyutlama, karmaşıklık ve süsleme yasaktır
- "Çalışıyor" yeterli değildir; **anlaşılır ve sürdürülebilir** olmalıdır

## 2. System Load & Reusability
- Tekrar eden yapı oluşturulamaz
- Benzer çözümler tek yapı altında birleştirilir, parametre ile genişletilir
- Her çözüm şu soruyla test edilir: *"Bu ileride sistem yükü veya karmaşıklık oluşturur mu?"*

## 3. Data Storage – Performance First
- Veri katmanı sistemin omurgasıdır
- Her veri yapısı net bir amaca hizmet eder
- Sorgu performansı ve ölçeklenebilirlik önceliklidir

## 4. Data Integrity & Optimization
- Veri ilişkileri (referanslar) doğru kurulmalıdır
- Gereksiz index, alan veya yapı oluşturulmaz
- "İleride lazım olur" yaklaşımı yasaktır

## 5. Syntax, Standards & Discipline
- Kullanılan dilin standartlarına %100 uyum zorunludur
- Kod formatlı, tutarlı ve lint/type hatasızdır

## 6. Long-Term Architecture
- Geçici, günü kurtaran çözümler yasaktır
- Mimariyi bozan bug-fix veya feature kabul edilmez
- Kod yazmadan önce şu soru sorulur: *"Bu çözüm 1 yıl sonra hâlâ doğru mu?"*

## 7. Atomic & Fully Connected Architecture
- Sistem üstten alta kesintisiz bağlıdır
- Başına buyruk component / servis / modül oluşturulamaz
- Her parça bir katmana aittir ve mimariye entegredir

## 8. Planning & Responsibility
- Koddan önce kısa ve net plan yapılır
- Riskli alanlar belirtilir
- Belirsizlik varsa varsayım yapılmaz, soru sorulur

## 9. Safety & Execution Rules
- Terminal komutları otomatik çalıştırılamaz
- Silme, deploy, migration işlemleri ekstra uyarı gerektirir
- Asla sessizce işlem yapılmaz

## 10. Error & Rollback Strategy
- Her değişiklik öncesi mevcut durumu not al
- Hata durumunda rollback adımlarını raporla
- DB migration'larında `down()` metodu zorunlu

## 11. Git Conventions
- Commit format: `type(scope): description` (conventional commits)
- Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`
- Branch format: `feature/xxx`, `fix/xxx`, `refactor/xxx`

## 12. Dependency Management
- Yeni paket eklemeden önce gerekliliği sorgula
- Güncel olmayan paketler = güvenlik riski
- Lock dosyası commit'e dahil

## 13. Final Principle
> Yazılan her kod parçası, bütün sistemin kalitesini temsil eder.
> Disiplinden asla taviz verilmez.

---

## 14. Secure Mode (v1.14.2+)
- Hassas işlemlerde tüm agent aksiyonları için kullanıcı onayı iste
- Otonom exploit çalıştırma yasak
- Şu durumlarda secure mode aktif:
  - Production ortam işlemleri
  - Credential/secret içeren işlemler
  - Bulk silme veya güncelleme
  - External API çağrıları

## 15. Agent Skills Kullanımı
- Workspace'te `.agent/skills/` klasörü varsa, ilgili skill'leri kullan
- Skill formatı: YAML frontmatter + markdown talimatlar
- Skill'ler göreve özel yetenekleri tanımlar
- Antigravity skill'leri description'lardan otomatik keşfeder

## 16. Conversation & Context Yönetimi
- Uzun görevlerde bağlamı korumak için `task.md` artifact kullan
- Önceki konuşma geçmişine güvenme, önemli bilgileri docs'a kaydet
- Context window dolmadan önce kritik bilgileri kaydet:
  - `docs/project_info.md` → Credentials/URL
  - `docs/registry.md` → Component listesi
