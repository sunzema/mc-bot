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

    history = requests.get(
        "https://slack.com/api/conversations.history",
        headers=headers,
        params={"channel": channel_id, "limit": 100}
    ).json()

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
            if delete_resp.json().get("ok"):
                silinenler += 1
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
