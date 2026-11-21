"""
Experiment 17: Flask API for Docker & Kubernetes Deployment
Author: Angulakshmi S (Reg No: 192524402)
Department of Computer Science and Engineering
Saveetha School of Engineering, SIMATS
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory student records
students = [
    {"id": 1, "name": "Arun", "dept": "CSE"},
    {"id": 2, "name": "Divya", "dept": "IT"},
    {"id": 3, "name": "Angulakshmi S", "dept": "AI & DS"}
]

@app.route("/")
def home():
    return jsonify({
        "message": "Hello from Flask API on Kubernetes",
        "student": "Angulakshmi S",
        "reg_no": "192524402",
        "course": "CSA10 - Software Engineering",
        "status": "RUNNING",
        "cluster_platform": "Kubernetes Pod"
    })

@app.route("/api/students", methods=["GET"])
def get_students():
    return jsonify({
        "count": len(students),
        "students": students
    })

@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.get_json(force=True, silent=True)
    if not data or "name" not in data or "dept" not in data:
        return jsonify({"error": "Invalid request. 'name' and 'dept' are required."}), 400
    
    new_student = {
        "id": len(students) + 1,
        "name": data["name"],
        "dept": data["dept"]
    }
    students.append(new_student)
    return jsonify({
        "message": "Student added successfully",
        "student": new_student
    }), 201

@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "service": "flask-api-service",
        "version": "1.0"
    })

if __name__ == "__main__":
    # Must listen on 0.0.0.0 to accept traffic forwarded into container
    app.run(host="0.0.0.0", port=5000, debug=False)
