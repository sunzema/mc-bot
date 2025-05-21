# MC Bot – Slack Mesaj Silici

MC Bot, Slack üzerinde slash komutuyla kullanıcıların son mesajlarını silmelerini sağlayan basit bir bot uygulamasıdır.

## Özellikler
- `/sil 5` komutuyla son 5 mesajını siler
- Sadece komutu yazan kişinin mesajlarını siler
- Flask ile yazılmıştır, Render üzerinde barındırılabilir

## Kurulum

### 1. GitHub Repo
Bu dosyaları bir GitHub reposuna yükle (`mc-bot` adında olabilir).

### 2. Render Üzerinde Web Servis Oluştur

- Build Command: `pip install -r requirements.txt`
- Start Command: `python app.py`
- Environment Variable ekle:
  - Key: `SLACK_BOT_TOKEN`
  - Value: Slack Bot Token'ın

### 3. Slack App Ayarları

- Slash Command:
  - Komut: `/sil`
  - URL: `https://mc-bot.onrender.com/sil` (örnek)
- Gerekli izinler:
  - `chat:write`
  - `channels:history`
  - `chat:delete`

## Kullanım

Slack’te:
```
/sil 10
```

komutunu yazarak MC Bot’un son 10 mesajını silmesini sağlayabilirsin.

---

MC Bot ile Slack'ini temiz tut. ✨
