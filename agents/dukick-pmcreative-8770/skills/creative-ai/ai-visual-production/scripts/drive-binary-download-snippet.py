"""
Safe binary download from Google Drive using the Dukick drive_tool service account.
Copy-paste this into a script when you need to download images, audio, GIFs, or any non-text file.
"""
import io
import sys

# Adjust path to where drive_tool.py lives
sys.path.insert(0, r"C:\DuKickAgent")
from drive_tool import get_service
from googleapiclient.http import MediaIoBaseDownload


def download_binary(file_id: str, out_path: str) -> None:
    """Download a Google Drive file as raw bytes. Suitable for images, audio, video, GIFs."""
    svc = get_service()
    request = svc.files().get_media(fileId=file_id)
    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    with open(out_path, "wb") as f:
        f.write(buf.getvalue())
    print(f"Downloaded: {out_path}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Download a Google Drive file as binary.")
    parser.add_argument("file_id", help="Google Drive file ID")
    parser.add_argument("out_path", help="Local output path")
    args = parser.parse_args()
    download_binary(args.file_id, args.out_path)
