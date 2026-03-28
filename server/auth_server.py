import os
from flask import Flask, request, jsonify
import requests
import hashlib
app = Flask(__name__)
BIN_ID = os.environ.get("JSON_BIN_ID")
BIN_URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
API_KEY = os.environ.get("BIN_API_KEY")

@app.route("/database", methods=['POST'])
def handle_db():
    if not API_KEY:
        return jsonify({'message': 'Server does not have api key.'}), 500
    HEADERS = {
    "X-Master-Key": API_KEY,
    "Content-Type": "application/json"
    }   
    req_data = request.json
    mode = req_data.get("mode")
    username_attempt = req_data.get("username").lower()
    password_attempt = req_data.get("password")
    response = requests.get(BIN_URL, headers=HEADERS)
    response.raise_for_status()
    json_read_data = response.json()["record"]
    if mode == "login":
        user_exists = False
        for user in json_read_data['users']:
            salt = user["salt"]
            hashed_password = user["password"]
            hashed_password_attempt = hashlib.sha256((password_attempt+salt).encode()).hexdigest()
            if username_attempt == user["username"]:
                user_exists = True
                if hashed_password_attempt == hashed_password:
                    return jsonify({"message": "Logged in."}), 200
        if user_exists == True:
            return jsonify({'message': 'Invalid password.'}), 401
        else:
            return jsonify({'message': 'Username does not exist in database.'}), 404
    elif mode == "register":
        user_exists = False
        for user in json_read_data['users']:
            if username_attempt == user["username"]:
                return jsonify({'message': 'Username already exists. Try another one.'}), 409
        salt = os.urandom(16).hex()
        hashed_password = hashlib.sha256((password_attempt+salt).encode()).hexdigest()
        json_read_data['users'].append({
            'username': username_attempt,
            'password': hashed_password,
            'salt': salt
        })
        response = requests.put(BIN_URL, headers=HEADERS, json=json_read_data)
        return jsonify({'message': 'Succesfully registered username and password into database.'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

