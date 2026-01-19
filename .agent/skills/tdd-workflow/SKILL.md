---
name: tdd-workflow
version: "1.0.0"
requires: []
conflicts_with: []
description: |
  Use when: Developing new features with tests first, writing unit tests,
  or following RED-GREEN-REFACTOR cycle.
  Keywords: TDD, unit test, test coverage, test yaz, RED GREEN REFACTOR
allowed-tools: Read, Write, Edit, Glob, Grep, Bash (Subject to Gatekeeper)
---

# TDD Workflow Skill

## Amaç
Yeni özellik geliştirirken Test-Driven Development metodolojisini uygulamak.

## Ne Zaman Kullanılır
- Yeni feature geliştirirken
- `/tdd` komutu ile
- "Test yazarak başla" dendiğinde

## TDD Döngüsü

```
┌─────────────────────────────────┐
│  🔴 RED: Test yaz (fail)        │
│            ↓                    │
│  🟢 GREEN: Kodu yaz (pass)      │
│            ↓                    │
│  🔵 REFACTOR: İyileştir         │
│            ↓                    │
│       ↩️ Tekrarla                │
└─────────────────────────────────┘
```

## Talimatlar

### Phase 1: RED (Test Yaz)
1. Feature gereksinimini anla
2. Minimal failing test yaz
3. Testi çalıştır, FAIL ettiğini doğrula

### Phase 2: GREEN (Kodu Yaz)
1. Testi geçirecek minimum kodu yaz
2. Fazladan kod yazma
3. Testi çalıştır, PASS ettiğini doğrula

### Phase 3: REFACTOR (İyileştir)
1. Kodu temizle
2. DRY prensibini uygula
3. Testlerin hala geçtiğini doğrula

## Çıktı Formatı

```markdown
## TDD Cycle Report

### 🔴 RED Phase
- Test: `test_should_do_something`
- Status: FAIL ✓

### 🟢 GREEN Phase  
- Implementation: `[dosya:satır]`
- Status: PASS ✓

### 🔵 REFACTOR Phase
- Changes: [yapılan değişiklikler]
- Tests: Still PASS ✓
```
