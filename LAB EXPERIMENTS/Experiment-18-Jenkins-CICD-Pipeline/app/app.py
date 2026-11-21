"""
Experiment 18: CI/CD Pipeline with Jenkins - Sample Flask Application
Author: Angulakshmi S (Reg No: 192524402)
Department of Computer Science and Engineering
Saveetha School of Engineering, SIMATS
"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "CI/CD with Jenkins - Build successful! Deployed by Angulakshmi S (192524402)"

@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "pipeline": "Jenkins CI/CD",
        "app": "flask-cicd"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
