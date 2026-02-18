# Component Config JSON Şablonları

Bu dosya component-architecture skill'i için referans şablonları içerir.

---

## Kart Config Şablonu

```json
{
  "variant": "default|featured|compact",
  "show_image": true,
  "show_badge": true,
  "badge_text": "Yeni",
  "cta_text": "Devam Et",
  "amounts": [50, 100, 250],
  "allow_custom_amount": true
}
```

---

## Form Fields Config Şablonu

```json
{
  "fields": [
    {
      "name": "field_name",
      "type": "text|email|tel|select|amount_selector|date",
      "label": "Görünen İsim",
      "required": true,
      "validation": "email|min:3|max:100",
      "options": ["opt1", "opt2"],
      "placeholder": "Örnek...",
      "default": null
    }
  ]
}
```

---

## Bağış Sistemi Örnek Config

```json
{
  "id": 1,
  "type": "subscription",
  "title": {"tr": "Aylık Destek", "en": "Monthly Support"},
  "config": {
    "periods": ["monthly", "yearly"],
    "amounts": [100, 250, 500]
  },
  "form_fields": [
    {"name": "name", "type": "text", "required": true},
    {"name": "period", "type": "period_selector", "required": true},
    {"name": "amount", "type": "amount_selector", "required": true}
  ]
}
```

---

## Component Yapısı

```
Components:
├─ x-donation-card :donation="$donation"   # Tüm kartlar
├─ x-donation-modal                        # Tek modal
├─ x-amount-selector                       # Yardımcı
└─ x-period-selector                       # Yardımcı
```
