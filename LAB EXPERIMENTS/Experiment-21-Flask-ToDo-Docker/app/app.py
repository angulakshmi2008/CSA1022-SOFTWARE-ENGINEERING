"""
Experiment 21: Containerizing a Python Flask To-Do Application using Docker
Author: Angulakshmi S (Reg No: 192524402)
Department of Computer Science and Engineering
Saveetha School of Engineering, SIMATS
"""

import os
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# In-memory storage for tasks
tasks = [
    {"id": 1, "title": "Complete SE Lab Experiments 4-30", "done": False},
    {"id": 2, "title": "Review Software Engineering Viva Questions", "done": True}
]

@app.route("/")
def index():
    return render_template(
        "index.html", 
        tasks=tasks, 
        student_name="Angulakshmi S", 
        reg_no="192524402"
    )

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("task", "").strip()
    if title:
        new_id = max([t["id"] for t in tasks], default=0) + 1
        tasks.append({"id": new_id, "title": title, "done": False})
    return redirect(url_for("index"))

@app.route("/done/<int:task_id>")
def done(task_id):
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            break
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for("index"))

@app.route("/api/tasks", methods=["GET"])
def api_tasks():
    return jsonify({
        "student": "Angulakshmi S",
        "reg_no": "192524402",
        "count": len(tasks),
        "tasks": tasks
    })

if __name__ == "__main__":
    # 0.0.0.0 binds to all network interfaces for container ingress
    app.run(host="0.0.0.0", port=5000, debug=False)
