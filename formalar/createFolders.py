import os
import json

def CreateTeamSeasonFolders(JsonFilePath, TargetPath):
    # JSON dosyasini oku
    with open(JsonFilePath, "r", encoding="utf-8") as File:
        Data = json.load(File)
    
    # Tum takim isimlerini toplamak icin bir set olustur
    Teams = set()
    
    # JSON yapisi; her sezon icin turler (round) var, her turda maclar listesi
    for Season in Data:
        SeasonData = Data[Season]
        for Round in SeasonData:
            for Match in SeasonData[Round]:
                Teams.add(Match["homeTeam"])
                Teams.add(Match["awayTeam"])
    
    # Her takim icin klasor olustur ve icine sezon klasorlerini ekle
    for Team in Teams:
        TeamFolder = os.path.join(TargetPath, Team)
        os.makedirs(TeamFolder, exist_ok=True)
        
        # 2011-2012'den 2023-2024'e kadar sezon klasorleri
        for StartYear in range(2011, 2024):  # range(2011,2024) -> 2011 ... 2023
            SeasonFolderName = f"{StartYear}-{StartYear+1}"
            SeasonFolder = os.path.join(TeamFolder, SeasonFolderName)
            os.makedirs(SeasonFolder, exist_ok=True)
            print(f"Created folder: {SeasonFolder}")

if __name__ == "__main__":
    JsonFilePath = "/home/kaan/Desktop/496-bitirme-projesi-footy-insights/detectMatchDetails/mac_verileri/matches.json"
    TargetPath = "/home/kaan/Desktop/496-bitirme-projesi-footy-insights/formalar"
    CreateTeamSeasonFolders(JsonFilePath, TargetPath)