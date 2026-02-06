import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import string

app = Flask(__name__)
CORS(app)

# Data stores
pending_verifications = {} 
messages = []

@app.route('/')
def home():
    return "Server is Online", 200

@app.route('/request_verify', methods=['POST'])
def request_verify():
    data = request.json
    username = data.get("username")
    if not username:
        return jsonify({"error": "Username required"}), 400
    
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
    if data and "username" in data and "content" in data:
        messages.append(f"{data['username']}: {data['content']}")
        return jsonify({"success": True})
    return jsonify({"error": "Invalid data"}), 400

@app.route('/get_updates', methods=['GET'])
def get_updates():
    return jsonify({
        "verifications": pending_verifications,
        "messages": messages
    })

@app.route('/confirm_roblox', methods=['POST'])
def confirm_roblox():
    data = request.json
    username = data.get("username")
    if username in pending_verifications:
        pending_verifications[username]["status"] = "verified"
        return jsonify({"success": True})
    return jsonify({"success": False})

if __name__ == '__main__':
    # Render Dynamic Port Binding
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)