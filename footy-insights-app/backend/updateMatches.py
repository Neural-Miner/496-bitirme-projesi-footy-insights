import json
import os
import re

# Türkçe karakterleri İngilizce'ye çevirmek için bir fonksiyon
def convert_to_ascii(text):
    char_map = str.maketrans("ıöüçşğİÖÜÇŞĞ", "ioucsgIOUCSG")
    return text.translate(char_map)

# Dosya adlarını uygun formata dönüştüren fonksiyon
def format_filename(filename):
    filename = convert_to_ascii(filename)  # Türkçe karakterleri dönüştür
    filename = filename.lower().replace(" ", "-")  # Küçük harfe çevir ve boşlukları kısa çizgi yap
    filename = re.sub(r"[^a-z0-9-]", "", filename)  # Geçersiz karakterleri kaldır
    return filename

# JSON dosyasını oku
with open('matches_with_paths.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# JSON dosyalarının bulunduğu ana klasör
base_path = "/mac_verileri"

# Her sezon ve hafta için detaylı dosya yolunu güncelle
for season, weeks in data.items():
    for week, matches in weeks.items():
        for match in matches:
            # Orijinal dosya ismi oluşturma
            home_team = format_filename(match['homeTeam'])
            away_team = format_filename(match['awayTeam'])
            file_name = f"{season}_{week}_{home_team}_{away_team}.json"
            
            # Dosya yolunu güncelle
            match["detailsPath"] = os.path.join(base_path, season, file_name)

# Güncellenmiş dosyayı kaydet
with open('matches_with_paths_updated.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("Detaylı maç dosyalarının yolları başarıyla güncellendi!")
