import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

headers = {
    "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
    "Content-Type": "application/json"
}

@app.route("/sil", methods=["POST"])
def sil():
    channel_id = request.form.get("channel_id")
    user_id = request.form.get("user_id")
    text = request.form.get("text", "").strip()
    amount = int(text) if text.isdigit() else 1

    # Mesaj geçmişini çek
    history = requests.get(
    "https://slack.com/api/conversations.history",
    headers=headers,
    params={"channel": channel_id, "limit": 100}
).json()

print("Conversations.history response:", history)  # Önce mesajları kontrol et

if not history.get("messages"):
    return jsonify({
        "response_type": "ephemeral",
        "text": "🤖 MC Bot: Bu kanalda silinecek mesaj bulunamadı."
    })

silinenler = 0
for msg in history.get("messages", []):
    if msg.get("user") == user_id and "subtype" not in msg:
        delete_resp = requests.post(
            "https://slack.com/api/chat.delete",
            headers=headers,
            json={"channel": channel_id, "ts": msg["ts"]}
        )
        delete_json = delete_resp.json()
        print("chat.delete response:", delete_json)  # Silme isteğinin sonucunu göster

        if delete_json.get("ok"):
            silinenler += 1
        else:
            print(f"Mesaj silme başarısız: {delete_json.get('error')}")

        if silinenler >= amount:
            break


    return jsonify({
        "response_type": "ephemeral",
        "text": f"🤖 MC Bot: <@{user_id}> - Son {silinenler} mesajın silindi."
    })
if __name__ == "__main__":
   import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port, debug=True)
