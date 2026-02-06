import requests
import time

BASE_URL = "https://robloxtest-2h1p.onrender.com" # Change this!

def main():
    username = input("Enter your Roblox Username: ")
    
    # 1. Wait for server to generate a code
    print(f"Checking status for {username}...")
    while True:
        resp = requests.get(f"{BASE_URL}/get_status/{username}").json()
        if resp['status'] == 'verified':
            print("Already verified!")
            break
        else:
            code = input(f"Enter the verification code shown in Roblox for {username}: ")
            v_resp = requests.post(f"{BASE_URL}/verify", json={"username": username, "code": code}).json()
            if v_resp.get("success"):
                print("Verification Successful!")
                break
            print("Wrong code, try again.")

    # 2. Message Loop (No more verification needed)
    print("\n--- Chat Mode Enabled ---")
    while True:
        msg = input("Message: ")
        if msg.lower() == "exit": break
        
        requests.post(f"{BASE_URL}/send", json={"username": username, "text": msg})
        print("Sent!")

if __name__ == "__main__":
    main()