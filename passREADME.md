# Futbol Pas Analizi

Bu proje, futbol maçlarındaki 2D taktik harita görüntülerini kullanarak pasları, top sahipliğini ve oyuncu hareketlerini tespit edip takip eder. Sistem, bilgisayarlı görü teknikleriyle takımlardaki oyuncuları forma renklerine göre tanımlar, topu takip eder ve pas olaylarını kaydeder.

## Özellikler

- **Takım Tespiti**: İki takımın oyuncularını forma renklerine göre (sarı ve mor/mavi) tespit eder
- **Top Takibi**: Beyaz topu kareler arasında tespit eder ve izler
- **Pas Tespiti**: Aynı takım oyuncuları arasındaki pasları tespit eder
- **Sahiplik Değişimleri**: Topun takımlar arasında el değiştirmesini tespit eder
- **Oyuncu Sürüşü**: Bir oyuncunun topu sürdüğü durumları tanır
- **Hız Analizi**: Farklı hareket türleri için top hızını hesaplar
- **Bölge Analizi**: Olayları sahanın farklı bölgelerine göre eşleştirir
- **Görselleştirme**: Pasların ve top sahipliğinin ısı haritalarını ve hareket grafiklerini oluşturur

## Gereksinimler

- Python 3.6+
- OpenCV (`cv2`)
- NumPy
- Matplotlib
- tqdm
- JSON

## Kurulum

```bash
pip install opencv-python numpy matplotlib tqdm
```

## Kullanım

1. Google Colab'da çalıştırma:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

2. Video ve parametreleri ayarlama:
   ```python
   VIDEO_PATH = "/content/drive/MyDrive/videos_bein_sports/outputs/last_2023-2024_11_fraport-tav-antalyaspor_besiktas.mp4"
   JSON_PATH = "/content/drive/MyDrive/videos_bein_sports/betul/pass_analysis_simple.json"
   BALL_POSSESSION_THRESHOLD = 60
   START_FRAME = 0
   MAX_FRAMES = None  # None = tüm videoyu işle
   ```

3. Analizi çalıştırma:
   ```python
   # Harita bölgesini otomatik tespit et
   MAP_REGION = auto_detect_map_region(VIDEO_PATH)
   
   # Geliştirilmiş analizi çalıştır
   IMPROVED_JSON_PATH = JSON_PATH.replace('.json', '_improved.json')
   pass_events = analyze_passes_from_2d_map_improved(
       input_video_path=VIDEO_PATH,
       output_json_path=IMPROVED_JSON_PATH,
       start_frame=START_FRAME,
       max_frames=MAX_FRAMES,
       ball_possession_threshold=BALL_POSSESSION_THRESHOLD,
       map_region=MAP_REGION
   )
   
   # Sonuçları analiz et
   analyze_json_data_improved(IMPROVED_JSON_PATH)
   ```

## Renk Ayarları

Kodda, takımları ve topu renk uzayında tespit etmek için HSV değerleri kullanılır. Bu değerler her video için farklı olabilir ve gerektiğinde ayarlanabilir:

```python
# Sarı oyuncular (Takım 1)
YELLOW_LOWER = np.array([20, 40, 40])
YELLOW_UPPER = np.array([40, 255, 255])

# Mor oyuncular (Takım 2)
PURPLE_LOWER = np.array([130, 30, 30])
PURPLE_UPPER = np.array([170, 255, 255])

# Beyaz top
WHITE_LOWER = np.array([0, 0, 180])
WHITE_UPPER = np.array([180, 50, 255])

# Mavi hakemler
BLUE_LOWER = np.array([100, 80, 80])
BLUE_UPPER = np.array([130, 255, 255])
```

## Çıktılar

Program aşağıdaki çıktıları üretir:

1. **JSON Dosyası**: Tüm tespit edilen pas, sürme ve top değişimi olaylarının detaylarını içerir
2. **Debug Videosu**: Tespit edilen oyuncuları, topu ve olayları gösteren işaretli video
3. **Pas Haritası**: Sahadaki pas dağılımını gösteren görsel
4. **Bölge Analizi Grafiği**: Sahanın farklı bölgelerindeki pas ve sürme sayılarını gösteren bar grafikleri
5. **Hız Analizi Grafiği**: Top hızı dağılımını gösteren histogram

## Fonksiyonlar

- `auto_detect_map_region`: Videodaki 2D harita bölgesini otomatik tespit eder
- `detect_objects_by_color`: Belirli renkteki nesneleri tespit eder
- `detect_ball_with_motion`: Hareket ve renk bilgisini kullanarak topu tespit eder
- `analyze_passes_from_2d_map_improved`: Geliştirilmiş pas analizi yapar
- `create_pass_map_improved`: Pas ve sürme hareketlerinin görsel haritasını oluşturur
- `analyze_json_data_improved`: JSON verilerini analiz edip istatistikler çıkarır

## Uyarılar ve İpuçları

- Program, BeIN Sports maç yayınlarındaki 2D taktik haritaları için optimize edilmiştir
- Farklı yayıncılar veya farklı renklerdeki formalar için renk aralıklarının ayarlanması gerekebilir
- Renk tespitinde sorun yaşanırsa `test_color_detection` fonksiyonu ile renk aralıklarını test edebilirsiniz
- Top tespitinde sorun olursa, farklı tespit algoritmalarını birleştiren `detect_ball_with_combined_features` fonksiyonunu kullanabilirsiniz
