# Google OAuth2 Endpoints for Dukick Drive Integration

## Authorization URL Template
```
https://accounts.google.com/o/oauth2/auth?
  client_id=553888273742-03danr8q3i40uuhodfgiop73lvdmu28d.apps.googleusercontent.com
  &redirect_uri=http://localhost:8499/
  &scope=https://www.googleapis.com/auth/documents%20https://www.googleapis.com/auth/spreadsheets%20https://www.googleapis.com/auth/drive
  &response_type=code
  &access_type=offline
  &prompt=consent
```

## Token Exchange Endpoint
```
POST https://oauth2.googleapis.com/token
Content-Type: application/x-www-form-urlencoded
```

Body params:
- `code` — from redirect URL
- `client_id`
- `client_secret`
- `redirect_uri` — must match exactly what was used in auth URL
- `grant_type=authorization_code`

## Refresh Endpoint
```
POST https://oauth2.googleapis.com/token
```
Body:
- `client_id`
- `client_secret`
- `refresh_token`
- `grant_type=refresh_token`

## Drive API Base URLs
- Upload: `https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart`
- Files: `https://www.googleapis.com/drive/v3/files`
- Permissions: `https://www.googleapis.com/drive/v3/files/{file_id}/permissions`
- About: `https://www.googleapis.com/drive/v3/about?fields=user`

## Docs API
- Documents: `https://docs.googleapis.com/v1/documents`
- BatchUpdate: `POST https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate`

## Sheets API
- Spreadsheets: `https://sheets.googleapis.com/v4/spreadsheets`
- Values: `https://sheets.googleapis.com/v4/spreadsheets/{id}/values/{range}`

## Scopes Used
- `https://www.googleapis.com/auth/drive` — Full Drive access
- `https://www.googleapis.com/auth/documents` — Google Docs
- `https://www.googleapis.com/auth/spreadsheets` — Google Sheets

## Account Info
- Display Name: Dukick Editor
- Email: editor.dukick@gmail.com
- Project ID: agenthermesdukick
