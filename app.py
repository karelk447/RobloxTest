from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

# Data stores
pending_verifications = {} # {username: code}
messages = []

@app.route('/request_verify', methods=['POST'])
def request_verify():
    data = request.json
    username = data.get("username")
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    pending_verifications[username] = {"code": code, "status": "pending"}
    return jsonify({"code": code})

@app.route('/check_verify', methods=['GET'])
def check_verify():
    username = request.args.get("username")
    user_data = pending_verifications.get(username)
    if user_data and user_data.get("status") == "verified":
        return jsonify({"verified": True})
    return jsonify({"verified": False})

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    messages.append(f"{data['username']}: {data['content']}")
    return jsonify({"success": True})

@app.route('/get_updates', methods=['GET'])
def get_updates():
    # Roblox calls this to see who needs to verify and get new messages
    return jsonify({
        "verifications": pending_verifications,
        "messages": messages
    })

@app.route('/confirm_roblox', methods=['POST'])
def confirm_roblox():
    # Roblox calls this when a player enters the right code
    username = request.json.get("username")
    if username in pending_verifications:
        pending_verifications[username]["status"] = "verified"
        return jsonify({"success": True})
    return jsonify({"success": False})

if __name__ == '__main__':
    app.run(port=5000)