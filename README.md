Simple Remote Auth System:
A basic authentication setup using Python, Flask, and JSONBin. It runs a backend on an Oracle VPS to keep credentials off the client.
///
Quick Setup:
Database: Create a JSONBin bin with {"users": []} as the starting structure.
///
Server (VPS):
Save your Bin ID as JSON_BIN_ID in your environment variables.
Save your Master API Key as BIN_API_KEY.
Run python auth_server.py.
///
Client (Local):
Save your server's IP as server_ip in your environment variables.
Run python auth_client.py.
///
Security Note:
I’ve set this up to use environment variables for keys and IPs so you don't accidentally leak them. If you're going to fork this or share it, don't hardcode your credentials—keep them in your environment.
