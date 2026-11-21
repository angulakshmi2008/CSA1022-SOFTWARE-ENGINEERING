"""
Experiment 19: Continuous Deployment of a Dockerized Application using GitHub Actions
Author: Angulakshmi S (Reg No: 192524402)
Department of Computer Science and Engineering
Saveetha School of Engineering, SIMATS
"""

import os
from flask import Flask, jsonify

app = Flask(__name__)

VERSION = "Version 1.0 - Deployed automatically with GitHub Actions"

@app.route("/")
def home():
    return jsonify({
        "status": "LIVE",
        "version": VERSION,
        "author": "Angulakshmi S",
        "reg_no": "192524402",
        "course": "CSA10 - Software Engineering",
        "ci_cd_platform": "GitHub Actions",
        "registry": "Docker Hub"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "HEALTHY",
        "uptime": "OK"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
