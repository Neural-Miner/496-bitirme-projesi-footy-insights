Futbol Maçı Video Analizi
Bu proje, futbol maçı videolarını analiz ederek oyuncuları, kalecileri, hakemleri ve topu tespit eden, takım sınıflandırması yapan ve bir 2D saha haritası oluşturan bir sistemdir.
1. Nesne Tespiti (Object Detection)
Sistem, önceden eğitilmiş bir derin öğrenme modeli kullanarak video karelerindeki nesneleri tespit eder.
Temel Özellikler:

Çoklu Sınıf Tespiti: Sistem 4 farklı kategoriyi ayırt eder:

BALL_ID = 0: Futbol topu
GOALKEEPER_ID = 1: Kaleciler
PLAYER_ID = 2: Saha oyuncuları
REFEREE_ID = 3: Hakemler


Güven Eşiği: Tespitler confidence_threshold=0.3 değerinin üzerindeki güven skorlarıyla filtrelenir.
NMS (Non-Maximum Suppression): Örtüşen tespitler threshold=0.5 eşiği ile elenir.
Özel İşlemler:

Top tespitlerinin görünürlüğünü artırmak için 10 piksellik dolgu eklenir.
Saha köşe noktaları confidence>0.5 eşiği ile tespit edilir.



2. Nesne Takibi (Object Tracking)
Sistem, frame'ler arasında nesneleri tutarlı bir şekilde takip etmek için ByteTrack algoritmasını kullanır.
Temel Özellikler:

ByteTrack Algoritması: Varsayılan parametrelerle nesne takibi sağlar.
Takım Sınıflandırması: Oyuncular için takım sınıflandırması yapılır (Sarı ve Mavi takım).
Kaleci Takım Ataması: Her frame için tekrar hesaplanır:
pythondef resolve_goalkeepers_team_id(players_detections, goalkeepers_detections):
    # Kalecilerin çevresindeki en yakın 3 oyuncunun çoğunluk takımına atama yapar

Dinamik Güncelleme: Her frame'de takip ve sınıflandırma yenilenir, bu da anlık hatalar olsa bile uzun vadede tutarlı takip sağlar.

3. 2D Saha Haritası (2D Pitch Mapping)
Sistem, tespit edilen nesneleri gerçek görüntüden 2D saha haritasına aktarır.
Temel Özellikler:

Perspektif Dönüşümü: En az 4 saha köşe noktası kullanılarak görüntüden saha koordinatlarına dönüşüm yapılır:
pythontransformer = ViewTransformer(
    source=frame_reference_points,
    target=pitch_reference_points
)

Renk Kodlaması:

Sarı Takım: #FFFF00
Mavi Takım: #00BFFF
Top: #FF00FF (Mor)
Hakemler: #FF69B4 (Pembe)


Görselleştirme: Orijinal video ve 2D saha haritası yan yana birleştirilerek gösterilir.

Kullanım
Proje şu parametrelerle çalıştırılabilir:
pythonprocess_soccer_video(
    source_video_path=SOURCE_VIDEO_PATH,
    output_video_path=OUTPUT_VIDEO_PATH,
    start_frame=0,      
    max_frames=4000,    # İşlenecek frame sayısı
    confidence_threshold=0.3,
    training_stride=30, # Eğitim için her 30 frame'de bir örnek
    training_frames=50  # Eğitim için kullanılacak frame sayısı
)
Gereksinimler

OpenCV
NumPy
Supervision
Matplotlib
PyTorch (nesne tespit modelleri için)