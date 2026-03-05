---
name: engineering-guardrails
description: Software architecture and clean coding guardrails (SSOT, DRY, Component principles).
---

# Engineering Guardrails (Minimal Skill Pack)

Apply these rules ONLY for software architecture/coding tasks:

- **SSOT**: One authoritative source per business data/rule.
- **DRY**: Avoid duplicated logic across layers/modules.
- **Components**: Prefer reusable components/modules when it reduces real duplication.
- **Persistence**: Backend/domain is truth for persistent data + business rules; frontend consumes/displays.
- **Simplicity**: Prefer simple solutions; avoid abstraction unless it solves real complexity.
- **Security**: Basic security: validate input, protect secrets/sensitive data.

> [!IMPORTANT]
> If the request is non-software, ignore this skill completely.

## 🛠️ Usage Triggers
This skill is activated when keywords like `code`, `logic`, `refactor`, `architecture`, `backend`, `frontend`, or `schema` are used.
