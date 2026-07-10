# Shared Dukick utilities

Scripts/creds dung chung cho 5 Hermes agent.

## upload_to_drive.py

Upload file len Google Drive Tong Dukick qua Service Account.

### Yeu cau

1. JSON key tai `shared/gcp/dukick-service-account.json` (KHONG commit - da gitignore)
2. Folder root "Drive Tong Dukick" da share voi email SA (Editor)
3. Python deps (da co trong venv): `google-api-python-client`, `google-auth-httplib2`

### Usage

```powershell
C:\DuKickAgent\venv\Scripts\python.exe C:\DuKickAgent\shared\upload_to_drive.py `
    "C:\path\to\file.docx" --folder "SEO/2026" --share --overwrite
```

Output stdout (JSON):
```json
{"file_id":"1Abc...","link":"https://drive.google.com/file/d/1Abc.../view","folder":"SEO/2026","name":"file.docx"}
```

Exit 0 = OK, 1 = error (stderr JSON). Hook-safe: khong crash bot.

### Env vars

- `DUKICK_SA_KEY` - duong dan JSON key (default `shared/gcp/dukick-service-account.json`)
- `DUKICK_DRIVE_ROOT` - ten root folder (default `Drive Tong Dukick`)

### Setup GCP (lam 1 lan)

1. https://console.cloud.google.com → tao project `dukick-agents`
2. APIs & Services → Enable **Google Drive API**
3. IAM & Admin → Service Accounts → Create `dukick-uploader` → download JSON key
4. Dat JSON key vao `shared/gcp/dukick-service-account.json`
5. Drive: share folder "Drive Tong Dukick" voi email SA `dukick-uploader@dukick-agents.iam.gserviceaccount.com` → Editor
6. Test: `python shared/upload_to_drive.py test.txt --folder _test --share`