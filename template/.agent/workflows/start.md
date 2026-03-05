---
description: start - Dokümanlara göre projenin fiziksel altyapısını ve projeyi kurar.
---

# 🚀 Otonom Proje Kurulumu (/start)

> ⚠️ **GATEKEEPER BAĞLANTISI:** Bu işlem terminalde dosya ve klasör oluşturma/silme/indirme işlemleri yapacağı için kullanıcı onayı (Gatekeeper) ZORUNLUDUR.

Bu workflow, daha önce `/temel` komutuyla veya manuel olarak doldurulmuş olan mimari belgelere (özellikle `docs/tech_stack.md` ve `docs/architecture.md`) bakarak projenin fiziksel iskeletini ve bağımlılıklarını bilgisayarınıza kurar.

---

## Aşama 1: Analiz ve Hazırlık

1. **SSOT Kontrolü:** `docs/tech_stack.md` ve `docs/architecture.md` dosyalarını `view_file` ile oku.
2. Eğer bu dosyalar boş şablon halinde veya hiç yoksa, kullanıcıya "Önce `/temel` komutuyla veya manuel olarak `docs/prd.md`, `docs/tech_stack.md` gibi dosyaları doldurmamız gerekiyor" diyerek işlemi durdur.
3. Bu dosyalardaki seçilmiş dilleri, framework'leri (örn: React, Next.js, Django, Express vb.), paket yöneticilerini (npm, pip, yarn vb.) ve linter/formatter/test araçlarını tespit et.

## Aşama 2: Komut Planlaması ve Güvenlik Onayı

1. Analiz edilen teknoloji yığınına göre çalıştırılması gereken terminal komutlarını **adım adım hazırla** (Örn: `npm create vite@latest . -- --template react-ts`, `npm install`, `pip install -r requirements.txt` vb.).
2. Eğer proje dizininde önceden oluşturulmuş çakışacak dosyalar varsa, bunları ne yapacağınızı planlayın. Bulunulan dizinde (`./`) projenin kurulmasını sağlayın. Yeni bir alt klasör oluşturmak yerine (eğer mimaride özellikle belirtilmemişse) doğrudan repo köküne kurmayı hedefleyin (örn: `npx create-next-app@latest .`).
3. Çalıştırılacak TÜM komutları bir liste halinde kullanıcıya sun (örn: "Şu komutları çalıştırarak projeyi ayağa kaldıracağım: 1... 2... 3...").
4. Bu işlemleri gerçekleştirmek için kullanıcıdan **AÇIK ONAY** (Gatekeeper) iste.
5. Kullanıcı "evet/onay" diyene kadar **ASLA** komut çalıştırma (`run_command` kullanma).

## Aşama 3: Fiziksel Kurulum (Execution)

Kullanıcı onayı alındıktan sonra:

1. Listelediğin kurulum komutlarını terminalde sırayla çalıştır (`run_command` aracı ile).
2. Beklenmeyen bir hata çıkarsa, problemi analiz edip (gerekirse internet araması veya `grep_search` kullanarak) çözmeye çalış ve gerekirse kullanıcıyı bilgilendir.
3. Eğer belirli klasör yapılarının manuel olarak oluşturulması gerekiyorsa (`mkdir -p src/components/ui`, `touch src/utils/constants.ts` gibi), bu komutları da çalıştırarak `docs/architecture.md`'deki hedeflenen dizin yapısını inşa et.
4. Gerekli env dosyası şablonlarını oluştur (`.env.example` gibi). Asla gerçek şifreleri (`secret_policy.md` kuralları gereği) kod içine gömme.

## Aşama 4: Raporlama ve Sonuç

1. Kurulum tamamen bittikten sonra, eğer frontend uygulamasını kaldırmak için bir komut gerekiyorsa (örn: `npm run dev`), terminali meşgul etmeden arka plana atacak şekilde çalıştırmayı (opsiyonel olarak) dene veya kullanıcıya bilgi ver.
2. İşlem tamamlandığında `notify_user` kullanarak işlemi başarıyla tamamladığını bildir. Ortaya çıkan fiziksel yapının `tech_stack.md` ile birebir eşleştiğini teyit et.
3. Çalışmaya başlayabileceğiniz ilk `task` veya feature için hazırsanız kullanıcıya sor.
