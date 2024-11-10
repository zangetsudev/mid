import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import time

# Kullanıcıdan URL'yi alma
base_url = "https://mangatr.me/manga/tower-of-god/bolum-"
download_base_folder = "indirilen_resimler"

# İndirme klasörünü oluşturma
if not os.path.exists(download_base_folder):
    os.makedirs(download_base_folder)

# Ziyaret edilen sayfaları takip etmek için bir set oluştur
visited = set()


# Resimleri bulma ve indirme fonksiyonu
def download_images(chapter_url):
    visited.add(chapter_url)

    try:
        response = requests.get(chapter_url)
        response.raise_for_status()  # Hata durumunda bir istisna fırlat
    except requests.exceptions.RequestException as e:
        print(f"Hata oluştu: {e}")
        return False  # Hata durumunda False döndür

    soup = BeautifulSoup(response.text, "html.parser")

    # Tüm <img> etiketlerini bul ve resimleri indir
    img_tags = soup.find_all("img")
    chapter_folder = os.path.join(download_base_folder,
                                  f"bolum_{chapter_url.split('-')[-1]}")

    if not os.path.exists(chapter_folder):
        os.makedirs(chapter_folder)

    for img in img_tags:
        img_url = img.get("src")
        if img_url and "tower-of-god" in img_url:  # Filtreleme (0.webp kısıtlamasını kaldırdık)
            img_url = urljoin(chapter_url, img_url)
            img_name = os.path.join(chapter_folder, img_url.split("/")[-1])

            # Resmi indirme
            try:
                img_data = requests.get(img_url).content
                with open(img_name, "wb") as img_file:
                    img_file.write(img_data)
                    print(f"{img_name} indirildi.")
            except Exception as img_e:
                print(f"{img_url} indirilirken hata oluştu: {img_e}")
                continue  # Hata durumunda devam et

    return True  # Başarılı bir şekilde indirildi


# Bölüm numarası
chapter = 601
# Tüm bölümleri indirme
while True:
    chapter_url = f"{base_url}{chapter}/"
    if chapter_url not in visited:
        print(f"{chapter_url} bölümü indiriliyor...")
        success = download_images(chapter_url)
        if not success:
            print(f"{chapter_url} bölümünde bir hata oluştu, devam edilecek.")
            break  # Hata durumunda döngüyü sonlandır
        chapter += 1  # Sonraki bölüme geç
    else:
        print(f"{chapter_url} bölümü zaten ziyaret edildi, devam ediliyor.")
        chapter += 1  # Mevcut bölümü atla ve devam et
    time.sleep(2)  # Sunucuya yük bindirmemek için bekleme süresi

print("İşlem tamamlandı!")
