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
url = 'https://beinsports.com.tr/mac-ozetleri-goller/super-lig'
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

# Sezon ve hafta seçimi (ID değerlerine göre)
season_select = driver.find_element(By.ID, 'season-select')
season_select.click()
time.sleep(2)
# Sezon listesinden istediğiniz sezonu seçin
desired_season = driver.find_element(By.XPATH, "//div[@class='rc-select-item-option-content' and text()='2023/2024']")
desired_season.click()
time.sleep(2)

round_select = driver.find_element(By.ID, 'round-select')
round_select.click()
time.sleep(1)
# Hafta listesinden istediğiniz haftayı seçin
desired_round = driver.find_element(By.XPATH, "//div[@class='rc-select-item-option-content' and text()='37 .Hafta']")
desired_round.click()

time.sleep(3)  # Seçimlerin uygulanması için bekle

# En son bu asamaya gelindi, oynat tuslarinin secimi yapilacak. Her bir oynatma tusuna tiklanmasi sonucu
# acilan videolarin indirilmesi saglanacaktir.

counter = 1

# Sınıfa sahip tüm 'a' elementlerini bul
elements = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 
            ".text-decoration-none.rounded-circle.bg-secondary.goals_play-icon-wrapper__DH44c"))
    )

# Linklerin href değerlerini al
href_links = [element.get_attribute("href") for element in elements]

# Her bir linki yeni bir sekmede ac
for link in href_links:
    if link:  # Href boş değilse
        print(f"Link aciliyor: {link}")
        driver.execute_script(f"window.open('{link}', '_blank');")

        time.sleep(5)

        # Videoya erisim
        try:
            # 'video' etiketini bul ve source altındaki src'ye eriş
            """
            video_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "bitmovinplayer-video-bs-player-wrapper"))
            )
            """
            video_element = driver.find_element(By.ID, "bitmovinplayer-video-bs-player-wrapper")

            # 'source' etiketini bul ve src değerini al
            source_element = video_element.find_element(By.TAG_NAME, "source")
            video_src = source_element.get_attribute("src")
            print(f"Video SRC: {video_src}")

            """
            # Yeni sekmede bu linki aç
            driver.execute_script(f"window.open('{video_src}', '_blank');")
            time.sleep(3)
            """

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
            time.sleep(2)
    

"""
# Oynat tuşlarını bul
play_buttons = driver.find_elements(By.CLASS_NAME, 'text-decoration-none rounded-circle bg-secondary goals_play-icon-wrapper__DH44c')


video_urls = []

for button in play_buttons:
    # Yeni bir sekmede açmak için Shift tuşuna basılı tutun
    webdriver.ActionChains(driver).key_down(u'\ue008').click(button).key_up(u'\ue008').perform()
    time.sleep(2)

    # En son açılan sekmeye geç
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(2)
    # Video URL'sini al
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    video_tag = soup.find('video')
    if video_tag and video_tag.has_attr('src'):
        video_url = video_tag['src']
        video_urls.append(video_url)
        # Video dosyasını indir
        video_content = requests.get(video_url).content
        video_name = video_url.split('/')[-1]
        with open(video_name, 'wb') as f:
            f.write(video_content)
        print(f"{video_name} indirildi.")
    else:
        print("Video URL'si bulunamadı.")
    # Sekmeyi kapat
    driver.close()
    # Ana sekmeye geri dön
    driver.switch_to.window(driver.window_handles[0])

    time.sleep(1)

    """

# WebDriver'ı kapat
# driver.quit()
