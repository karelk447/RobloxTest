import requests
import time

BASE_URL = "https://robloxtest-2h1p.onrender.com" # Use localhost for testing
username = input("Enter Roblox Username: ")

# 1. Request Verification
res = requests.post(f"{BASE_URL}/request_verify", json={"username": username})
code = res.json()['code']
print(f"Your verification code is: {code}")
print("Please enter this in the Roblox game...")

# 2. Wait for Roblox to confirm
verified = False
while not verified:
    check = requests.get(f"{BASE_URL}/check_verify", params={"username": username}).json()
    if check.get("verified"):
        print("Verified successfully!")
        verified = True
    else:
        time.sleep(2)

# 3. Chat loop
while True:
    msg = input("Type a message: ")
    requests.post(f"{BASE_URL}/send_message", json={"username": username, "content": msg})