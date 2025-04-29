# Footy Insights

Bu döküman, projenin dizin yapısını ve her klasör/dosyanın hangi aşamada kullanıldığını, ne işe yaradığını özetler.
<br>


## 📂 Proje Yapısı

Proje, çeşitli modüller ve işlem adımlarından oluşmaktadır. Her bir bileşenin fonksiyonu aşağıda detaylı olarak açıklanmıştır:
<br>

**Veri Toplama & İşleme**

- **downloadMatchDetailsDataset/** <br>
***Aşama:*** Veri toplama <br>
***İçerik:*** TFF web sitesinden maç meta-verilerini (takımlar, tarih, skor vb.) çeken ve JSON olarak kaydeden script'ler.

- **VideoDataset/** <br>
***Aşama:*** Video indirme <br>
***İçerik:*** BeIN Sports web scraping ile maç özet videolarının URL'lerini bulup indiren kodlar.
<br>

**Oyuncu Takibi, Takım Sınıflandırılması**

- **video_processingf_faz1.py** <br>
***Aşama:*** Temel video işleme <br>
***İçerik:*** OpenCV tabanlı; oyuncu, kaleci, hakem ve top tespiti, takım sınıflandırması ve 2D saha haritası oluşturma.

- **team_classifier/** <br>
***Aşama:*** Takım clustering <br>
***İçerik:*** Oyuncuları saha konumlarına göre 0/1 etiketleriyle iki kümeye ayıran UMAP ve SIGLIP tabanlı sınıflandırıcı kodları.

- **Team_identification/** <br>
***Aşama:*** Takım tespiti denemeleri <br>
***İçerik:*** Forma renklerinden ve görüntülerden takım belirleme sürecinde kullanılan kod. Sonuç alınamadı.

- **jersey_number_recognition/** <br>
  **paddleocr_forma/** <br>
***Aşama:*** Forma numarası okuma <br>
***İçerik:*** Forma üzerindeki numaraları OCR ile okumayı deneyen farklı yaklaşımlar. Sonuç alınamadı.
<br>

**Olay Tespiti**

- **ballAndEventAction/** <br>
***Aşama:*** Olay detection <br>
***İçerik:*** Maçtaki olayları (pas, şut, gol vb.) ve top durumunu tespit eden SoccerNet tabanlı modellerin kodları.

- **pass.ipynb** <br>
***Aşama:*** Pas analizi <br>
***İçerik:*** Object tracking ile pasları ve hangi iki oyuncu arasında olduğunu tespit eden Jupyter Notebook.

- **Position_Transition_Detection/** <br>
***Aşama:*** Gol öncesi/sonrası pozisyon geçiş tespiti <br>
***İçerik:*** Skor tabelasını OCR ile okuyup pozisyon başlangıç-bitişlerini tespit eden kodları içerir.

- **goal_validation/** <br>
***Aşama:*** Gol doğrulama <br>
***İçerik:*** OCR ile skor tabelasından okunan veriler ve TFF gollerini karşılaştırarak gol tespit doğruluğunu artıran kodlar.

- **kritik_pozisyon_tespiti/** <br>
***Aşama:*** Kritik gol kaçırma tespiti <br>
***İçerik:*** Kale direğinden dönen pozisyonları algılayıp işaretleyen kodlar.
<br>

**Dil İşleme ve Ses Entegrasyonu**

- **NLP-TTS-STT/** <br>
***Aşama:*** NLP, TTS, STT üzerine deneme amaçlı üzerinde çalışılmış kodlar <br>
***İçerik:*** Konuşma-metin (STT) ve metin-konuşma (TTS) modelleri üzerine çeşitli çalışmaları barındırır. Son üründe kullanılmadı.

- **TTS-final/** <br>
***Aşama:*** Son TTS entegrasyonu <br>
***İçerik:*** Projenin nihai seslendirme (Text-to-Speech) aşamasında kullanılan kodlar.

- **bark_voice_clone/** <br>
***Aşama:*** Ses klonlama denemesi <br>
***İçerik:*** Bark tabanlı ses klonlama prototipi; proje sonunda kullanılmadı.
<br>

**Veri Entegrasyonu ve Kullanıcı Arayüzü**

- **merge_last/** <br>
***Aşama:*** LLM girdi hazırlık <br>
***İçerik:*** Farklı aşamalardan gelen JSON çıktıları birleştirip, modele beslemeden önceki son temizleme ve formatlama adımı.

- **footy-insights-app/** <br>
***Aşama:*** Kullanıcı arayüzü <br>
***İçerik:*** React.js tabanlı web uygulaması; video yükleme, analiz sonuçlarını gösterme ve spiker yorumlarını dinleme ekranları.
<br>


## 💻 Teknolojik Altyapı

Proje kapsamında kullanılan temel teknolojiler:

- **Bilgisayarlı Görü:** OpenCV, objekt tespiti ve takip
- **Derin Öğrenme:** SoccerNet modelleri (futbol olaylarının tespiti için)
- **Kümeleme ve Sınıflandırma:** UMAP ve SIGLIP (takım sınıflandırması için)
- **OCR:** PaddleOCR (skor tabelası okuma ve forma numarası tanıma denemeleri)
- **Web Teknolojileri:** React.js (kullanıcı arayüzü)
- **NLP ve Ses:** Text-to-Speech teknolojileri
<br>


## 🦾 Katkıda Bulunanlar
- Hayrettin Kaan Özsoy - *Project Manager*
  - Email: hkaanozsoy@gmail.com
- Ali Şahin - *Team Member*
  - Email: alisahin7601@gmail.com
- Alperen Tolga Karaçam - *Team Member*
  - Email: alperentolgakaracam@gmail.com
- Betül Biçer - *Team Member*
  - Email: betul.bicer@icloud.com
- İlayda Uysal - *Team Member*
  - Email: uysalilayda0212@gmail.com
<br>


## 📌 Referanslar

- **SoccerNet:** A Scalable Dataset for Action Spotting in Soccer Videos (https://arxiv.org/abs/1804.04527)

