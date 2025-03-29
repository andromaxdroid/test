import os
import requests
import yt_dlp
from tqdm import tqdm

def get_video_info(url):
    """Mengambil URL video dengan yt-dlp"""
    ydl_opts = {
        'quiet': True,
        'format': 'best',
        'noplaylist': True,
        'dump_single_json': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        print(f"❌ Error mengambil informasi video: {e}")
        return None

def get_file_size(url):
    """Mendapatkan ukuran file sebelum diunduh"""
    try:
        response = requests.head(url, allow_redirects=True)
        size = int(response.headers.get("content-length", 0))
        return size / (1024 * 1024)  # Convert bytes to MB
    except:
        return 0

def download_video(url, filename="video.mp4"):
    """Mengunduh video dengan progress bar & resume"""
    print(f"\n🚀 Memulai download dengan multi-threaded mode...\n")

    file_size = get_file_size(url)
    print(f"📦 Ukuran file: {file_size:.2f} MB")

    cmd = f'aria2c -x 16 -s 16 -c "{url}" -o "{filename}"'
    os.system(cmd)
    print(f"\n✅ Download selesai: {filename}")

if __name__ == "__main__":
    print("\n====== IDM-Like Video Downloader ======")
    page_url = input("Masukkan URL halaman web: ")

    print("\n🔍 Mencari video...")
    video_info = get_video_info(page_url)

    if not video_info:
        print("❌ Gagal menemukan video di halaman yang diberikan.")
    else:
        print("\n🎥 Video ditemukan! Pilih resolusi:")
        formats = video_info.get("formats", [])
        for i, fmt in enumerate(formats):
            size = get_file_size(fmt["url"])
            print(f"[{i+1}] {fmt['format']} - {size:.2f} MB - {fmt['url']}")

        choice = int(input("\nMasukkan nomor video yang ingin diunduh: ")) - 1
        selected_video = formats[choice]["url"]

        filename = input("Masukkan nama file (default: video.mp4): ") or "video.mp4"
        download_video(selected_video, filename)
