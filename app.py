from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

# Config — replace these with your actual values
CLIENT_ID = "Uomay4DRutkcoW2jsK66IWNczOhQq4aVBhad32fa"
CLIENT_SECRET = "o4ulDyW98ODtKWC1nxg41i4aG4J0RNsPw8dI0hfi3tt6rcC5mLGOuRIqtEhkEMAxsHBkRt0YinXCSyfsqZaDXi7TkTvKYcihUheoTfFPVwUOzVQNCVBbv1avoVtlR2Os"
TOKEN_URL = "https://uatapi.tarrakki.com/access_token"  # Replace with actual token endpoint

# Store token and expiration time
token_data = {
    "access_token": None,
    "expires_at": 0
}

def get_new_token():
    print("Fetching new token...")
    response = requests.post(TOKEN_URL, data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    })

    if response.status_code == 200:
        data = response.json()
        token_data["access_token"] = data["access_token"]
        token_data["expires_at"] = time.time() + data["expires_in"] - 60  # Subtract 60s as buffer
    else:
        print("Failed to fetch token:", response.text)

@app.route("/get-access-token", methods=["GET"])
def serve_token():
    # Refresh token if expired or not set
    if not token_data["access_token"] or time.time() >= token_data["expires_at"]:
        get_new_token()

    return jsonify({
        "token_type": "Bearer",
        "access_token": token_data["access_token"]
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
