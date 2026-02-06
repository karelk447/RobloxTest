import os
from flask import Flask, request, jsonify

app = Flask(__name__)
pending_messages = {}

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    username = data.get("username")
    text = data.get("text")
    pending_messages[username] = text
    print(f"Stored message for {username}")
    return jsonify({"status": "received"}), 200

@app.route('/get/<username>', methods=['GET'])
def get_message(username):
    # This is what Roblox calls
    message = pending_messages.pop(username, None)
    return jsonify({"message": message}), 200

if __name__ == "__main__":
    # Crucial for Render/Cloud: Use the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)