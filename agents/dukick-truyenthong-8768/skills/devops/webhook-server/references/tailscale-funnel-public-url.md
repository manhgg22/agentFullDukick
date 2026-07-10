# Public URL cho Webhook Server (Tailscale Funnel)

## Tóm tắt
- Tailscale Funnel → URL **cố định** (không đổi khi restart)
- Cloudflare Quick Tunnel → URL thay đổi mỗi lần restart

## Cấu hình Tailscale Funnel (Windows + MSYS/Git Bash)

### 1. Kiểm tra Tailscale chạy

```bash
tailscale status
tailscale ip -4          # lấy tailnet IP
tailscale serve status    # xem serve hiện tại
tailscale funnel status   # xem funnel hiện tại
```

### 2. Serve (tailnet only) vs Funnel (public internet)

| Lệnh | Phạm vi | Dùng khi |
|------|---------|----------|
| `tailscale serve` | Chỉ trong tailnet (các máy cùng account) | Truy cập nội bộ giữa team |
| `tailscale funnel` | Public internet (bất kỳ ai) | Zalo, Stripe, webhook từ bên ngoài |

### 3. Expose port qua Funnel

```bash
# Map root path "/" → port 8888 (KHÔNG dùng --set-path)
tailscale funnel --bg http://127.0.0.1:8888

# Kết quả: https://admin-pc-1.tailc0eb7b.ts.net/ → proxy → localhost:8888
```

> ⚠️ **KHÔNG dùng `--set-path=/webhook`** vì path bị cắt lúc forward. Webhook server đã có route `/webhook/zalo`, nên map root `/` để giữ nguyên path.

### 4. MSYS Path Conversion Bug

Trên Git Bash / MSYS, `tailscale serve --set-path=/webhook` bị MSYS convert path thành `C:/Program Files/Git/webhook`.

**Fix:** Set env var trước khi chạy:

```bash
export MSYS_NO_PATHCONV=1
tailscale funnel --bg http://127.0.0.1:8888
```

### 5. Kiểm tra

```bash
# Xem status
tailscale funnel status
# hoặc
tailscale serve status

# Test public URL
curl -s "https://admin-pc-1.tailc0eb7b.ts.net/health"
curl -s -X POST "https://admin-pc-1.tailc0eb7b.ts.net/webhook/zalo" \
  -H "Content-Type: application/json" \
  -d '{"event_name":"user_send_text","sender":{"id":"test"},"message":{"text":"hi"}}'
```

### 6. Tắt Funnel

```bash
tailscale funnel --https=443 off
```

## So sánh các phương án Public URL

| Phương án | Cố định? | Cần setup | Độ tin cậy |
|-----------|----------|-----------|------------|
| Tailscale Funnel | ✅ Yes | Tailscale đã có sẵn | Cao (production-ready) |
| Cloudflare Quick Tunnel | ❌ No | Chỉ cần cloudflared | Trung bình (temp) |
| Cloudflare Named Tunnel | ✅ Yes | Cần CF account + domain | Cao |
| ngrok | ❌ No (free tier) | Chỉ cần ngrok | Trung bình |
| ngrok (paid) | ✅ Yes | Paid plan | Cao |

## URL hiện tại của Dukick

```
https://admin-pc-1.tailc0eb7b.ts.net/
├── /webhook/zalo          (Zalo Bot Platform)
├── /webhook/<source>      (Generic webhooks)
├── /webhook/debt/update   (Debt status updates)
└── /health                (Health check)
```
