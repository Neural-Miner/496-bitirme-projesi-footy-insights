from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os
import json
import random

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
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
)
print("Eklenti yuklendi!")


# Videolarin indirilecegi linklerin bulundugu json dosyasi
input_file = "download_videos\match_highlights.json"
with open(input_file, "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

selectedURLs = []

downloadType = int(
    input(
        "Belirli bir sezona ait videolari indir. (1) \nSezon fark etmeden karisik indir. (2)"
    )
)

if downloadType == 1:
    season = input("Videolarini indirmek istediginiz sezon?: ")
    lowerWeekLimit = int(input("Hangi haftadan baslansin?"))
    upperWeekLimit = int(input("Hangi haftada bitsin?"))

    selectedURLs = [
        item["url"]
        for item in data["match_highlights"]
        if item["season"].startswith(season)
        and lowerWeekLimit <= int(item["week"]) <= upperWeekLimit
    ]
elif downloadType == 2:
    numberOfVideos = int(input("Indirmek istediginiz video sayisini giriniz: "))

    if numberOfVideos > len(data["match_highlights"]):
        print(
            f'Sadece {len(data["match_highlights"])} adet URL mevcut. Daha az bir sayi girin.'
        )
    else:
        allURLs = [item["url"] for item in data["match_highlights"]]
        selectedURLs = random.sample(allURLs, numberOfVideos)
        for i in selectedURLs:
            print(i)


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

    # Sinifa sahip tum 'a' elementlerini bul
    elements = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located(
            (
                By.CSS_SELECTOR,
                ".text-decoration-none.rounded-circle.bg-secondary.goals_play-icon-wrapper__DH44c",
            )
        )
    )

    # Linklerin href degerlerini al
    href_links = [element.get_attribute("href") for element in elements]

    save_directory = r"download_videos\downloaded_videos"
    os.makedirs(save_directory, exist_ok=True)

    for link in href_links:
        if link:
            print(f"Link aciliyor: {link}")
            driver.get(link)

            video_title = link.split("/ozet/")[1].replace("/", "_")
            # print("title: " + video_title)

            save_path = os.path.join(save_directory, f"{video_title}.mp4")

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
                print(f"Video SRC: {video_src}")

                # Videoyu kaydet..
                response = requests.get(
                    video_src, stream=True
                )  # Video dosyasini indirme
                if response.status_code == 200:
                    with open(save_path, "wb") as file:
                        for chunk in response.iter_content(chunk_size=1024):
                            file.write(chunk)
                    print("Video basariyla indirildi.")

                else:
                    print(f"Video indirilemedi. HTTP Hatasi: {response.status_code}")
            except Exception as e:
                print(f"Video veya src bulunamadi: {e}")
