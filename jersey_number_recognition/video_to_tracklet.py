{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "aa3c2669-1193-4c38-9b8c-93c6e8527a3f",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "✅ 'video_to_tracklets.py' dosyası oluşturuldu.\n"
     ]
    }
   ],
   "source": [
    "import os\n",
    "\n",
    "# video_to_tracklets.py dosyasını oluştur\n",
    "script_code = \"\"\"\n",
    "import cv2\n",
    "import torch\n",
    "from deep_sort_realtime.deepsort_tracker import DeepSort\n",
    "import os\n",
    "\n",
    "VIDEO_PATH = \"1.mp4\"  # Girdi videonuzun yolu\n",
    "OUTPUT_DIR = \"data/SoccerNet/test/images\"  # Tracklet görüntüleri buraya kaydedilecek\n",
    "CONFIDENCE_THRESHOLD = 0.4\n",
    "\n",
    "# YOLOv5 modelini yükle (GPU destekli)\n",
    "model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)\n",
    "model.conf = CONFIDENCE_THRESHOLD\n",
    "model.to('cuda')\n",
    "\n",
    "# DeepSORT tracker\n",
    "tracker = DeepSort(max_age=30)\n",
    "\n",
    "# Video okuma\n",
    "cap = cv2.VideoCapture(VIDEO_PATH)\n",
    "frame_idx = 0\n",
    "\n",
    "os.makedirs(OUTPUT_DIR, exist_ok=True)\n",
    "\n",
    "while True:\n",
    "    ret, frame = cap.read()\n",
    "    if not ret:\n",
    "        break\n",
    "    frame_idx += 1\n",
    "\n",
    "    # YOLOv5 ile kişi tespiti\n",
    "    results = model(frame)\n",
    "    people = []\n",
    "    for *box, conf, cls in results.xyxy[0]:\n",
    "        if int(cls) == 0:  # person sınıfı\n",
    "            x1, y1, x2, y2 = map(int, box)\n",
    "            people.append(([x1, y1, x2 - x1, y2 - y1], conf.item(), 'person'))\n",
    "\n",
    "    # DeepSORT ile takip\n",
    "    tracks = tracker.update_tracks(people, frame=frame)\n",
    "    for track in tracks:\n",
    "        if not track.is_confirmed():\n",
    "            continue\n",
    "\n",
    "        track_id = track.track_id\n",
    "        l, t, w, h = track.to_ltrb()\n",
    "        x1, y1, x2, y2 = map(int, [l, t, l + w, t + h])\n",
    "\n",
    "        # tracklet klasörünü oluştur\n",
    "        track_dir = os.path.join(OUTPUT_DIR, f\"track_{track_id}\")\n",
    "        os.makedirs(track_dir, exist_ok=True)\n",
    "\n",
    "        # kişinin kırpılmış görüntüsünü kaydet\n",
    "        crop = frame[y1:y2, x1:x2]\n",
    "        if crop.size != 0:\n",
    "            out_path = os.path.join(track_dir, f\"frame_{frame_idx}.jpg\")\n",
    "            cv2.imwrite(out_path, crop)\n",
    "\n",
    "    print(f\"Frame {frame_idx} işlendi.\")\n",
    "\n",
    "cap.release()\n",
    "print(f\"✅ Tracklet kırpmaları tamamlandı. Kayıt klasörü: {OUTPUT_DIR}\")\n",
    "\"\"\"\n",
    "\n",
    "with open(\"video_to_tracklets.py\", \"w\", encoding=\"utf-8\") as f:\n",
    "    f.write(script_code)\n",
    "\n",
    "print(\"✅ 'video_to_tracklets.py' dosyası oluşturuldu.\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "9af97dc8-518e-4ed7-ab06-d3df5a819ef5",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.21"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
