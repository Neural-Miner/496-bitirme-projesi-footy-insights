import cv2
import pytesseract
import numpy as np

# Tesseract yolu
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Goruntu dosyalari
imagePaths = ['mac_bilgileri_tespiti/takim1.png', 'mac_bilgileri_tespiti/takim2.png']

# Goruntuden metin cikarim fonksiyonu
def extractTextFromImage(image_path):
    # Goruntuyu yukle
    img = cv2.imread(image_path)
    
    # Goruntuyu gri tonlamaya cevir
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Gurultu azaltma icin bulaniklastirma
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Kontrast artir
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # OCR ile metin cikarimi
    text = pytesseract.image_to_string(thresh, lang='eng')
    return text

# Metin cikarimi ve duzenleme
for imagePath in imagePaths:
    print(f"Analyzing: {imagePath}")
    extracted_text = extractTextFromImage(imagePath)
    print("Extracted Text:\n", extracted_text)

    #Takim ve oyuncu bilgilerini ayristirma
    # import re
    # team_name = re.search(r'(T\.\s?[A-Z]+|V\.\s?[A-Z]+)', extracted_text)
    # if team_name:
    #     print("Team Name:", team_name.group(0))
    
    # players = re.findall(r'(\d+)\s+([A-Za-zğüşıöçĞÜŞİÖÇ]+)', extracted_text)
    # print("Players:", players)