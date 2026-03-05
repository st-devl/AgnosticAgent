---
name: performance
version: "1.0.0"
requires: [database-architecture]
conflicts_with: []
description: |
  Use when: Implementing cache strategies, optimizing slow queries, managing memory,
  setting up background jobs, or improving API response times.
  Keywords: cache, redis, slow query, memory leak, queue job, background job, performans
allowed-tools: Read, Glob, Grep, Edit, Write (Subject to Gatekeeper)
---

# Performance Skill

> 📌 Ortak kurallar için: `.agent/rules/common-rules.md`

> **Teknoloji Agnostik:** Tüm diller ve framework'ler için performans prensipleri.

## 🎯 Selective Reading Rule

**Sadece ilgili dosyayı oku!**

| Dosya | Ne Zaman Oku |
|-------|-------------|
| `cache.md` | Cache stratejisi kurulurken |
| `query.md` | Query optimizasyonu, N+1 |
| `memory.md` | Memory leak, batch processing |
| `jobs.md` | Background job, queue |
| `api.md` | API response optimizasyonu |

---

## 🚀 Performans Hedefleri

| Metrik | Hedef | Kritik Sınır |
|--------|-------|--------------| 
| API Response (p50) | < 100ms | < 500ms |
| API Response (p95) | < 200ms | < 1s |
| Database Query | < 50ms | < 200ms |
| Cache Hit Ratio | > 90% | > 80% |
| Memory per Request | < 50MB | < 128MB |
| Error Rate | < 0.1% | < 1% |

---

## 🛠️ Tools (Hibrit Güç)

**DO NOT** guess performance issues. Measure them.

| Amaç | Tool |
|------|------|
| **Log Analizi** | `python3 .agent/skills/performance/scripts/log_analyzer.py [log_path]` |
| **Dosya Haritası** | `python3 .agent/scripts/core/files_map.py` |

---

## 📋 Quick Checklist

Her feature'da kontrol et:

- [ ] Cache strategy belirlendi mi?
- [ ] N+1 query yok mu?
- [ ] Pagination var mı?
- [ ] Background job gerekli mi?
- [ ] Memory impact hesaplandı mı?

> 📌 Detaylı kurallar için: alt dosyalara bak
