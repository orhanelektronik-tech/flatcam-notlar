# FlatCAM 8.994 Notları (TB2EOS)

FlatCAM 8.994 BETA (64 bit) kullanımında karşılaşılan sorunlar ve lazer için bakır temizleme ayarları.

---

## 1. Bakır temizlemede 200 MB dosya / kilitlenme sorunu

**Belirti:** Bakır Temizleme (NCC) çalıştırıldığında 200 MB'ı geçen dosyalar oluşuyor, program kilitleniyor ya da kendi kendine kapanıyor.

**Sebep:** Gerber'deki gereksiz detay (özellikle EAGLE polygon / bakır dökümü alanlarının binlerce küçük çizgi olarak çıkması) çok büyük geometri üretiyor.

**Çözüm (denendi, çalıştı: 200 MB → 300 KB, takılma yok):**

1. `Seçenekler → Ayarlar → GERBER` sekmesi
2. **Gerber Genel → Daire Adımı:** 16 (64 yerine 16–32)
3. **Gerber Gelişmiş Seçenekleri → "Basitleştir"** kutucuğunu işaretle (İngilizce: *Simplify*)
4. **Hata Payı** (İngilizce: *Tolerance*): `0,0050` (karmaşık kartlarda `0,0100`'e kadar)
   - Pedlerde / ince yollarda köşeler fazla düz çıkarsa `0,0030`'a düşür.
5. **Uygula → Kaydet**
6. **Önemli:** Ayar sadece Gerber açılırken uygulanır. Yüklü Gerber'leri silip yeniden aç.

### Diğer kontrol edilecekler
- NCC yöntemi: **Çizgi Bazlı (Lines)** — "Seed" ve "Combo" çok ağır.
- Üst Üste Gelme (overlap) çok yüksek olmasın (%80–90 geometriyi patlatır).
- Tüm kartı çok ince uçla temizleme; gerekirse büyük uç + ince uç ile **Kalan Parça İşleme** (Rest Machining).
- Pay (margin) büyükse gereksiz geniş alan temizlenir.
- Büyük geometri objelerinde "Göster/Plot" kutucuğunu kapatmak arayüzü rahatlatır.
- 64 bit sürüm kullan.
- Alternatif: Tam bakır temizleme yerine Yalıtım aracında 2–3 geçiş + %10–20 bindirme.

---

## 2. Bakır Temizleme seçenekleri ne işe yarar?

| Türkçe | İngilizce | Açıklama | Öneri |
|---|---|---|---|
| **Birleştir** | Connect | Temizleme çizgilerini ucu kaldırmadan, alan içinden düz çizgilerle bağlar. Daha az kalkma/inme, daha kısa G-code. | ✔ Açık |
| **Kenar** | Contour | En sonda temizlenen alanın sınırları boyunca bir tur atar; Lines yönteminin bıraktığı testere dişi kalıntıları temizler. | ✔ Açık |
| **Hizala** | Offset | Temizlemenin bakır yol/pedlerden ne kadar uzak duracağı (Hizalama Değeri). Uç salgılıysa veya yollar ince çıkıyorsa kullanılır. | ✘ Kapalı (gerekirse 0,05–0,1 mm) |

---

## 3. Lazer için Bakır Temizleme ayarları (lazer ışın çapı 0,1 mm)

| Ayar | Önerilen | Not |
|---|---|---|
| Uç Kalınlığı | **0,1** | Lazer ışın çapı |
| Uç Tipi | **Dairesel** | Lazerde V-Şekli kullanılmaz |
| Z Derinliği | **0,0000** | Lazerde Z inmesine gerek yok |
| Freze Tipi / Uç Sırası | Fark etmez | Lazerde etkisi yok |
| Üst Üste Gelme | **%15–20** | %5 az; çizgiler arasında yanmamış şerit kalabilir |
| Pay | **0,0000** | |
| Yöntem | **Çizgi Bazlı** | |
| Birleştir | **✔** | Bağlantı çizgileri alan içinden geçer, bakırı yakmaz |
| Kenar | **✔** | Lazerde özellikle önemli |
| Hizala | **✘** veya **0,02–0,03** | Lazer yanığı yolları inceltiyorsa aç |
| Kalan Parça İşleme | **✘** | Tek uç kullanıldığı için gerek yok |
| Uygunluğu Kontrol Et | **✔** | |

### CNC İş nesnesi (G-code üretimi)
- **Önişlemci:** `GRBL_laser` — Z hareketi yapmaz, lazeri M3/M5 + S değeriyle yakar/söndürür. (`GRBL_11_no_M6` freze içindir.)
- **Dönüş hızı** alanı = lazer gücü (S değeri).
- **İlerleme hızı / güç:** malzemeye göre değişir. Kartın boş köşesinde küçük kare ile test et; 1000–1500 mm/dk ile başla, gücü kademeli artır.
- **GRBL:** lazer modu açık olmalı → `$32=1` (kapalıysa her durmada noktasal yanık kalır).
- Boya/toner maskesi yakıp asitle aşındırma yönteminde %15 bindirme yeterli. Doğrudan bakır kaldırma (fiber lazer) için ayarlar farklıdır.

---

## 4. 5,5 W optik (diyot) lazer ile sprey boyalı PCB — F / S başlangıç değerleri

| Ayar | Başlangıç | Aralık |
|---|---|---|
| **F (hız)** | **1500 mm/dk** | 1000–2500 |
| **S (güç)** | **%80** (`$30=1000` ise **S800**) | %60–100 |
| Geçiş sayısı | 1 | Temiz çıkmazsa 2 |
| Mod | M04 (dinamik) | GRBL_laser önişlemcisi bunu kullanır |
| Çizgi aralığı | 0,08 mm | Uç 0,1 mm, %15–20 bindirme |

- **S hesabı:** UGS konsolunda `$$` → `$30` değerine bak (MKS DLC32 / Grbl_ESP32'de genelde 1000). `$30=255` ise %80 = S204.
- **Test:** Kartın boş köşesinde 5×5 mm kareler — hız 1000 / 1500 / 2000 / 2500, güç %60 / %80 / %100. Bakırın parlak çıktığı ve yolların incelmediği **en hızlı** kombinasyonu seç.
  - Boya kalıntısı / kahverengi leke → yavaşla veya gücü artır.
  - Yol/ped kenarları eriyip inceliyor → hızlan veya gücü azalt; gerekirse "Hizala" 0,02–0,03.
- **Odak** çok önemli: kartın üst yüzeyine göre ayarla.
- **Boya:** ince, tek kat **mat siyah** (450 nm'yi iyi emer). Kalın kat temizlenmez, açık renk boya lazeri almaz.
- Bakır ışığı yansıtır, lazer bakıra zarar vermez.
- Aşındırmadan önce kuru bez/fırça ile hafifçe sil; tiner veya alkol kullanma.
- Boya dumanı zehirli: havalandırma + lazer gözlüğü.
- FlatCAM CNC İş nesnesinde: hız → **"İlerleme Hızı X-Y"**, güç → **"Dönüş Hızı"**, önişlemci → **GRBL_laser**.

---

## 5. FlatCAM ayarlarının saklandığı yer (Windows)

Klasör: `C:\Users\<kullanıcı>\AppData\Roaming\FlatCAM\` (FlatCAM'de *Ayarlar → "Ayarlar Klasörünü Aç"* butonu burayı açar)

| Dosya | İçerik |
|---|---|
| `current_defaults.FlatConfig` | **Geçerli tüm ayarlar** (Ayarlar → Kaydet ile yazılır). Yedeklenecek asıl dosya bu. |
| `factory_defaults.FlatConfig` | Fabrika ayarları ("Varsayılanları Geri Yükle" buradan okur) |
| `tools_db.FlatDB` | Uç veritabanı (Tools Database) |
| `recent.json` / `recent_projects.json` | Son açılan dosyalar / projeler |
| `preprocessors\` | Kullanıcı önişlemcileri (FlatCAM kurulum klasöründeki `preprocessors` ile birlikte yüklenir) |

- **Yedek:** `current_defaults.FlatConfig` dosyasını kopyala. Geri yüklemek için FlatCAM kapalıyken yerine koy.
- Dosya JSON biçimindedir, metin editörüyle açılabilir.
- Pencere düzeni / araç çubuğu konumları ayrıca Windows kayıt defterinde (Qt ayarları) tutulur.

---
*73 de TB2EOS*
# FlatCAM 8.994 Notları (TB2EOS)

FlatCAM 8.994 BETA (64 bit) kullanımında karşılaşılan sorunlar ve lazer için bakır temizleme ayarları.

---

## 1. Bakır temizlemede 200 MB dosya / kilitlenme sorunu

**Belirti:** Bakır Temizleme (NCC) çalıştırıldığında 200 MB'ı geçen dosyalar oluşuyor, program kilitleniyor ya da kendi kendine kapanıyor.

**Sebep:** Gerber'deki gereksiz detay (özellikle EAGLE polygon / bakır dökümü alanlarının binlerce küçük çizgi olarak çıkması) çok büyük geometri üretiyor.

**Çözüm (denendi, çalıştı: 200 MB → 300 KB, takılma yok):**

1. `Seçenekler → Ayarlar → GERBER` sekmesi
2. **Gerber Genel → Daire Adımı:** 16 (64 yerine 16–32)
3. **Gerber Gelişmiş Seçenekleri → "Basitleştir"** kutucuğunu işaretle (İngilizce: *Simplify*)
4. **Hata Payı** (İngilizce: *Tolerance*): `0,0050` (karmaşık kartlarda `0,0100`'e kadar)
   - Pedlerde / ince yollarda köşeler fazla düz çıkarsa `0,0030`'a düşür.
5. **Uygula → Kaydet**
6. **Önemli:** Ayar sadece Gerber açılırken uygulanır. Yüklü Gerber'leri silip yeniden aç.

### Diğer kontrol edilecekler
- NCC yöntemi: **Çizgi Bazlı (Lines)** — "Seed" ve "Combo" çok ağır.
- Üst Üste Gelme (overlap) çok yüksek olmasın (%80–90 geometriyi patlatır).
- Tüm kartı çok ince uçla temizleme; gerekirse büyük uç + ince uç ile **Kalan Parça İşleme** (Rest Machining).
- Pay (margin) büyükse gereksiz geniş alan temizlenir.
- Büyük geometri objelerinde "Göster/Plot" kutucuğunu kapatmak arayüzü rahatlatır.
- 64 bit sürüm kullan.
- Alternatif: Tam bakır temizleme yerine Yalıtım aracında 2–3 geçiş + %10–20 bindirme.

---

## 2. Bakır Temizleme seçenekleri ne işe yarar?

| Türkçe | İngilizce | Açıklama | Öneri |
|---|---|---|---|
| **Birleştir** | Connect | Temizleme çizgilerini ucu kaldırmadan, alan içinden düz çizgilerle bağlar. Daha az kalkma/inme, daha kısa G-code. | ✔ Açık |
| **Kenar** | Contour | En sonda temizlenen alanın sınırları boyunca bir tur atar; Lines yönteminin bıraktığı testere dişi kalıntıları temizler. | ✔ Açık |
| **Hizala** | Offset | Temizlemenin bakır yol/pedlerden ne kadar uzak duracağı (Hizalama Değeri). Uç salgılıysa veya yollar ince çıkıyorsa kullanılır. | ✘ Kapalı (gerekirse 0,05–0,1 mm) |

---

## 3. Lazer için Bakır Temizleme ayarları (lazer ışın çapı 0,1 mm)

| Ayar | Önerilen | Not |
|---|---|---|
| Uç Kalınlığı | **0,1** | Lazer ışın çapı |
| Uç Tipi | **Dairesel** | Lazerde V-Şekli kullanılmaz |
| Z Derinliği | **0,0000** | Lazerde Z inmesine gerek yok |
| Freze Tipi / Uç Sırası | Fark etmez | Lazerde etkisi yok |
| Üst Üste Gelme | **%15–20** | %5 az; çizgiler arasında yanmamış şerit kalabilir |
| Pay | **0,0000** | |
| Yöntem | **Çizgi Bazlı** | |
| Birleştir | **✔** | Bağlantı çizgileri alan içinden geçer, bakırı yakmaz |
| Kenar | **✔** | Lazerde özellikle önemli |
| Hizala | **✘** veya **0,02–0,03** | Lazer yanığı yolları inceltiyorsa aç |
| Kalan Parça İşleme | **✘** | Tek uç kullanıldığı için gerek yok |
| Uygunluğu Kontrol Et | **✔** | |

### CNC İş nesnesi (G-code üretimi)
- **Önişlemci:** `GRBL_laser` — Z hareketi yapmaz, lazeri M3/M5 + S değeriyle yakar/söndürür. (`GRBL_11_no_M6` freze içindir.)
- **Dönüş hızı** alanı = lazer gücü (S değeri).
- **İlerleme hızı / güç:** malzemeye göre değişir. Kartın boş köşesinde küçük kare ile test et; 1000–1500 mm/dk ile başla, gücü kademeli artır.
- **GRBL:** lazer modu açık olmalı → `$32=1` (kapalıysa her durmada noktasal yanık kalır).
- Boya/toner maskesi yakıp asitle aşındırma yönteminde %15 bindirme yeterli. Doğrudan bakır kaldırma (fiber lazer) için ayarlar farklıdır.

---
*73 de TB2EOS*
