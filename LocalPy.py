import requests
import json
import sys
import time

try:
    with open("config.json", "r") as f:
        config = json.load(f)
        BASE_URL = config["BASE_URL"].rstrip("/")
except:
    print("CRITICAL: config.json missing!")
    sys.exit()

def check_online():
    try:
        return requests.get(BASE_URL, timeout=3).status_code == 200
    except:
        return False

def main():
    # Initial Wait
    print(f"Connecting to {BASE_URL}...")
    while not check_online():
        print("Waiting for server to wake up...", end="\r")
        time.sleep(2)
    print("\n[!] Server Online.")

    user = input("Username: ").strip()
    
    # Connect
    try:
        res = requests.post(f"{BASE_URL}/connect", json={"username": user})
        if res.status_code != 200:
            print(f"Error: {res.json().get('error')}")
            return
        
        print(f"Code sent to {user} in-game.")
        
        # Verify
        while True:
            code = input("Code: ").strip().upper()
            if code == "CANCEL": return
            if requests.post(f"{BASE_URL}/verify_code", json={"username": user, "code": code}).status_code == 200:
                print("Verified!")
                break
            print("Wrong code.")

        # Chat
        while True:
            msg = input("> ")
            if msg.lower() == "exit": break
            
            # Double check server status before sending
            if check_online():
                requests.post(f"{BASE_URL}/send_message", json={"username": user, "content": msg})
            else:
                print("⚠️ Message failed: Server went offline.")

    finally:
        requests.post(f"{BASE_URL}/disconnect", json={"username": user})

if __name__ == "__main__":
    main()