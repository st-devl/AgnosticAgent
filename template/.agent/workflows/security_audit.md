---
description: security_audit - Güvenlik açıkları + kapatma aksiyonları (acımasız denetim)
---

# Security Audit Workflow

## Amaç
Kod, config ve endpoint'lerde güvenlik açıklarını tespit etmek.

## İlgili Skill'ler
- `enterprise-security/vulnerability.md` - OWASP, scanning
- `enterprise-security/api-security.md` - API güvenlik

## Adımlar

### 0. Otomatik Tarama (Hibrit Güç)
// turbo
İlk olarak aşağıdaki scripti çalıştır:
```bash
python3 .agent/skills/enterprise-security/scripts/secret_scanner.py
```
Çıktıyı incele ve `docs/project_keys.md` raporunu analiz et.

### 1. Tarama Kapsamı
- Mevcut kod dosyaları
- Config dosyaları (.env, config/, vb.)
- API endpoint'leri
- Auth/permission yapısı

### 2. Risk Kategorileri

| Seviye | Tanım |
|--------|-------|
| 🔴 ÇOK KRİTİK | Acil aksiyon gerekli, sistem tehlikede |
| 🟠 KRİTİK | 24 saat içinde çözülmeli |
| 🟡 DÜZELTİLMELİ | Sprint içinde çözülmeli |

### 3. Her Risk İçin Rapor

```markdown
### [Risk Adı]
- **Seviye**: 🔴/🟠/🟡
- **Açıklama**: [Ne?]
- **Etki**: [Ne olur?]
- **Kanıt**: [Dosya/satır]
- **Çözüm**: [Net adımlar]
```

### 4. Güvenlik Kontrolleri

> 📌 Detaylı kontrol listesi: `.agent/rules/checklists/security_checklist.md`

Her maddeyi sırayla kontrol et ve bulguları raporla.

### 6. Sonuç Raporu

> 📌 Rapor şablonu: `.agent/templates/reports/security_audit_report.md`

Raporu oluşturmak için script kullan (opsiyonel):
```bash
python3 .agent/scripts/auto/gen_report.py --type security
```
