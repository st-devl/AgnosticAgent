# Yeni Feature Tamamlama Raporu

✅ FEATURE TAMAMLANDI: {{ feature_name }}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 OLUŞTURULAN KONTRATLAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{% for contract in contracts %}
[{{ contract.operation }}@{{ contract.version }}] → {{ contract.path }}
{% endfor %}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️ BACKEND DOSYALAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{% for file in backend_files %}
[{{ file }}]
{% endfor %}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎨 FRONTEND DOSYALAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{% for file in frontend_files %}
[{{ file }}]
{% endfor %}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧪 TEST SENARYOLARI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{% for scenario in test_scenarios %}
[{{ scenario }}]
{% endfor %}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 GÜNCELLENMİŞ DOKÜMANTASYON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 contracts/registry.json [x]
 docs/registry.md [x]
 CHANGELOG.md [x]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 KULLANICI AKIŞI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{{ user_flow }}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ ENTEGRASYON DOĞRULAMA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Checklist sonuçları]
