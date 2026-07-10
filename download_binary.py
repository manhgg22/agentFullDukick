
import sys
sys.path.insert(0, "C:/DuKickAgent")
from drive_tool import get_service
import io
from googleapiclient.http import MediaIoBaseDownload

svc = get_service()
file_id = sys.argv[1]
out_path = sys.argv[2]

request = svc.files().get_media(fileId=file_id)
buf = io.BytesIO()
downloader = MediaIoBaseDownload(buf, request)
done = False
while not done:
    _, done = downloader.next_chunk()

with open(out_path, "wb") as f:
    f.write(buf.getvalue())
print("Downloaded:", out_path)
