import sys
import yt_dlp
import os

def download_video(url):
    # Konfigurasi opsi yt-dlp
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.%(ext)s',  # Simpan dengan nama ini
        'progress_hooks': [download_progress]
    }

    # Mulai proses download
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except yt_dlp.utils.DownloadError as e:
            print(f"❌ Gagal mengunduh video: {e}")
            sys.exit(1)

def download_progress(d):
    if d['status'] == 'downloading':
        print(f"📥 Mengunduh... {d['_percent_str']} [{d['_speed_str']}]")
    elif d['status'] == 'finished':
        print("✅ Unduhan selesai! File tersimpan.")

if __name__ == "__main__":
    # Periksa apakah argumen URL diberikan
    if len(sys.argv) < 2:
        print("❌ Error: Harap masukkan URL video sebagai argumen.")
        sys.exit(1)

    # Ambil URL dari argumen
    page_url = sys.argv[1]
    print(f"🔍 Mencari video dari: {page_url}")

    # Jalankan proses download
    download_video(page_url)
