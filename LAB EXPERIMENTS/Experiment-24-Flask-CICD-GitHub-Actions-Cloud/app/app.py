import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify(
        message="Flask CI/CD with GitHub Actions",
        status="running",
        student="Angulakshmi S",
        reg_no="192524402",
        institution="Saveetha School of Engineering, SIMATS"
    )

@app.route("/add/<int:a>/<int:b>")
def add(a, b):
    return jsonify(
        operation="addition",
        a=a,
        b=b,
        result=a + b
    )

@app.route("/health")
def health():
    return jsonify(status="healthy", code=200)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
