from flask import Flask, request, jsonify
import requests
import getpass
import os
server_ip = os.environ.get("server_ip")
port = "5000"
mode = input(f'1 to login. 2 to register. ')
while mode not in ['1', '2']:
    mode = input(f'1 to login. 2 to register. ')
mode_map = {'1': 'login', '2': 'register'}
selected_mode = mode_map[mode]
server_url = (f'http://{server_ip}:{port}/database')
username = input("Username: ").lower()
password = getpass.getpass("Password: ")
payload = {
    "mode": selected_mode,
    "username": username,
    "password": password
}
response = requests.post(server_url, json=payload)
results = response.json()
if response.status_code == 200:
    print(f'Success: {results.get('message')}')
else:
    print(f'Error: {response.status_code}: {results.get('message')}')
