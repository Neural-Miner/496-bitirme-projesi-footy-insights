from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def download_from_drive(file_title):
    """
    'file_title' Drive'daki dosya adı (ör. '2023-2024_1_fatih-karagumruk_besiktas.mp4')
    """

    # 1. Kimlik doğrulama
    gauth = GoogleAuth()
    # Eğer ilk defa yapıyorsanız LocalWebserverAuth() tarayıcı açarak OAuth izinleri alacak
    gauth.LocalWebserverAuth()

    # 2. Drive nesnesini oluştur
    drive = GoogleDrive(gauth)

    # 3. Dosyayı arayalım (title alanına göre)
    # Not: Dosya adları tam olarak eşleşmeli veya ek sorgular ekleyebilirsiniz
    file_list = drive.ListFile(
        {'q': f"title = '{file_title}' and trashed=false"}
    ).GetList()

    if not file_list:
        print(f"{file_title} adlı dosya bulunamadı.")
        return

    # 4. Bulunan ilk dosyayı indir
    drive_file = file_list[0]
    print(f"İndiriliyor: {drive_file['title']} (ID: {drive_file['id']})")
    drive_file.GetContentFile(drive_file['title'])
    print("İndirme tamamlandı.")

if __name__ == "__main__":
    # Örnek kullanım
    download_from_drive("2023-2024_1_fatih-karagumruk_besiktas.mp4")
