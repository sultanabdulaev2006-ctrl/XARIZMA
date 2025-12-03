import requests
import json
import getpass
import time
from datetime import datetime

# --- Game Service Configuration ---
FIREBASE_API_KEY = 'YOUR_FIREBASE_KEY'
FIREBASE_LOGIN_URL = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={FIREBASE_API_KEY}"
RANK_URL = "https://us-central1-cp-multiplayer.cloudfunctions.net/SetUserRating4"
CLAN_ID_URL = "https://us-central1-cp-multiplayer.cloudfunctions.net/GetClanId"

# --- Telegram Bot Configuration ---
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = 0   # не используется

def login(email, password):
    print("\n🔐 Logging in to CPM1...")
    payload = {
        "clientType": "CLIENT_TYPE_ANDROID",
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12)",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(FIREBASE_LOGIN_URL, headers=headers, json=payload)
        response_data = response.json()

        if response.status_code == 200 and 'idToken' in response_data:
            print("✅ Login successful!")
            return response_data.get('idToken')
        else:
            error_message = response_data.get("error", {}).get("message", "Unknown error during login.")
            print(f"❌ Login failed: {error_message}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return None


def set_rank(token):
    print("👑 Injecting KING RANK...")
    rating_data = {k: 100000 for k in [
        "cars", "car_fix", "car_collided", "car_exchange", "car_trade", "car_wash",
        "slicer_cut", "drift_max", "drift", "cargo", "delivery", "taxi", "levels", "gifts",
        "fuel", "offroad", "speed_banner", "reactions", "police", "run", "real_estate",
        "t_distance", "treasure", "block_post", "push_ups", "burnt_tire", "passanger_distance"
    ]}
    rating_data["time"] = 10000000000
    rating_data["race_win"] = 3000

    payload = {"data": json.dumps({"RatingData": rating_data})}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "okhttp/3.12.13"
    }

    try:
        response = requests.post(RANK_URL, headers=headers, json=payload)
        if response.status_code == 200:
            print("✅ Rank successfully set!")
            return True
        else:
            print(f"❌ Failed to set rank. HTTP Status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error during rank set: {e}")
        return False


def check_clan_id(token, email, password):
    """Теперь просто проверяет ClanId без отправки в Telegram."""
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "okhttp/3.12.13",
        "Content-Type": "application/json"
    }
    payload = {"data": None}

    try:
        response = requests.post(CLAN_ID_URL, headers=headers, json=payload)
        if response.status_code == 200:
            raw = response.json()
            clan_id = raw.get("result", "")
            # ничего не отправляем
    except requests.exceptions.RequestException:
        pass


def main_logic():
    while True:
        print("\nFree King Rank & Daily Task")
        try:
            email = input("📧 Enter email: ").strip()
            password = input("🔒 Enter password: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        auth_token = login(email, password)
        if auth_token:
            if set_rank(auth_token):
                check_clan_id(auth_token, email, password)
                print("\n✅ Operation completed.")


if __name__ == "__main__":
    main_logic()
