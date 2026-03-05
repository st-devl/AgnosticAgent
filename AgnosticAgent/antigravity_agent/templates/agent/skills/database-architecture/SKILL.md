---
name: database-architecture
version: "1.0.0"
requires: []
conflicts_with: []
description: |
  Use when: Creating/modifying database tables, adding indexes, writing migrations,
  optimizing queries, fixing N+1 problems, designing partitions, or doing DB audits.
  Keywords: tablo, migration, index, query, partition, FK, foreign key, N+1, slow query
allowed-tools: Read, Glob, Grep, Edit
---

# Database Architecture Skill

> 📌 Ortak kurallar için: `.agent/rules/common-rules.md`

> **Teknoloji Agnostik:** Tüm veritabanları için mimari prensipleri.

## 🔗 İlgili Workflow
- `/db_audit` - Kapsamlı veritabanı denetimi için bu workflow'u kullan

## 🎯 Selective Reading Rule

**Sadece ilgili dosyayı oku!**

| Dosya | Ne Zaman Oku |
|-------|-------------|
| `schema.md` | Tablo tasarımı, ilişkiler |
| `indexing.md` | Index stratejisi, performans |
| `migration.md` | Schema değişiklikleri |
| `partition.md` | Büyük tablolar, partitioning |

---

## 🛠️ Tools (Hibrit Güç)

**DO NOT** read migration files manually to understand the schema.
Instead, run this specific script to get a perfect JSON summary:

```bash
python3 .agent/skills/database-architecture/scripts/schema_inspector.py
```

---

## 🏗️ Temel Kurallar

| Kural | Açıklama |
|-------|----------|
| `id` BIGINT | Auto-increment, asla UUID (performans) |
| `created_at` | Zorunlu, indexed |
| `updated_at` | Zorunlu |
| `deleted_at` | Soft delete için (nullable) |
| `tenant_id` | Multi-tenant projelerde zorunlu |

---

## 📋 Quick Checklist

- [ ] Primary key BIGINT mi?
- [ ] created_at/updated_at var mı?
- [ ] Tenant-aware (tenant_id) mi?
- [ ] Foreign key'ler tanımlı mı?
- [ ] Gerekli index'ler eklendi mi?

> 📌 Detaylı kurallar için: alt dosyalara bak

---

## ❌ Anti-Patterns

| YAPMA | YAP |
|-------|-----|
| Her şey için PostgreSQL | Projeye uygun DB seç |
| UUID primary key | BIGINT kullan |
| SELECT * | Spesifik kolonlar |
| Index atlama | Query planına göre indexle |
| Büyük JSON kolonları | Normalize et |
