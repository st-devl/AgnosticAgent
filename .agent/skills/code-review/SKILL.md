---
name: code-review
version: "1.0.0"
requires: []
conflicts_with: []
description: |
  Use when: Reviewing pull requests, checking code quality, doing security audits,
  or analyzing code before refactoring.
  Keywords: code review, PR review, incele, kalite kontrol, refactor analizi
allowed-tools: Read, Glob, Grep
---

# Code Review Skill

## Amaç
Kod kalitesini artırmak için sistematik inceleme yapmak.

## Ne Zaman Kullanılır
- PR review istendiğinde
- "Kodu incele" dendiğinde
- Refactor öncesi analiz gerektiğinde

## Talimatlar

### 1. Genel Kontroller
- [ ] Kod okunabilir mi?
- [ ] İsimlendirme tutarlı mı?
- [ ] Gereksiz karmaşıklık var mı?

### 2. Güvenlik Kontrolleri
- [ ] Input validation yapılmış mı?
- [ ] SQL injection riski var mı?
- [ ] Hardcoded credentials var mı?

### 3. Performans Kontrolleri
- [ ] N+1 query var mı?
- [ ] Gereksiz loop var mı?
- [ ] Memory leak riski var mı?

### 4. Test Kontrolleri
- [ ] Unit test yazılmış mı?
- [ ] Edge case'ler düşünülmüş mü?

## Çıktı Formatı

```markdown
## Code Review Özeti

### ✅ İyi Yönler
- ...

### ⚠️ Düzeltilmeli
| Dosya | Satır | Sorun | Öncelik |
|-------|-------|-------|---------|

### 🔴 Kritik
- ...

### 📝 Öneriler
- ...
```
