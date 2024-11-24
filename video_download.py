from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import time
import requests
from bs4 import BeautifulSoup
import os

# ChromeDriver servisini oluştur
service = Service('C:/Users/kaan/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe')

# WebDriver'ı başlat
driver = webdriver.Chrome(service=service)

# Ana sayfaya git
url = 'https://beinsports.com.tr/mac-ozetleri-goller/super-lig'
driver.get(url)
time.sleep(5)  # Sayfanın yüklenmesi için bekle


# İframe'i gizle (eğer varsa)
driver.execute_script("""
var iframe = document.querySelector('iframe[src*="netmera_worker.html"]');
if(iframe){
    iframe.style.display = 'none';
}
""")

# Bekleme tanımla
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

video = driver.find_element(By.CSS_SELECTOR, 'span.text-decoration-none.rounded-circle.bg-secondary.goals_play-icon-wrapper__DH44c')
video.click()


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
