import os
import gc
import subprocess

from flask import Flask, request, jsonify, send_from_directory
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   # tum routelar icin herkese acik izin sagliyor


# ROOT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(ROOT, "downloads")

CLIENT_SECRETS = os.path.join(ROOT, "client_secrets.json")
CREDENTIALS_FILE = os.path.join(ROOT, "mycreds.json")
ANALYSIS_DIR = os.path.join(ROOT, "analysis")   # action modeli icin

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)

# Google drive kimlik dogrulamasi
gauth = GoogleAuth()

gauth.LoadClientConfigFile(CLIENT_SECRETS)
gauth.LoadCredentialsFile(CREDENTIALS_FILE)

if not gauth.credentials or gauth.access_token_expired:
    # tarayici acilip dogrulama yapilir
    gauth.LocalWebserverAuth()
    gauth.SaveCredentialsFile( os.path.join("mycreds.json") )

drive = GoogleDrive(gauth)

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

    for i in possibleNames:
        print(f"Possible {i}")

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

            downloadPath = os.path.join(DOWNLOAD_DIR, file['title'])
            file.GetContentFile(downloadPath)
            print(f"Downloaded to {downloadPath}")
            return name  # indirilen dosyanin adi return

    print("No matching file found in Drive.")
    return False

@app.route("/downloads/<path:filename>")
def serve_downloads(filename):
    # DOWNLOAD_DIR: indirdiğiniz videoların bulunduğu klasörün tam yolu
    return send_from_directory(
        DOWNLOAD_DIR,   # directory
        filename,       # filename
        mimetype="video/mp4",
        conditional=True  # Range isteği desteği
    )

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

    for name in possible_names:
        localPath = os.path.join(DOWNLOAD_DIR, name)
        if os.path.isfile(localPath):
            return jsonify({
                "success": True,
                "alreadyExists": True,
                "message": "Dosya zaten mevcut",
                "videoFileName": name,
                "localPath": localPath
            })

    # 2) Yerelde yoksa Drive'dan indir
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.json")
    if not gauth.credentials or gauth.access_token_expired:
        gauth.LocalWebserverAuth()
        gauth.SaveCredentialsFile("mycreds.json")
    global drive
    drive = GoogleDrive(gauth)

    downloaded = findAndDownloadFromDrive(possible_names)
    if downloaded:
        return jsonify({
            "success": True,
            "alreadyExists": False,
            "message": "Dosya Drive'dan indirildi",
            "videoFileName": downloaded,
            "localPath": os.path.join(DOWNLOAD_DIR, downloaded)
        })
    else:
        return jsonify({"success": False, "message": "Dosya bulunamadi!"}), 404
    

@app.route("/predict-video", methods=["POST"])
def predict_video():
    """
    React'ten gelen JSON:
    { "videoFileName": "2023-2024_1_antalyaspor_besiktas.mp4" }

    Dönen cevap:
    {
      "success": true,
      "eventsOnly": "/analysis/2023-2024_1_antalyaspor_besiktas/events_only_goals.json",
      "eventsWithout": "/analysis/2023-2024_1_antalyaspor_besiktas/events_without_goals.json"
    }
    """
    data = request.get_json()
    video_filename = data.get("videoFileName")
    if not video_filename:
        return jsonify({"success": False, "message": "Eksik parametre: videoFileName"}), 400

    video_path = os.path.join(DOWNLOAD_DIR, video_filename)
    if not os.path.exists(video_path):
        return jsonify({"success": False, "message": "Video dosyası bulunamadı"}), 404

    # Oyun adını dosya adından türet
    game_name = os.path.splitext(video_filename)[0]
    output_dir = os.path.join(ANALYSIS_DIR, game_name)
    os.makedirs(output_dir, exist_ok=True)

    # predict_action.py ile analiz işlemi
    try:
        subprocess.run([
            "python3", os.path(ROOT, "predict_action.py"),
            "--video_path", video_path,
            "--output_dir", output_dir,
            "--game_name", game_name
        ], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "message": str(e)}), 500

    return jsonify({
        "success": True,
        "eventsOnly": f"/analysis/{game_name}/events_only_goals.json",
        "eventsWithout": f"/analysis/{game_name}/events_without_goals.json"
    })



if __name__ == "__main__":
    app.run(port=5000, debug=True)