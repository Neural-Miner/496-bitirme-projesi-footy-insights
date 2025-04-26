from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

TEAM_DRIVE_TAGS = {
    "Adana Demirspor": ["adana-demirspor"],
    "Adanaspor": ["adanaspor"],
    "Akhisarspor": ["akhisarspor", "akhisar-genclikspor"],
    "Alanyaspor": ["alanyaspor", "corendon-alanyaspor"],
    "Altay": ["altay"],
    "Antalyaspor": ["antalyaspor", "fraport-tav-antalyaspor"],
    "Konyaspor": ["konyaspor", "ittifak-holding-konyaspor"],
    "Hatayspor": ["hatayspor", "atakas-hatayspor"],
    "Beşiktaş": ["besiktas"],
    "Bursaspor": ["bursaspor"],
    "Trabzonspor": ["trabzonspor"],
    "Galatasaray": ["galatasaray"],
    "Fenerbahçe": ["fenerbahce"],
    "Başakşehir": ["istanbul-basaksehir"],
    "İstanbul Büyükşehir Belediyespor": ["istanbul-basaksehir"],
    "Mersin İdmanyurdu": ["mersin-idman-yurdu"],
    "Ankaragücü": ["mke-ankaragucu"],
    "Orduspor": ["orduspor"],
    "Ankaraspor": ["ankaraspor"],
    "Samsunspor": ["samsunspor"],
    "Pendikspor": ["pendikspor"],
    "Kayserispor": ["kayserispor", "yukatel-kayserispor"],
    "Erzurumspor": ["erzurumspor", "bsb-erzurumspor"],
    "Elazığspor": ["elazigspor"],
    "Eskişehirspor": ["eskisehirspor"],
    "Malatyaspor": ["malatyaspor", "oznur-kablo-yeni-malatyaspor"],
    "Giresunspor": ["giresunspor", "gzt-giresunspor"],
    "Gaziantepspor": ["gaziantepspor"],
    "Gaziantep FK": ["gaziantep-fk"],
    "Gençlerbirliği": ["genclerbirligi"],
    "Sivasspor": ["sivasspor"],
    "Rizespor": ["caykur-rizespor"],
    "İstanbulspor": ["istanbulspor"],
    "Karabükspor": ["kardemir-karabukspor"],
    "Kayseri Erciyesspor": ["kayseri-erciyesspor"],
    "Kasımpaşa": ["kasimpasa"],
    "Manisaspor": ["manisaspor"],
    "Balıkesirspor": ["balikesirspor"],
    "Fatih Karagümrük": ["fatih-karagumruk"],
    "Göztepe": ["goztepe"],
    "Ümraniyespor": ["umraniyespor"],
    "Denizlispor": ["denizlispor"]
}

def get_drive_tag(team_name):
    if team_name in TEAM_DRIVE_TAGS:
        return TEAM_DRIVE_TAGS[team_name][0]
    else:
        return None

"""
filename = get_drive_filename("2023-2024", 1, "Fatih Karagümrük", "Beşiktaş")
            --> "2023-2024_1_fatih-karagumruk_besiktas.mp4"
"""
def get_drive_filename(season, week, home_team, away_team):
    home_tag = get_drive_tag(home_team)
    away_tag = get_drive_tag(away_team)
    if not home_tag or not away_tag:
        raise ValueError(f"Takim etiketlerinden biri bulunamadi! {home_team}, {away_team}")

    return f"{season}_{week}_{home_tag}_{away_tag}.mp4"

def generatePossibleDriveNames(season, week, homeTeam, awayTeam):

    homeTags = TEAM_DRIVE_TAGS.get(homeTeam, [])
    awayTags = TEAM_DRIVE_TAGS.get(awayTeam, [])

    possibleNames = []

    # home_away siralamasi
    for hTag in homeTags:
        for aTag in awayTags:
            filename = f"{season}_{week}_{hTag}_{aTag}.mp4"
            possibleNames.append(filename)

    # away_home siralamasi
    for hTag in homeTags:
        for aTag in awayTags:
            filename = f"{season}_{week}_{aTag}_{hTag}.mp4"
            possibleNames.append(filename)

    return possibleNames

"""
# Ornek kullanim
if __name__ == "__main__":
    season = "2023-2024"
    week = 1
    homeTeam = "Antalyaspor"   # Iki etiket var: antalyaspor, fraport-tav-antalyaspor
    awayTeam = "Beşiktaş"     # Tek etiket: besiktas

    names = generatePossibleDriveNames(season, week, homeTeam, awayTeam)
    for n in names:
        print(n)
"""

# https://drive.google.com/drive/u/2/folders/1274uOwn4Es5-bGlJvc4e1awzAfsuDvyO
def tryDownloadAll(drive, possibleNames, folder_id=None):
    """
    'drive' -> PyDrive ile oluşturulmuş GoogleDrive nesnesi
    'possibleNames' -> generatePossibleDriveNames fonksiyonundan gelen list
    """
    for name in possibleNames:
        print(f"Trying: {name}")

        if folder_id:
            query = f"'{folder_id}' in parents and title = '{name}' and trashed=false"
        else:
            query = f"title = '{name}' and trashed=false"

        file_list = drive.ListFile({'q': query}).GetList()

        if file_list:
            # Bulduysak indir
            file = file_list[0]
            print(f"Found! Downloading {file['title']}")
            file.GetContentFile(file['title'])
            return  # Tek bir dosya indirdikten sonra çıkabiliriz

    print("No matching file found in Drive.")

gauth = GoogleAuth()
# gauth.LocalWebserverAuth()
# drive = GoogleDrive(gauth)

# Daha once kaydedilmis kimlik bilgileri var mi?
gauth.LoadCredentialsFile("mycreds.json")  # Adi ne isterseniz

if not gauth.credentials or gauth.access_token_expired:
    # Yoksa veya suresi bittiyse, tarayici acarak sifirdan kimlik dogrula
    gauth.LocalWebserverAuth()
    # Basarili olunca mycreds.json dosyasina kaydet
    gauth.SaveCredentialsFile("mycreds.json")

drive = GoogleDrive(gauth)

list = generatePossibleDriveNames("2022-2023", "27", "Ümraniyespor", "Konyaspor")
tryDownloadAll(drive=drive, possibleNames=list)