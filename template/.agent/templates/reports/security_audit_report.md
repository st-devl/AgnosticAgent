# Güvenlik Denetim Raporu

## Özet
Kritik Bulgu Sayısı: {{ critical_count }}
Yüksek Riskli Bulgu Sayısı: {{ high_count }}

## Bulgular
| Kategori | Seviye | Açıklama |
|----------|--------|----------|
{% for finding in findings %}
| {{ finding.category }} | {{ finding.level }} | {{ finding.description }} |
{% endfor %}

## Güvenlik Task Listesi
- [ ] KRITIK: ...
- [ ] YÜKSEK: ...
