import os
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

# Data storage
pending_codes = {}    # {username: "1234"}
verified_users = set() # {username1, username2}
pending_messages = {} # {username: "Hello"}

@app.route('/get_status/<username>', methods=['GET'])
def get_status(username):
    # Roblox checks this. If no code exists, generate one.
    if username not in verified_users:
        if username not in pending_codes:
            pending_codes[username] = str(random.randint(1000, 9999))
        return jsonify({"status": "unverified", "code": pending_codes[username]}), 200
    return jsonify({"status": "verified"}), 200

@app.route('/verify', methods=['POST'])
def verify_user():
    data = request.json
    username, code = data.get("username"), data.get("code")
    
    if pending_codes.get(username) == code:
        verified_users.add(username)
        pending_codes.pop(username, None)
        return jsonify({"success": True}), 200
    return jsonify({"success": False, "error": "Invalid Code"}), 400

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    username, text = data.get("username"), data.get("text")
    
    if username in verified_users:
        pending_messages[username] = text
        return jsonify({"status": "sent"}), 200
    return jsonify({"error": "Not verified"}), 403

@app.route('/poll/<username>', methods=['GET'])
def poll_message(username):
    msg = pending_messages.pop(username, None)
    return jsonify({"message": msg}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))