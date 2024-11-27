from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from bs4 import BeautifulSoup
import os

# ChromeDriver servisini oluştur
service = Service('C:/Users/kaan/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe')

chrome_options = Options()
chrome_options.add_extension('C:/Users/kaan/Downloads/BGNKHHNNAMICMPEENAELNJFHIKGBKLLG_5_0_170_0.crx')
# WebDriver'ı başlat
driver = webdriver.Chrome(service=service, options=chrome_options)

# time.sleep(20)  # Sayfanın yüklenmesi için bekle

# Eklentinin yüklenmesini bekle
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "body"))  # Basit bir bekleme, tarayıcı hazır olduğunda
)
print("Eklenti basariyla yüklendi!")

# Ana sayfaya git
# url = 'https://beinsports.com.tr/mac-ozetleri-goller/super-lig/ozet/2023-2024/38/fenerbahce-6-0-istanbulspor-mac-ozeti'
url = 'https://beinsports.com.tr/mac-ozetleri-goller/super-lig/ozet/2023-2024/38'
driver.get(url)
time.sleep(5)  # Sayfanın yüklenmesi için bekle


# iFrame gizle
driver.execute_script("""
var iframe = document.querySelector('iframe[src*="netmera_worker.html"]');
if(iframe){
    iframe.style.display = 'none';
}
""")

# Bekleme tanimla
wait = WebDriverWait(driver, 10)

counter = 1

# Sınıfa sahip tüm 'a' elementlerini bul
elements = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 
            ".text-decoration-none.rounded-circle.bg-secondary.goals_play-icon-wrapper__DH44c"))
    )

# Linklerin href değerlerini al
href_links = [element.get_attribute("href") for element in elements]


for link in href_links:
    if link:  # Href boş değilse
        print(f"Link aciliyor: {link}")
        driver.get(link)

        time.sleep(5)

        # Videoya erisim
        try:
            # 'video' etiketini bul ve source altındaki src'ye eriş
            video_element = driver.find_element(By.ID, "bitmovinplayer-video-bs-player-wrapper")

            # 'source' etiketini bul ve src değerini al
            source_element = video_element.find_element(By.TAG_NAME, "source")
            video_src = source_element.get_attribute("src")
            print(f"Video SRC: {video_src}")

            # Videoyu kaydet..
            # Video URL'sini bilgisayara kaydet
            response = requests.get(video_src, stream=True) # Video dosyasini indirme
            if response.status_code == 200:
                with open(f"video{counter}.mp4", "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)
                print("Video başarıyla kaydedildi: video.mp4")
                counter += 1
            else:
                print(f"Video indirilemedi. HTTP Hatası: {response.status_code}")
        except Exception as e:
            print(f"Video veya src bulunamadı: {e}")