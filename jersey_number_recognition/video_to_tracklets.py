
import cv2
import torch
from deep_sort_realtime.deepsort_tracker import DeepSort
import os

VIDEO_PATH = "1.mp4"  # Girdi videonuzun yolu
OUTPUT_DIR = "data/SoccerNet/test/images"  # Tracklet görüntüleri buraya kaydedilecek
CONFIDENCE_THRESHOLD = 0.4

# YOLOv5 modelini yükle (GPU destekli)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.conf = CONFIDENCE_THRESHOLD
model.to('cuda')

# DeepSORT tracker
tracker = DeepSort(max_age=30)

# Video okuma
cap = cv2.VideoCapture(VIDEO_PATH)
frame_idx = 0

os.makedirs(OUTPUT_DIR, exist_ok=True)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_idx += 1

    # YOLOv5 ile kişi tespiti
    results = model(frame)
    people = []
    for *box, conf, cls in results.xyxy[0]:
        if int(cls) == 0:  # person sınıfı
            x1, y1, x2, y2 = map(int, box)
            people.append(([x1, y1, x2 - x1, y2 - y1], conf.item(), 'person'))

    # DeepSORT ile takip
    tracks = tracker.update_tracks(people, frame=frame)
    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        l, t, w, h = track.to_ltrb()
        x1, y1, x2, y2 = map(int, [l, t, l + w, t + h])

        # tracklet klasörünü oluştur
        track_dir = os.path.join(OUTPUT_DIR, f"track_{track_id}")
        os.makedirs(track_dir, exist_ok=True)

        # kişinin kırpılmış görüntüsünü kaydet
        crop = frame[y1:y2, x1:x2]
        if crop.size != 0:
            out_path = os.path.join(track_dir, f"frame_{frame_idx}.jpg")
            cv2.imwrite(out_path, crop)

    print(f"Frame {frame_idx} işlendi.")

cap.release()
print(f"✅ Tracklet kırpmaları tamamlandı. Kayıt klasörü: {OUTPUT_DIR}")
