import requests, json, sys

# Load URL from config file
try:
    with open("config.json", "r") as f:
        BASE_URL = json.load(f)["BASE_URL"]
except Exception as e:
    print("Error: Could not read config.json")
    sys.exit()

def main():
    user = input("Username: ").strip()
    res = requests.post(f"{BASE_URL}/connect", json={"username": user})
    
    if res.status_code != 200:
        print(f"Error: {res.json().get('error', 'Unknown error')}")
        return

    print(f"Code sent to Roblox for {user}...")
    while True:
        code_in = input("Enter Code: ").strip().upper()
        if code_in == "CANCEL": 
            requests.post(f"{BASE_URL}/disconnect", json={"username": user})
            return
        
        if requests.post(f"{BASE_URL}/verify_code", json={"username": user, "code": code_in}).status_code == 200:
            print("Verified!")
            break

    try:
        while True:
            txt = input("> ")
            requests.post(f"{BASE_URL}/send_message", json={"username": user, "content": txt})
    finally:
        requests.post(f"{BASE_URL}/disconnect", json={"username": user})

if __name__ == "__main__":
    main()