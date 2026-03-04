---
name: enterprise-security
version: "1.0.0"
requires: []
conflicts_with: []
description: |
  Use when: Implementing RBAC, audit logging, data encryption, GDPR/SOC2 compliance,
  API security, vulnerability scanning, or admin impersonation features.
  Keywords: RBAC, audit log, encryption, GDPR, SOC2, permission, güvenlik, compliance, OWASP, vulnerability
allowed-tools: Read, Glob, Grep
---

# Enterprise Security Skill

> **Teknoloji Agnostik:** Tüm diller ve framework'ler için güvenlik prensipleri.
> Think like an attacker, defend like an expert.

## 🔗 İlgili Workflow
- `/security_audit` - Kapsamlı güvenlik denetimi için bu workflow'u kullan

## 🎯 Selective Reading Rule

**Sadece ilgili dosyayı oku!**

| Dosya | Ne Zaman Oku |
|-------|-------------|
| `rbac.md` | Rol/izin sistemi kurulurken |
| `audit.md` | Audit log implementasyonu |
| `encryption.md` | Veri şifreleme gerektiğinde |
| `vulnerability.md` | Güvenlik taraması/audit |
| `compliance.md` | GDPR/SOC2 gereksinimleri |
| `api-security.md` | API güvenlik kontrolü |

---

## ⚠️ Core Security Principles

| Prensip | Uygulama |
|---------|----------|
| **Assume Breach** | Saldırgan içeride gibi tasarla |
| **Zero Trust** | Asla güvenme, her zaman doğrula |
| **Defense in Depth** | Çoklu katman, tek nokta yok |
| **Least Privilege** | Minimum gerekli yetki |
| **Fail Secure** | Hata durumunda erişimi reddet |

---

## 🛠️ Tools (Hibrit Güç)

**Trust but Verify.** Use these tools to scan the codebase.

| Amaç | Tool |
|------|------|
| **Secret Scan** | `python3 .agent/skills/enterprise-security/scripts/secret_scanner.py [path]` |
| **File Architecture** | `python3 .agent/scripts/core/files_map.py` |

---

## 📋 Quick Security Checklist

> 📌 Detaylı kontrol listesi: `.agent/rules/checklists/security_checklist.md`

> 📌 Detaylı checklist'ler için: alt dosyalara bak

---

## ❌ Anti-Patterns

| YAPMA | YAP |
|-------|-----|
| Her CVE'ye alarm ver | Exploitability + asset'e göre önceliklendir |
| Güvenliği sonraya bırak | Tasarımdan itibaren düşün |
| Tek katman savunma | Defense in depth |
| Hata durumunda izin ver (fail-open) | Hata durumunda reddet (fail-closed) |
| Third-party'ye körü körüne güven | Verify, audit |
