from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
import json


def extract_match_details(file_name):
    # 1. Sezon ve hafta bilgisini ayır
    season_week_part = file_name.split("_", 2)[:2]  # İlk iki kısmı al
    season = season_week_part[0]  # Sezon bilgisi
    week = season_week_part[1]  # Hafta bilgisi

    # 2. Takım bilgileri ve skor
    main_part = file_name.split("_", 2)[2]  # 3. kısmı al (takımlar ve skor)
    main_part = main_part.rsplit("-mac-ozeti", 1)[0]  # "-mac-ozeti" kısmını kaldır

    # 3. Takımları ve skoru ayır
    parts = main_part.split("-")
    for i, part in enumerate(parts):
        if part.isdigit():  # Skorun başlangıcını bul
            team1 = "-".join(parts[:i])  # Skor öncesi takım 1
            team2 = "-".join(parts[i + 2 :])  # Skor sonrası takım 2
            return season, week, team1, team2

    # Eğer skor bulunamazsa hata ver
    raise ValueError("Dosya adi formatinda skor bilgisi bulunamadi.")


# ChromeDrive service
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

chrome_options = Options()
extension_path = os.path.join(
    os.path.dirname(__file__),
    "extensions",
    "BGNKHHNNAMICMPEENAELNJFHIKGBKLLG_5_0_170_0.crx",
)
chrome_options.add_extension(extension_path)


# WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# AdBlocker eklentisi
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
)
print("Eklenti yuklendi!")

# Videolarin indirilecegi linklerin bulundugu json dosyasi
input_file = "download_videos\match_highlights.json"
with open(input_file, "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

# JSON dosyasının adı
output_file = r"download_videos\video_data_with_details.json"

# Mevcut dosyayı kontrol et ve içeriği yükle
if os.path.exists(output_file):
    # Eğer dosya varsa, içeriği yükle
    with open(output_file, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)
else:
    # Eğer dosya yoksa, boş bir liste başlat
    json_data = []


# season = input("Videolarini indirmek istediginiz sezon?: ")
# lowerWeekLimit = int(input("Hangi haftadan baslansin?"))
# upperWeekLimit = int(input("Hangi haftada bitsin?"))

selectedURLs = [
    item["url"]
    for item in data["match_highlights"]
    # if item["season"].startswith(season) and lowerWeekLimit <= int(item["week"]) <= upperWeekLimit
    if item["season"]
    in ["2015-2016", "2014-2015", "2013-2014", "2012-2013", "2011-2012"]
    # and 13 <= int(item["week"]) <= 34
]

for url in selectedURLs:

    driver.get(url)
    time.sleep(5)  # Sayfanin yuklenmesi icin bekle

    # iFrame gizle
    driver.execute_script(
        """
    var iframe = document.querySelector('iframe[src*="netmera_worker.html"]');
    if(iframe){
        iframe.style.display = 'none';
    }
    """
    )

    # Bekleme
    wait = WebDriverWait(driver, 5)
    try:
        # Sinifa sahip tum 'a' elementlerini bul
        elements = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    ".text-decoration-none.rounded-circle.bg-secondary.goals_play-icon-wrapper__DH44c",
                )
            )
        )
    except TimeoutException:
        continue

    # Linklerin href degerlerini al
    href_links = [element.get_attribute("href") for element in elements]

    save_directory = r"download_videos\downloaded_videos"
    os.makedirs(save_directory, exist_ok=True)

    for link in href_links:
        if link:
            # print(f"Link aciliyor: {link}")
            driver.get(link)

            video_title = link.split("/ozet/")[1].replace("/", "_")
            season, week, team1, team2 = extract_match_details(video_title)

            print(f"{season} - {week} - {team1} - {team2}")

            time.sleep(5)

            # Videoya erisim
            try:
                # 'video' etiketini bul ve source altindaki src'ye eris
                video_element = driver.find_element(
                    By.ID, "bitmovinplayer-video-bs-player-wrapper"
                )

                # 'source' etiketini bul ve src degerini al
                source_element = video_element.find_element(By.TAG_NAME, "source")
                video_src = source_element.get_attribute("src")
                # print(f"Video SRC: {video_src}")

                # JSON için kaydet
                new_entry = {
                    "season": season,
                    "week": week,
                    "team1": team1,
                    "team2": team2,
                    "link": link,
                    "src": video_src,
                }

                json_data.append(new_entry)

                # JSON dosyasını her adımda güncelle
                with open(output_file, "w", encoding="utf-8") as json_file:
                    json.dump(json_data, json_file, ensure_ascii=False, indent=4)
                print(f"Yeni veri eklendi: {new_entry}")

            except Exception as e:
                print(f"Video veya src bulunamadi: {e}")
