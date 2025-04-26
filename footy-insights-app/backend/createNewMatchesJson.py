import json
import os

# JSON dosyasını oku
with open('matches.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# JSON dosyalarının bulunduğu ana klasör
base_path = "/mac_verileri"

# Her sezon ve hafta için detaylı dosya yolunu ekle
for season, weeks in data.items():
    for week, matches in weeks.items():
        for match in matches:
            # Dosya ismi oluşturma
            file_name = f"{season}_{week}_{match['homeTeam'].upper()}_{match['awayTeam'].upper()}.json"

            # Dosya yolu ekleme
            match["detailsPath"] = os.path.join(base_path, season, file_name)

# Sonuçları yeni bir dosyaya yaz
with open('matches_with_paths.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("Detaylı maç dosyalarının yolları başarıyla eklendi!")
