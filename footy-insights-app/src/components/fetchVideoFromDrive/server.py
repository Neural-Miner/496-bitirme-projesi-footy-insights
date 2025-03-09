import os
from flask import Flask, request, jsonify, send_from_directory
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   # tum routelar icin herkese acik izin sagliyor

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

# Google drive kimlik dogrulamasi
gauth = GoogleAuth()

gauth.LoadCredentialsFile("mycreds.json")

if not gauth.credentials or gauth.access_token_expired:
    # Kimlik dogrulamasi yoksa, tarayici acilip dogrulama yapilir
    gauth.LocalWebserverAuth()

    gauth.SaveCredentialsFile("mycreds.json")

drive = GoogleDrive(gauth)

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

def findAndDownloadFromDrive(possibleNames, folder_id=None):
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

            downloadPath = os.path.join("downloads", file['title'])
            file.GetContentFile(downloadPath)
            print(f"Downloaded to {downloadPath}")
            return name  # indirilen dosyanin adi return

    print("No matching file found in Drive.")
    return False

@app.route("/downloads/<path:filename>")
def serve_downloads(filename):
    return send_from_directory("downloads", filename)

# React'ten gelecek post istegi yakalanir
@app.route("/download-video", methods=["POST"])
def downloadVideo():
    """
    React'tan gelen JSON:
    {
      "season": "2023-2024",
      "week": "1",
      "homeTeam": "Antalyaspor",
      "awayTeam": "Beşiktaş"
    }
    Dönen cevap:
    {
      "success": true/false,
      "message": "...",
      "localPath": "..."
    }
    """

    data = request.get_json()
    
    season = data.get("season")
    week = data.get("week")
    homeTeam = data.get("homeTeam")
    awayTeam = data.get("awayTeam")

    # Eksik veri
    if not all([season, week, homeTeam, awayTeam]):
        return jsonify({"success": False, "message": "Eksik parametre"}), 400
    
    possible_names = generatePossibleDriveNames(season, week, homeTeam, awayTeam)
    result = findAndDownloadFromDrive(possible_names)

    if result:
        return jsonify({"success": True, "message": "Dosya bulundu, indirildi!", "videoFileName": result})
    else:
        return jsonify({"success": False, "message": "Dosya bulunamadi!"})
    

if __name__ == "__main__":
    os.makedirs("downloads", exist_ok=True)
    app.run(port=5000, debug=True)