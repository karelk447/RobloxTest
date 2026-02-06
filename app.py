import os
import time
import random
import string
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Storage: { "username": { "status": "pending"|"active", "code": "123456" } }
sessions = {}
# Chat history
messages = []
# Event flag for instant messaging
new_msg_arrival = False

@app.route('/connect', methods=['POST'])
def connect():
    username = request.json.get("username")
    # Check if this specific account is already in use by another Py client
    if username in sessions and sessions[username]["status"] == "active":
        return jsonify({"error": f"Account {username} is already connected elsewhere."}), 403
    
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    sessions[username] = {"code": code, "status": "pending"}
    return jsonify({"code": code})

@app.route('/verify_code', methods=['POST'])
def verify_code():
    data = request.json
    username, code = data.get("username"), data.get("code")
    
    if username in sessions and sessions[username]["code"] == code:
        sessions[username]["status"] = "active"
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Invalid code"}), 401

@app.route('/send_message', methods=['POST'])
def send_message():
    global new_msg_arrival
    data = request.json
    messages.append(f"{data['username']}: {data['content']}")
    new_msg_arrival = True # Trigger long poll wake-up
    return jsonify({"success": True})

@app.route('/poll_updates', methods=['GET'])
def poll_updates():
    global new_msg_arrival
    # Long Polling: Wait up to 20 seconds for activity
    start = time.time()
    while not new_msg_arrival and (time.time() - start) < 20:
        time.sleep(0.5)
    
    new_msg_arrival = False
    return jsonify({"verifications": sessions, "messages": messages})

@app.route('/disconnect', methods=['POST'])
def disconnect():
    username = request.json.get("username")
    if username in sessions:
        del sessions[username]
    return jsonify({"success": True})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)