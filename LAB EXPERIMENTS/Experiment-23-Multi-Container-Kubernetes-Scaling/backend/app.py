import os
from flask import Flask, jsonify

app = Flask(__name__)

# Sample fallback mock dataset when running standalone verification without active MySQL cluster
MOCK_STUDENTS = [
    {"id": 1, "name": "Angulakshmi S", "dept": "CSE - AI & DS", "reg_no": "192524402"},
    {"id": 2, "name": "Priya Sharma", "dept": "Information Technology", "reg_no": "192524403"},
    {"id": 3, "name": "Rahul Kumar", "dept": "Computer Science & Engineering", "reg_no": "192524404"},
    {"id": 4, "name": "Sneha Patel", "dept": "AI & Machine Learning", "reg_no": "192524405"}
]

def db_connect():
    import mysql.connector
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "mysql-service"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", "college123"),
        database=os.environ.get("DB_NAME", "college")
    )

@app.route("/")
def home():
    return jsonify({
        "service": "College Backend API",
        "status": "healthy",
        "institution": "Saveetha School of Engineering, SIMATS",
        "student": "Angulakshmi S",
        "register_number": "192524402"
    })

@app.route("/api/students")
def students():
    try:
        con = db_connect()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT id, name, dept FROM students")
        rows = cur.fetchall()
        con.close()
        return jsonify(rows)
    except Exception as e:
        # Graceful fallback for offline verification testing
        return jsonify({"data": MOCK_STUDENTS, "notice": f"Live DB offline, serving verified mock: {str(e)}"})

@app.route("/health")
def health():
    return jsonify({"status": "UP", "tier": "backend"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
