import requests
from bs4 import BeautifulSoup
import json

# URL artikel yang Anda buka di gambar sebelumnya
url = "https://umsida.ac.id/risiko-aset-kripto-dan-bitcoin-menurut-dosen-umsida/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

def scraping_ke_json():
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        list_hasil = []

        # 1. Ambil Judul Utama (Menggunakan tag h1 yang biasanya ada di artikel)
        judul_utama = soup.find('h1')
        if judul_utama:
            list_hasil.append({
                "kategori": "Berita Utama",
                "judul": judul_utama.text.strip(),
                "link": url
            })

        # 2. Ambil Berita Lainnya (Mencari semua link yang ada di dalam sidebar atau list)
        # Kita cari elemen <a> yang berada di dalam widget atau area post terbaru
        for link_tag in soup.find_all('a', href=True):
            # Kita filter agar hanya mengambil judul yang panjangnya masuk akal (bukan menu)
            title = link_tag.text.strip()
            link = link_tag['href']
            
            # Filter: Judul berita biasanya panjang dan linknya mengandung kata kunci tertentu
            if len(title) > 30 and "umsida.ac.id" in link and link != url:
                list_hasil.append({
                    "kategori": "Berita Terkait/Terbaru",
                    "judul": title,
                    "link": link
                })

        # Simpan ke file
        with open('hasil_scraping_umsida.json', 'w', encoding='utf-8') as f:
            json.dump(list_hasil, f, indent=4, ensure_ascii=False)
        
        print(f"Selesai! Berhasil mengambil {len(list_hasil)} data.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scraping_ke_json()