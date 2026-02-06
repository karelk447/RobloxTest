import requests

# REPLACE THIS with your actual Render URL after deployment
CLOUD_URL = "https://robloxtest-2h1p.onrender.com/send"

def login():
    user = input("Enter Roblox Username: ")
    msg = input("Enter Message to send: ")
    
    payload = {"username": user, "text": msg}
    
    try:
        response = requests.post(CLOUD_URL, json=payload)
        if response.status_code == 200:
            print("Successfully sent to cloud!")
        else:
            print(f"Server error: {response.status_code}")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    login()