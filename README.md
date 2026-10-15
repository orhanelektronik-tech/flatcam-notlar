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
