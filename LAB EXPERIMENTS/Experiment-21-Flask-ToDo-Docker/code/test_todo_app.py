"""
Experiment 21: Flask To-Do Application Verification Script
Author: Angulakshmi S (Reg No: 192524402)
Department of Computer Science and Engineering
Saveetha School of Engineering, SIMATS
"""

import os
import sys
import json
import time
import threading
import urllib.request
import urllib.parse

base_dir = os.path.dirname(os.path.abspath(__file__))
exp_dir = os.path.abspath(os.path.join(base_dir, ".."))
app_dir = os.path.join(exp_dir, "app")
out_dir = os.path.join(exp_dir, "output")
os.makedirs(out_dir, exist_ok=True)

sys.path.insert(0, app_dir)
from app import app
from werkzeug.serving import make_server

class ServerThread(threading.Thread):
    def __init__(self, app, port=5003):
        super().__init__()
        self.server = make_server('127.0.0.1', port, app)
        self.ctx = app.app_context()
        self.ctx.push()
        self.daemon = True

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

def test_todo():
    print("=" * 80)
    print("EXPERIMENT 21: FLASK TO-DO APPLICATION CONTAINERIZATION & FUNCTIONAL TEST")
    print("STUDENT: Angulakshmi S | REGISTER NUMBER: 192524402")
    print("=" * 80)

    port = 5003
    server = ServerThread(app, port=port)
    server.start()
    time.sleep(1)

    base_url = f"http://127.0.0.1:{port}"

    try:
        # 1. Test GET / (HTML Rendering)
        print("\n[1] TEST GET / (Web UI Rendering):")
        with urllib.request.urlopen(f"{base_url}/") as res:
            html = res.read().decode("utf-8")
            print(f"  * Status: {res.getcode()} OK")
            print(f"  * Student Name Rendered: {'Angulakshmi S' in html}")
            print(f"  * Reg No Rendered:       {'192524402' in html}")

        # 2. Add tasks matching lab manual
        print("\n[2] TEST POST /add (Adding 3 Lab Tasks):")
        sample_tasks = ["Complete SE record", "Prepare viva", "Submit assignment"]
        for t in sample_tasks:
            data = urllib.parse.urlencode({"task": t}).encode("utf-8")
            req = urllib.request.Request(f"{base_url}/add", data=data, method="POST")
            with urllib.request.urlopen(req) as res:
                print(f"  * Added Task: '{t}' -> HTTP {res.getcode()}")

        # 3. Query API before modifications
        print("\n[3] TEST GET /api/tasks (State After Additions):")
        with urllib.request.urlopen(f"{base_url}/api/tasks") as res:
            api_data = json.loads(res.read().decode("utf-8"))
            print(f"  * Total Tasks in List: {api_data['count']}")
            for item in api_data["tasks"]:
                status_str = "[DONE]" if item["done"] else "[PENDING]"
                print(f"    - ID {item['id']}: {status_str} {item['title']}")

        # 4. Mark Task ID 3 as Done
        print("\n[4] TEST GET /done/3 (Mark 'Complete SE record' as Done):")
        with urllib.request.urlopen(f"{base_url}/done/3") as res:
            print(f"  * Status: {res.getcode()} Redirected")

        # 5. Delete Task ID 4 ('Prepare viva')
        print("\n[5] TEST GET /delete/4 (Delete Task ID 4):")
        with urllib.request.urlopen(f"{base_url}/delete/4") as res:
            print(f"  * Status: {res.getcode()} Redirected")

        # 6. Verify final state via API
        print("\n[6] TEST GET /api/tasks (Final Verified State):")
        with urllib.request.urlopen(f"{base_url}/api/tasks") as res:
            final_data = json.loads(res.read().decode("utf-8"))
            print(f"  * Final Task Count: {final_data['count']}")
            for item in final_data["tasks"]:
                status_str = "[DONE]" if item["done"] else "[PENDING]"
                print(f"    - ID {item['id']}: {status_str} {item['title']}")

    finally:
        server.shutdown()

    print("\n" + "=" * 80)
    print("[7] DOCKER EXECUTION COMMAND REFERENCE:")
    print("  1. Build Image:      docker build -t todo-app:1.0 .")
    print("  2. Verify Image:     docker images todo-app")
    print("  3. Run Container:    docker run -d --name todo -p 5000:5000 todo-app:1.0")
    print("  4. Exec Inside Test: docker exec -it todo python -c \"import urllib.request; print(urllib.request.urlopen('http://localhost:5000/api/tasks').read())\"")
    print("  5. Tag for Registry: docker tag todo-app:1.0 <dockerhub-username>/todo-app:1.0")
    print("  6. Push Image:       docker push <dockerhub-username>/todo-app:1.0")
    print("  7. Clean Up:         docker stop todo && docker rm todo")
    print("=" * 80)

if __name__ == "__main__":
    report_file = os.path.join(out_dir, "run_output.txt")
    orig_stdout = sys.stdout
    with open(report_file, "w", encoding="utf-8") as f:
        sys.stdout = f
        test_todo()
    sys.stdout = orig_stdout
    test_todo()
    print(f"\n[+] Real run log saved to: {report_file}")
