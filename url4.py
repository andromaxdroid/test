import os
import sys
import argparse
import requests
import yt_dlp
from tqdm import tqdm

def get_video_info(url):
    """Mengambil informasi video dengan yt-dlp"""
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
    """Mendapatkan ukuran file sebelum diunduh (dalam MB)"""
    try:
        response = requests.head(url, allow_redirects=True)
        size = int(response.headers.get("content-length", 0))
        return size / (1024 * 1024)  # Convert bytes ke MB
    except Exception:
        return 0

def download_video(url, filename="video.mp4"):
    """Mengunduh video menggunakan aria2c dengan multi-threading dan resume"""
    print(f"\n🚀 Memulai download dengan multi-threaded mode...\n")
    file_size = get_file_size(url)
    print(f"📦 Ukuran file: {file_size:.2f} MB")
    
    # Perintah aria2c: -x 16 (max connection per server), -s 16 (segmen per download), -c (lanjutkan download)
    cmd = f'aria2c -x 16 -s 16 -c "{url}" -o "{filename}"'
    os.system(cmd)
    print(f"\n✅ Download selesai: {filename}")

def select_format(formats, resolution):
    """
    Pilih format video yang sesuai dengan resolusi yang diinginkan.
    Contoh: resolution = "1080p", "720p", "480p", "360p", "240p"
    """
    for fmt in formats:
        fmt_str = fmt.get('format', '')
        if resolution in fmt_str:
            return fmt.get('url')
    return None

def main():
    parser = argparse.ArgumentParser(description="IDM-Like Video Downloader")
    parser.add_argument('-url', required=True, help="URL halaman video")
    parser.add_argument('-r', '--resolution', required=True, help="Resolusi video (1080p, 720p, 480p, 360p, 240p)")
    parser.add_argument('-o', '--output', default="video.mp4", help="Nama file output (default: video.mp4)")
    args = parser.parse_args()
    
    page_url = args.url
    resolution = args.resolution
    output_file = args.output
    
    print(f"🔍 Mencari video dari: {page_url}")
    video_info = get_video_info(page_url)
    
    if not video_info:
        print("❌ Gagal menemukan video di halaman yang diberikan.")
        sys.exit(1)
        
    formats = video_info.get("formats", [])
    selected_video = select_format(formats, resolution)
    
    if not selected_video:
        print(f"❌ Tidak ditemukan format dengan resolusi {resolution}.")
        sys.exit(1)
        
    download_video(selected_video, output_file)

if __name__ == "__main__":
    main()
