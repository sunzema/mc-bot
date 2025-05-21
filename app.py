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
    
    print(f"Channel ID: {channel_id}, User ID: {user_id}, Amount: {amount}")

    history = requests.get(
        "https://slack.com/api/conversations.history",
        headers=headers,
        params={"channel": channel_id, "limit": 10000}
    ).json()

    print(f"Channel: {channel_id}, User: {user_id}")
    print(f"Messages fetched: {len(history.get('messages', []))}")
     for msg in history.get("messages", []):
        print(f"Message ts: {msg.get('ts')}, user: {msg.get('user')}, subtype: {msg.get('subtype')}")

    # Silme işlemi devam eder...

    return jsonify({"response_type": "ephemeral", "text": "Silme işlemi tamamlandı."})
    silinenler = 0
    for msg in history.get("messages", []):
        print(f"Message user: {msg.get('user')}, subtype: {msg.get('subtype')}")
        if msg.get("user") == user_id and "subtype" not in msg:
            delete_resp = requests.post(
                "https://slack.com/api/chat.delete",
                headers=headers,
                json={"channel": channel_id, "ts": msg["ts"]}
            )
            print(f"Deleting message ts={msg['ts']} result: {delete_resp.json()}")
            if delete_resp.json().get("ok"):
                silinenler += 1
            if silinenler >= amount:
                break

    if silinenler == 0:
        return jsonify({
            "response_type": "ephemeral",
            "text": f"🤖 MC Bot: Bu kanalda silinecek mesaj bulunamadı."
        })
    else:
        return jsonify({
            "response_type": "ephemeral",
            "text": f"🤖 MC Bot: <@{user_id}> - Son {silinenler} mesajın silindi."
        })
if __name__ == "__main__":
   import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port, debug=True)
