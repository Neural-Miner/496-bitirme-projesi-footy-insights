import os
import json

def fixKeys(obj):
    # JSON objesini (dict veya list) rekürsif olarak dolaşarak "oyuncuAdi:" anahtarlarını "oyuncuAdi" olarak değiştirir.
    if isinstance(obj, dict):
        newDict = {}
        for key, value in obj.items():
            newKey = key
            if key == "oyuncuAdi:":
                newKey = "oyuncuAdi"
            newDict[newKey] = fixKeys(value)
        return newDict
    elif isinstance(obj, list):
        return [fixKeys(item) for item in obj]
    else:
        return obj

def fixOyuncuAdiStrings(rootPath):
    # rootPath içindeki tüm klasör ve alt klasörlerdeki .json dosyalarını bulur, içeriklerini günceller.
    for root, dirs, files in os.walk(rootPath):
        for file in files:
            if file.endswith(".json"):
                filePath = os.path.join(root, file)
                # JSON dosyasını oku
                with open(filePath, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Anahtar değişikliğini uygula
                data = fixKeys(data)

                # Dosyayı güncellenmiş içerikle tekrar yaz
                with open(filePath, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    targetDir = "/home/kaan/Desktop/496-bitirme-projesi-footy-insights/detectMatchDetails/mac_verileri"
    fixOyuncuAdiStrings(targetDir)