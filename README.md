# Footy Insights

Bu döküman, projenin dizin yapısını ve her klasör/dosyanın hangi aşamada kullanıldığını, ne işe yaradığını özetler.

## 📂 Proje Yapısı

Proje, çeşitli modüller ve işlem adımlarından oluşmaktadır. Her bir bileşenin fonksiyonu aşağıda detaylı olarak açıklanmıştır:
Veri Toplama & İşleme

downloadMatchDetailsDataset/

Aşama: Veri toplama
İçerik: TFF web sitesinden maç meta-verilerini (takımlar, tarih, skor vb.) çeken ve JSON olarak kaydeden script'ler.


VideoDataset/

Aşama: Video indirme
İçerik: BeIN Sports web scraping ile maç özet videolarının URL'lerini bulup indiren kodlar.



Görsel Analiz

video_processingf_faz1.py

Aşama: Temel video işleme
İçerik: OpenCV tabanlı; oyuncu, kaleci, hakem ve top tespiti, takım sınıflandırması ve 2D saha haritası oluşturma.


team_classifier/

Aşama: Takım clustering
İçerik: Oyuncuları saha konumlarına göre 0/1 etiketleriyle iki kümeye ayıran UMAP ve SIGLIP tabanlı sınıflandırıcı kodları.


Team_identification/

Aşama: Takım tespiti denemeleri
İçerik: Forma renklerinden ve görüntülerden takım belirleme sürecinde kullanılan kod. Sonuç alınamadı.


jersey_number_recognition/ & paddleocr_forma/

Aşama: Forma numarası okuma
İçerik: Forma üzerindeki numaraları OCR ile okumayı deneyen farklı yaklaşımlar. Sonuç alınamadı.



Olay Tespiti

ballAndEventAction/

Aşama: Olay detection
İçerik: Maçtaki olayları (pas, şut, gol vb.) ve top durumunu tespit eden SoccerNet tabanlı modellerin kodları.


pass.ipynb

Aşama: Pas analizi
İçerik: Object tracking ile pasları ve hangi iki oyuncu arasında olduğunu tespit eden Jupyter Notebook.


Position_Transition_Detection/

Aşama: Gol öncesi/sonrası pozisyon geçiş tespiti
İçerik: Skor tabelasını OCR ile okuyup pozisyon başlangıç-bitişlerini tespit eden kodları içerir.


goal_validation/

Aşama: Gol doğrulama
İçerik: OCR ile skor tabelasından okunan veriler ve TFF gollerini karşılaştırarak gol tespit doğruluğunu artıran kodlar.


kritik_pozisyon_tespiti/

Aşama: Kritik gol kaçırma tespiti
İçerik: Kale direğinden dönen pozisyonları algılayıp işaretleyen kodlar.



Dil İşleme ve Ses Entegrasyonu

NLP-TTS-STT/

Aşama: Deneme
İçerik: Konuşma-metin (STT) ve metin-konuşma (TTS) modelleri üzerine çeşitli çalışmaları barındırır. Son üründe kullanılmadı.


TTS-final/

Aşama: Son TTS entegrasyonu
İçerik: Projenin nihai seslendirme (Text-to-Speech) aşamasında kullanılan kodlar.


bark_voice_clone/

Aşama: Ses klonlama denemesi
İçerik: Bark tabanlı ses klonlama prototipi; proje sonunda kullanılmadı.



Veri Entegrasyonu ve Kullanıcı Arayüzü

merge_last/

Aşama: LLM girdi hazırlık
İçerik: Farklı aşamalardan gelen JSON çıktıları birleştirip, modele beslemeden önceki son temizleme ve formatlama adımı.


footy-insights-app/

Aşama: Kullanıcı arayüzü
İçerik: React.js tabanlı web uygulaması; video yükleme, analiz sonuçlarını gösterme ve spiker yorumlarını dinleme ekranları.



Teknolojik Altyapı
Proje kapsamında kullanılan temel teknolojiler:

Bilgisayarlı Görü: OpenCV, objekt tespiti ve takip
Derin Öğrenme: SoccerNet modelleri (futbol olaylarının tespiti için)
Kümeleme ve Sınıflandırma: UMAP ve SIGLIP (takım sınıflandırması için)
OCR: PaddleOCR (skor tabelası okuma ve forma numarası tanıma denemeleri)
Web Teknolojileri: React.js (kullanıcı arayüzü)
NLP ve Ses: Text-to-Speech teknolojileri

---
