# api/index.py

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "Trading Journal API",
        "message": "Welcome!"
    })

# Vercel expects the `app` variable to be present
# No need to call app.run() — Vercel handles this
