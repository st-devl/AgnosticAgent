---
description: start - Dokümanlara göre projenin fiziksel altyapısını ve projeyi kurar.
---

# 🚀 Proje İnşa Protokolü (/start)

Bu komut, `docs/` klasöründeki belgelere (özellikle `tech_stack.md` ve `architecture.md`) dayalı olarak projenin fiziksel altyapısını otonom bir şekilde kurar. Gerekli paket yöneticileri çalıştırılır, framework iskeleti oluşturulur ve proje dosyaları ayağa kaldırılır.

> ⚠️ **UYARI:** Bu komut terminal terminal ortamında (`run_command`) çalışmasını gerektirir. Kullanıcıdan mutlaka GATEKEEPER onayı al.

Aşağıdaki adımları sırayla izle:

1. **Bağlam ve Strateji Okuma:**
   - `docs/tech_stack.md` ve `docs/architecture.md` dosyalarını `view_file` ile oku.
   - Projenin ana teknolojilerini tespit et (Örn: React, Vue, Next.js, Node.js, Python FastAPI, Laravel vb.).
   - Hangi paket yöneticisinin kullanılacağını sapta (npm, pnpm, yarn, bun, pip, composer vb.).

2. **Kurulum Planı (Komut Haritası) Çıkarma:**
   - Okuduğun standartlara göre çalıştırılacak fiziksel komutların kesin bir listesini oluştur.
   - Örnek Frontend: `npx create-next-app@latest .` veya `npm create vite@latest . -- --template react-ts`
   - Örnek Backend Python: `python3 -m venv .venv`, `source .venv/bin/activate`, `pip3 install -r requirements.txt` vb.
   - Ana klasör yapısına göre oluşturulacak dizinleri planla (`mkdir src/components`, `mkdir api/routes` vb.).

3. **Kullanıcı Onayı (Checkpoint):**
   - Planladığın tüm komut listesini ve oluşturulacak yapıyı kullanıcıya şeffaf bir şekilde sun.
   - `notify_user` kullanarak "Fiziksel proje kurulumunu başlatmak için plan onaylıyor musunuz?" diye sor.
   - KULLANICI ONAYI OLMADAN HİÇBİR TERMİNAL KOMUTU VEYA FİZİKSEL DOSYA SİLME İŞLEMİ YAPMA.

4. **Fiziksel İnşaat (Execution):**
   - Kullanıcı onay verdikten sonra, `run_command` ile belirlediğin komutları sıraraya çalıştır.
   - Paketlerin inmesini bekle, hatalarla karşılaşırsan logları okuyup (`command_status`) çöz.
   - Ek olarak projenin `architecture.md`'ye tam uyması için eksik klasörleri manuel `mkdir` ile aç veya eksik .config dosyalarını `write_to_file` aracıyla oluştur.

5. **Son Kontrol ve Devir Teslim:**
   - Uygulama iskeletinin hatasız çalıştığını test et (Örn. package.json veya .venv geldi mi kontrol et).
   - Kullanıcıya başarı mesajı ver: "Uygulama çatıları kuruldu! Kod yazmaya hazırız."
