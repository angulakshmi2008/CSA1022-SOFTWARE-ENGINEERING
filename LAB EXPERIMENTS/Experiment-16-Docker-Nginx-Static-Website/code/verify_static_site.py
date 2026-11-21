"""
Experiment 16: Static Website Verification Script
Author: Angulakshmi S (Reg No: 192524402)
Department of Computer Science and Engineering
Saveetha School of Engineering, SIMATS
"""

import os
import sys
import threading
import time
import urllib.request
from http.server import SimpleHTTPRequestHandler, HTTPServer

def run_verification():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.abspath(os.path.join(base_dir, ".."))
    src_dir = os.path.join(exp_dir, "src")
    out_dir = os.path.join(exp_dir, "output")
    os.makedirs(out_dir, exist_ok=True)

    print("=" * 80)
    print("EXPERIMENT 16: STATIC WEBSITE AND NGINX CONTAINERIZATION VERIFICATION")
    print("STUDENT: Angulakshmi S | REGISTER NUMBER: 192524402")
    print("=" * 80)

    # 1. Verify files exist
    html_file = os.path.join(src_dir, "index.html")
    css_file = os.path.join(src_dir, "style.css")
    docker_file = os.path.join(exp_dir, "Dockerfile")

    print(f"\n[1] VERIFYING STATIC ARTEFACTS:")
    print(f"  * index.html exists: {os.path.exists(html_file)} ({os.path.getsize(html_file)} bytes)")
    print(f"  * style.css exists:  {os.path.exists(css_file)} ({os.path.getsize(css_file)} bytes)")
    print(f"  * Dockerfile exists: {os.path.exists(docker_file)} ({os.path.getsize(docker_file)} bytes)")

    # 2. Inspect Dockerfile instructions
    print(f"\n[2] DOCKERFILE CONFIGURATION:")
    with open(docker_file, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if line_str and not line_str.startswith("#"):
                print(f"  -> {line_str}")

    # 3. Spin up local HTTP server to test serving assets on port 8080
    port = 8080
    class CustomHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=src_dir, **kwargs)
        def log_message(self, format, *args):
            pass # Suppress noisy server log

    server = None
    actual_port = port
    for test_port in [8080, 8081, 8082, 8888]:
        try:
            server = HTTPServer(("127.0.0.1", test_port), CustomHandler)
            actual_port = test_port
            break
        except OSError:
            continue

    if not server:
        print("[!] Could not bind to local port for test server.")
        return

    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.5)

    test_url = f"http://127.0.0.1:{actual_port}/index.html"
    print(f"\n[3] TESTING LOCAL ASSET SERVING AT: {test_url}")
    try:
        req = urllib.request.Request(test_url, headers={"User-Agent": "DockerNginxTest/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            status_code = response.getcode()
            content_type = response.headers.get("Content-Type")
            body = response.read().decode("utf-8")

        print(f"  * HTTP Response Status: {status_code} OK")
        print(f"  * Content-Type:         {content_type}")
        print(f"  * Body Size:             {len(body)} characters")
        print(f"  * Verified Title:        'My Static Website - Docker & Nginx' present: {'My Static Website' in body}")
        print(f"  * Verified Student Name: 'Angulakshmi S' present: {'Angulakshmi S' in body}")
        print(f"  * Verified Reg Number:   '192524402' present: {'192524402' in body}")

        # Save downloaded HTML
        curl_file = os.path.join(out_dir, "curl_response.html")
        with open(curl_file, "w", encoding="utf-8") as f:
            f.write(body)
        print(f"  * Saved response to:    {curl_file}")

    except Exception as e:
        print(f"[!] Request error: {e}")
    finally:
        server.shutdown()
        server.server_close()

    print("\n" + "=" * 80)
    print("[4] DOCKER EXECUTION COMMAND REFERENCE:")
    print("  1. Build Image:     docker build -t static-site:1.0 .")
    print("  2. Verify Image:    docker images static-site")
    print("  3. Run Container:   docker run -d --name mysite -p 8080:80 static-site:1.0")
    print("  4. Inspect Status:  docker ps")
    print("  5. Verify HTTP:     curl http://localhost:8080")
    print("  6. Clean Up:        docker stop mysite && docker rm mysite")
    print("=" * 80)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.abspath(os.path.join(base_dir, "..", "output"))
    os.makedirs(out_dir, exist_ok=True)
    report_file = os.path.join(out_dir, "run_output.txt")
    
    orig_stdout = sys.stdout
    with open(report_file, "w", encoding="utf-8") as f:
        sys.stdout = f
        run_verification()
    sys.stdout = orig_stdout
    run_verification()
    print(f"\n[+] Real run log saved to: {report_file}")
