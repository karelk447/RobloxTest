import requests
import time

BASE_URL = "https://your-app-name.onrender.com" # Replace with your Render URL

def main():
    user = input("Enter Roblox Username: ").strip()
    
    # 1. Attempt Connection
    res = requests.post(f"{BASE_URL}/connect", json={"username": user})
    if res.status_code == 403:
        print(f"Error: {res.json()['error']}")
        return
    
    print(f"Connection requested. Look at the code on your ROBLOX screen for {user}.")
    
    # 2. Verification Loop
    while True:
        code_input = input("Enter code (or 'cancel' to quit): ").strip().upper()
        if code_input == "CANCEL":
            requests.post(f"{BASE_URL}/disconnect", json={"username": user})
            print("Cancelled.")
            return
        
        verify = requests.post(f"{BASE_URL}/verify_code", json={"username": user, "code": code_input})
        if verify.status_code == 200:
            print("Verified! Messaging active.")
            break
        print("Incorrect code. Try again.")

    # 3. Messaging
    print("(Type 'exit' to logout)")
    try:
        while True:
            text = input(f"{user}> ")
            if text.lower() == "exit": break
            requests.post(f"{BASE_URL}/send_message", json={"username": user, "content": text})
    finally:
        requests.post(f"{BASE_URL}/disconnect", json={"username": user})
        print("Disconnected.")

if __name__ == "__main__":
    main()