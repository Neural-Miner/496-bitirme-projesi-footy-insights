from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def main():
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile('client_secrets.json')
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    folderId = '1m4pWcxNQdUNyhZH6NA3b9Tjd_vp2ghCm'

    # 'title': Drive'da görünecek dosya adi
    # Varsayılan olarak "root" klasörüne yüklenir
    newFile = drive.CreateFile({
    'title': 'deneme.txt',
    'parents': [{'id': folderId}]
    })

    newFile.SetContentString("Deneme dosyasi")

    # Dosyayi Drive'a yukle
    newFile.Upload()

    print("Dosya yuklendi!")
    print("Dosya ID:", newFile['id'])
    print("Dosya Baglantisi:", newFile['alternateLink'])

if __name__ == '__main__':
    main()