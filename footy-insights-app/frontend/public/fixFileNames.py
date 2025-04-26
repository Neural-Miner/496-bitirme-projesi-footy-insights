import os
import re

# Türkçe karakterleri İngilizceye çevirmek için dönüşüm tablosu
char_map = str.maketrans(
    "çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU"
)

# Ana dizin (Dosya yapısına göre güncelle)
base_path = "mac_verileri"

# 2011-2012'den 2023-2024'e kadar olan klasörleri işle
for year in range(2011, 2024):  # 2011 → 2023 (sonraki yıl dahil olduğu için 2024 yazıldı)
    season_folder = f"{year}-{year+1}"
    full_path = os.path.join(base_path, season_folder)

    # Eğer klasör mevcutsa işlem yap
    if os.path.exists(full_path):
        print(f"\n📂 İşleniyor: {season_folder}")

        for file_name in os.listdir(full_path):
            if file_name.endswith(".json"):
                # Dosya adını ve uzantıyı ayır
                name, ext = os.path.splitext(file_name)
                
                # Türkçe karakterleri değiştir, küçük harfe çevir
                name = name.translate(char_map).lower()
                
                name = re.sub(r'\s+', '-', name)  # Sadece boşlukları değiştir, alt çizgilere dokunma
                name = re.sub(r"[^a-z0-9-_]", "", name)  # Geçersiz karakterleri kaldır, noktayı koru
                
                # Yeni dosya adını oluştur
                new_name = f"{name}{ext}"

                # Eski ve yeni dosya yolları
                old_path = os.path.join(full_path, file_name)
                new_path = os.path.join(full_path, new_name)

                # Dosya ismi değişmişse yeniden adlandır
                if old_path != new_path:
                    os.rename(old_path, new_path)
                    print(f"✅ '{file_name}' → '{new_name}' olarak değiştirildi.")
