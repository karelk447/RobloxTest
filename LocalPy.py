import requests
import json
import sys
import time

try:
    with open("config.json", "r") as f:
        BASE_URL = json.load(f)["BASE_URL"].rstrip("/")
except:
    print("CRITICAL: config.json missing!")
    sys.exit()

def check_online():
    try: return requests.get(BASE_URL, timeout=3).status_code == 200
    except: return False

def main():
    print(f"Connecting to {BASE_URL}...")
    while not check_online():
        print("Waiting for server to wake up...", end="\r")
        time.sleep(2)
    print("\n[!] Server Online.")

    user = input("Enter Roblox Username: ").strip()
    
    res = requests.post(f"{BASE_URL}/connect", json={"username": user})
    if res.status_code != 200:
        print(f"Error: {res.json().get('error', 'Player not found in-game')}")
        return
    
    print(f"Code sent to {user} in-game. Please verify.")
    
    while True:
        code = input("Code: ").strip().upper()
        if code == "CANCEL": return
        if requests.post(f"{BASE_URL}/verify_code", json={"username": user, "code": code}).status_code == 200:
            print("Verified! Your messages will appear as Bubbles in-game.")
            break
        print("Wrong code.")

    try:
        while True:
            msg = input(f"{user}> ")
            if msg.lower() == "exit": break
            if msg.strip():
                requests.post(f"{BASE_URL}/send_message", json={"username": user, "content": msg})
    finally:
        requests.post(f"{BASE_URL}/disconnect", json={"username": user})

if __name__ == "__main__":
    main()