# Secret Yönetimi Politikası

> Bu dosya proje içindeki hassas verilerin (API keys, passwords, tokens) yönetim kurallarını tanımlar.

---

## 🔐 Temel Kurallar

1. **Asla Hardcode Yapma**
   - Şifreler, API anahtarları, tokenlar kod içinde olmamalı
   - `.env` dosyası kullan

2. **Git'e Commit Etme**
   - `.env` dosyası `.gitignore`'da olmalı
   - `docs/project_keys.md` gitignore'da olmalı

3. **Environment-Based Injection**
   ```bash
   # Production'da
   export DB_PASSWORD="xxx"
   export API_KEY="yyy"
   ```

---

## 📁 Dosya Hiyerarşisi

| Dosya | Amaç | Git'te |
|-------|------|--------|
| `.env` | Local development secrets | ❌ Hayır |
| `.env.example` | Template (değerler boş) | ✅ Evet |
| `docs/project_keys.md` | Audit için key listesi | ❌ Hayır |

---

## 🔄 Rotation Policy

| Secret Tipi | Rotation Süresi |
|-------------|-----------------|
| API Keys | 90 gün |
| Database passwords | 180 gün |
| JWT secrets | 30 gün |
| OAuth tokens | 7 gün |

---

## 🛡️ Access Control

```yaml
# Kimlerin secrets'a erişimi var
access:
  admin:
    - read
    - write
    - rotate
  developer:
    - read (only dev env)
  ci_cd:
    - read (injected at runtime)
```

---

## 🔍 Audit

`secret_scanner.py` düzenli olarak çalıştırılmalı:
```bash
python3 .agent/skills/enterprise-security/scripts/secret_scanner.py
```

Çıktı: `docs/project_keys.md`

---

## ⚠️ Vault Entegrasyonu (Opsiyonel)

Production ortamlar için HashiCorp Vault önerilir:

```python
import hvac

client = hvac.Client(url='https://vault.example.com')
secret = client.secrets.kv.read_secret_version(path='myapp/db')
password = secret['data']['data']['password']
```

---

> **NOT:** Bu dosyadaki kurallara uymayan kod PR'larda reddedilmelidir.
