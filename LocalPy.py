import requests
import time

# REPLACE THIS with your Render URL (must have https://)
BASE_URL = "https://robloxtest-2h1p.onrender.com"

username = input("Enter Roblox Username to verify: ")

try:
    print("Connecting to server...")
    res = requests.post(f"{BASE_URL}/request_verify", json={"username": username}, timeout=30)
    res.raise_for_status()
    
    code = res.json()['code']
    print(f"\n[!] YOUR CODE IS: {code}")
    print("[!] Join the game and type this code in chat.\n")

    # Polling for verification status
    verified = False
    while not verified:
        try:
            check = requests.get(f"{BASE_URL}/check_verify", params={"username": username}).json()
            if check.get("verified"):
                print("Successfully Verified!")
                verified = True
            else:
                time.sleep(3)
        except Exception:
            time.sleep(3)

    # Chat loop
    print("--- Chat Room Active (Ctrl+C to quit) ---")
    while True:
        msg = input(f"{username}> ")
        if msg.strip():
            requests.post(f"{BASE_URL}/send_message", json={"username": username, "content": msg})

except requests.exceptions.HTTPError as e:
    print(f"Server Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")