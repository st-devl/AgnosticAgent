---
description: Projedeki prd.md içeriğini okuyup diğer tüm docs/*.md şablonlarını otonom olarak doldurur.
---

Bu komut sayesinde, `docs/prd.md` dosyasındaki ürün gereksinimleri analiz edilecek ve projenin diğer temel dokümanları (`tech_stack.md`, `architecture.md`, `project_brief.md`, `design_brief.md`, `data_privacy.md`, `secret_policy.md`, `memory.md`, `decision_log.md` vb.) otonom olarak doldurulacaktır. 

Aşağıdaki adımları ÇOK SIKI bir şekilde takip et:

1. **SSOT (Single Source of Truth) Analizi:**
   - İlk olarak `docs/prd.md` dosyasını `view_file` aracıyla oku ve içeriği bütünüyle analiz et.
   - PRD'de belirtilen özellikleri, teknolojileri, kullanıcı hikayelerini ve diğer tüm gereksinimleri iyice anla.

2. **Doldurulacak Hedeflerin Belirlenmesi:**
   - `docs/` klasörünü `list_dir` ile listele ve içindeki tüm `.md` dosyalarını tespit et.

3. **Dokümanların Tek Tek Otonom Doldurulması:**
   - Her bir dokümanı sırayla ele al.
   - O dokümanın amacına uygun olarak (örn. `tech_stack.md` için kullanılacak teknolojiler, diller, framework'ler; `architecture.md` için dizin yapısı ve yazılım kalıpları; `project_brief.md` için genel proje özeti vb.) PRD'den çektiğin bağlamı kullanarak dokümanı doldur.
   - Dokümanları doldururken `multi_replace_file_content` veya `write_to_file` araçlarıyla ilgili `.md` dosyalarını baştan aşağı güncelle. Eğer şablon (template) bilgileri varsa onları silip kendi ürettiğin gerçek bilgilerle değiştir.
   - Eğer PRD'de eksik olan ancak standart bir projede olması gereken bazı detaylar (örn. default güvenlik politikaları) varsa, en iyi uygulamalara (best-practices) uygun olarak bunları sen belirle ve belgelere ekle.

4. **Kapsam Kontrolü (Checklist):**
   - Aşağıdaki dokümanların tümünün GÜNCELLENDİĞİNDEN kesinlikle emin ol:
     - `tech_stack.md`
     - `architecture.md`
     - `project_brief.md`
     - `design_brief.md`
     - `data_privacy.md`
     - `secret_policy.md`
     - `decision_log.md`
     - `memory.md`
   - Hiçbir dosyayı SAKIN es geçme! Asla kısmen bırakma. Başlıkları ve içini projeye göre dolu dolu yaz.

5. **Kullanıcıya Bildirim:**
   - Tüm dokümanlar başarıyla güncellendikten sonra kullanıcıya `notify_user` kullanarak işlemi başarıyla tamamladığını ve projenin yeni bir mimari anayasaya kavuştuğunu bildir. 
   - Kullanıcıya, fiziksel proje dosyalarını kurabilmesi için bir sonraki adım olan `/start` komutunu çalıştırabileceğini hatırlat.
