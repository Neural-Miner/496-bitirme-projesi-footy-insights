#!sudo apt-get install tesseract-ocr -y
#!pip install pytesseract

import cv2
import pytesseract
import json
import os
import re
from typing import List, Tuple

import pandas as pd

videoPath = "/content/drive/MyDrive/cropped_2023-2024_11_fraport-tav-antalyaspor_besiktas.mp4"
resultsJsonPath = "/content/drive/MyDrive/colab_notebooks/goal_detection/2023-2024_11_fraport-tav-antalyaspor_besiktas/events_only_goals.json"
matchJsonPath = "/content/drive/MyDrive/colab_notebooks/goal_detection/2023-2024_11_fraport-tav-antalyaspor_besiktas/2023-2024_11_BITEXEN ANTALYASPOR_BEŞİKTAŞ A.Ş..json"
outputDir = "/content/drive/MyDrive/colab_notebooks/goal_detection/2023-2024_11_fraport-tav-antalyaspor_besiktas"
os.makedirs(outputDir, exist_ok=True)
outputFramesDir = os.path.join(outputDir, "goal_frames")
os.makedirs(outputFramesDir, exist_ok=True)

# videoPath = "/content/drive/MyDrive/videos_bein_sports/downloads/2023-2024/2023-2024_4_besiktas_sivasspor.mp4"
# resultsJsonPath = "/content/drive/MyDrive/colab_notebooks/goal_detection/2023-2024_4_besiktas_sivasspor/2023-2024_4_besiktas_sivasspor/results_spotting.json"
# matchJsonPath = "/content/drive/MyDrive/colab_notebooks/goal_detection/2023-2024_4_besiktas_sivasspor/2023-2024_4_BEŞİKTAŞ A.Ş._EMS YAPI SİVASSPOR.json"
# outputDir = "/content/drive/MyDrive/colab_notebooks/goal_detection/2023-2024_4_besiktas_sivasspor/goal_frames"

with open(resultsJsonPath, "r", encoding="utf-8") as f:
    resultsData = json.load(f)

with open(matchJsonPath, "r", encoding="utf-8") as f:
    matchData = json.load(f)

# Gercek gollerin bilgisi
realGoalDetails = []
half = "?"
for team in matchData["takimlar"].values():
    for gol in team.get("goller", []):
        dakika_raw = gol["dakika"]
        if "+" in dakika_raw:
            ana, uzatma = re.findall(r"(\d+)\+(\d+)", dakika_raw)[0]
            realMinute = int(ana) + int(uzatma)
            if int(ana) <= 45:
                half = 1
            else:
                half = 2
        else:
            realMinute = int(re.findall(r"\d+", dakika_raw)[0])
            if realMinute < 45:
                half = 1
            else:
                half = 2

        print(f"realMinute: {realMinute}, half: {half}")

        realGoalDetails.append({
            "minute": realMinute,
            "half": half,
            "takim": team["takimAdi"][0],
            "oyuncu": gol["oyuncu"],
            "checked": False
        })

print("Gercek mac golleri (JSON'dan):")
for items in realGoalDetails:
    print(items)
print("-" * 50)


# 3. OCR ile skor suresi oku
def extractTimeFromFrame(frame, frameId):

    # cropped = frame[26:52, 60:126]

    # Oran bazli kirpma
    h, w = frame.shape[:2]

    # yaklasik oranlar
    y1 = int(0.05 * h)   # 26/540 ≈ 0.048
    y2 = int(0.10 * h)   # 52/540 ≈ 0.096
    x1 = int(0.06 * w)   # 60/960 ≈ 0.0625
    x2 = int(0.14 * w)   # 126/960 ≈ 0.131

    # Kirpma islemi
    cropped = frame[y1:y2, x1:x2]

    croppedPath = os.path.join(outputFramesDir, f"frame_{frameId}_cropped.png")
    cv2.imwrite(croppedPath, cropped)

    text = pytesseract.image_to_string(cropped, config='--psm 7')
    text = text.strip().replace("|", "").replace("]", "").replace("[", "").replace("(", "").replace(")", "")
    print(f"OCR metni (frame {frameId}):", text)

    match = re.search(r'(\d+)(?:\+(\d+))?[:.](\d{2})', text)
    if match:
        minute = int(match.group(1))
        extra  = int(match.group(2)) if match.group(2) else 0
        second = int(match.group(3))
        return minute + extra, second
    return None, None

# 4. Goal etiketlerini işle
cap = cv2.VideoCapture(videoPath)
fps = cap.get(cv2.CAP_PROP_FPS)

verifiedGoals = []
# verifiedMinutes = []
seen_summary_secs = []
duplicate_threshold = 5

for prediction in resultsData:
    # if prediction["label"].lower() != "goal":
    #     continue

    # gameTime'dan dakika ve saniye al

    # gameTimeRaw = prediction.get("gameTime", "")
    # match = re.search(r"(\d{1,2}):(\d{2})", gameTimeRaw)
    # if not match:
    #     print(f"Geçersiz gameTime formatı: {gameTimeRaw}")
    #     continue

    try:
        minute_str, second_str = prediction["gameTime"].split(":")
        minute, second = int(minute_str), int(second_str)
    except Exception:
        print(f"Gecersiz gameTime formati: {prediction.get('gameTime')}")
        continue

    # minute = int(match.group(1))
    # second = int(match.group(2))
    totalSeconds = minute * 60 + second

    if any(abs(totalSeconds - prev) <= duplicate_threshold for prev in seen_summary_secs):
    # print(f"→ Atlanan tekrar: {prediction['gameTime']}")
      continue

    seen_summary_secs.append(totalSeconds)

    # Frame index hesapla
    frameIndex = int(totalSeconds * fps)

    cap.set(cv2.CAP_PROP_POS_FRAMES, frameIndex)
    ret, frame = cap.read()

    gameTimeRaw = prediction.get("gameTime", "")
    if not ret:
        print(f"Frame okunamadi - GameTime: {gameTimeRaw}, frameIndex: {frameIndex}")
        continue

    # Goruntuyu kaydet
    filename = f"frame_{frameIndex}_{minute:02d}m{second:02d}s.png"
    imgPath   = os.path.join(outputFramesDir, filename)
    success   = cv2.imwrite(imgPath, frame)

    # imgPath = os.path.join(outputFramesDir, f"frame_{frameIndex}.png")
    # success = cv2.imwrite(imgPath, frame)
    if not success:
        print(f"Görüntü kaydedilemedi: {imgPath}")
        continue

    # OCR ile sure oku
    ocr_minute, ocr_second = extractTimeFromFrame(frame, frameIndex)
    if ocr_minute is None:
        continue

    candidates = [
      g for g in realGoalDetails
      if not g["checked"] and abs(ocr_minute - g["minute"]) <= 1
    ]
    if not candidates:
      print(f"Eşleşecek gol yok (ocr={ocr_minute})")
      continue

    pick = next((g for g in candidates if g["half"] == 1), candidates[0])


    verifiedGoals.append({
        "frame":      frameIndex,
        "half":       pick["half"],
        "ocr_minute": ocr_minute,
        "ocr_second": ocr_second,
        "takim":      pick["takim"],
        "oyuncu":     pick["oyuncu"],
        "ozet_dakika": minute,
        "ozet_saniye": second,
        "image_path": imgPath
    })
    pick["checked"] = True

cap.release()

print("Modelin 'goal' olarak etiketlediği anlar (gameTime):")
for prediction in resultsData:
    if prediction["label"].lower() == "goal":
        print(f"gameTime: {prediction.get('gameTime', 'N/A')}")
print("-" * 50)


# Dogrulanan goller CSV benzeri cikti olarak

if verifiedGoals:
    print("Doğrulanan goller:")
    for goal in verifiedGoals:
        print(f"Frame: {goal['frame']}, Zaman (OCR): {goal['ocr_minute']}:{str(goal['ocr_second']).zfill(2)}, Takım: {goal['takim']}, Oyuncu: {goal['oyuncu']}, Ozet dakika: {goal['ozet_dakika']}, Ozet saniye: {goal['ozet_saniye']}, Half: {goal['half']}")
else:
    print("Dogrulanan gol bulunamadi.")


# CSV olusturma

# 1) Takim + oyuncu bazli forma no haritasi olustur
jersey_map = {}
for team in matchData["takimlar"].values():
    team_name = team["takimAdi"][0]
    jersey_map[team_name] = {}
    # ilk11 ve yedekler içinde ara
    for p in team.get("ilk11", []) + team.get("yedekler", []):
        jersey_map[team_name][p["oyuncuAdi"]] = p["formaNo"]

# 2) (takim, oyuncu, yari) uclusundan gercek dakikayi donen map
real_goal_map = {
    (g["takim"], g["oyuncu"], g["half"]): g["minute"]
    for g in realGoalDetails
}

import csv
# 3) CSV dosyasini yaz
csv_path = os.path.join(outputDir, "verified_goals.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "real_minute",
        "ozet_dakika",
        "ozet_saniye",
        "oyuncu",
        "takim",
        "formaNo"
    ])

    for vg in verifiedGoals:
        key = (vg["takim"], vg["oyuncu"], vg["half"])
        real_min = real_goal_map.get(key, "")
        form_no = jersey_map.get(vg["takim"], {}).get(vg["oyuncu"], "")
        writer.writerow([
            real_min,
            vg["ozet_dakika"],
            vg["ozet_saniye"],
            vg["oyuncu"],
            vg["takim"],
            form_no
        ])

print(f"CSV kaydedildi: {csv_path}")