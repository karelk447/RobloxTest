import os, time, random, string, json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

sessions = {}
online_players = []
messages = []

# This is the endpoint the client uses to check if server is awake
@app.route('/')
def health_check():
    return "OK", 200

@app.route('/roblox_sync', methods=['POST'])
def roblox_sync():
    global online_players
    data = request.json
    online_players = data.get("players", [])
    return jsonify({"sessions": sessions, "messages": messages})

@app.route('/connect', methods=['POST'])
def connect():
    username = request.json.get("username")
    if username not in online_players:
        return jsonify({"error": "Player not in-game"}), 404
    if username in sessions and sessions[username]["status"] == "active":
        return jsonify({"error": "Account already active"}), 403
    
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    sessions[username] = {"code": code, "status": "pending"}
    return jsonify({"code": code})

@app.route('/verify_code', methods=['POST'])
def verify_code():
    data = request.json
    user, code = data.get("username"), data.get("code")
    if user in sessions and sessions[user]["code"] == code:
        sessions[user]["status"] = "active"
        return jsonify({"success": True})
    return jsonify({"success": False}), 401

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    messages.append(f"{data['username']}: {data['content']}")
    return jsonify({"success": True})

@app.route('/disconnect', methods=['POST'])
def disconnect():
    username = request.json.get("username")
    if username in sessions: del sessions[username]
    return jsonify({"success": True})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)