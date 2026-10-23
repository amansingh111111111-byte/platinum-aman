import os
import requests
import pyotp
from dotenv import dotenv_values
from pathlib import Path

config = dotenv_values("dhan.env")
client_id = config.get("DHAN_CLIENT_ID", "").strip()
pin = config.get("DHAN_PIN", "").strip()
secret = config.get("DHAN_TOTP_SECRET", "").strip()

if not all((client_id, pin, secret)):
    raise SystemExit("Missing configuration. Check dhan.env locally.")

totp = pyotp.TOTP(secret).now()
url = "https://auth.dhan.co/app/generateAccessToken"
params = {
    "dhanClientId": client_id,
    "pin": pin,
    "totp": totp,
}

try:
    response = requests.post(url, params=params, timeout=20)
    try:
        data = response.json()
    except ValueError:
        raise SystemExit(
            f"Dhan returned non-JSON response (HTTP {response.status_code})."
        )

    token = data.get("accessToken") if isinstance(data, dict) else None

    if response.ok and token:
        token_path = Path.home() / ".platinum_dhan_token"
        temp_path = token_path.with_suffix(".tmp")
        temp_path.write_text(token + "\n")
        os.chmod(temp_path, 0o600)
        temp_path.replace(token_path)
        print("Authentication succeeded. Token saved to a private file.")
        print("Token value was not displayed.")
    else:
        print(f"Authentication did not succeed (HTTP {response.status_code}).")
        if isinstance(data, dict):
            print("Dhan response fields:", ", ".join(sorted(data.keys())))
            if data.get("errorMessage"):
                print("Dhan message:", str(data["errorMessage"])[:250])
            elif data.get("message"):
                print("Dhan message:", str(data["message"])[:250])
        else:
            print("Unexpected response format.")

except requests.RequestException as exc:
    print("Network request failed:", type(exc).__name__)
