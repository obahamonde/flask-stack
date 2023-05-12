"""App entry point."""
import socket
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def index():
    """Index page."""
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    return jsonify(host_name=host_name, host_ip=host_ip)