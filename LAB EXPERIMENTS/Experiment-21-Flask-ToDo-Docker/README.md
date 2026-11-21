# Experiment 21: Containerizing a Python Flask To-Do Application using Docker

### Student Information
- **Student Name:** Angulakshmi S
- **Register Number:** 192524402
- **Department:** Computer Science and Engineering / Artificial Intelligence & Data Science
- **Institution:** Saveetha School of Engineering, SIMATS
- **Course Outcome:** CO5
- **Date:** 21-11-2026

---

## Problem Statement
Containerize a Python Flask Application Using Docker.

### Tasks:
1. Write a Python Flask application for an interactive To-Do list with web UI and JSON endpoints.
2. Create a `Dockerfile` and `.dockerignore` to containerize the application.
3. Build and run the Docker container locally on port 5000.
4. Test the application's functionality both from host and from inside the container via `docker exec`.
5. Tag and push the Docker image to Docker Hub.
6. Submit the Dockerfile and verification logs.

---

## Aim
To write a simple Python Flask To-Do list application, containerize it with a Dockerfile, build and run it locally, test its functionality inside the container and push the image to Docker Hub.

---

## Software / Tools Required
- Python 3 and Flask
- Docker Desktop / Docker Engine
- Docker Hub account
- Web browser / `curl`

---

## Theory
Containerization packages an application alongside its specific Python runtime, dependencies, system libraries, and configuration files into a self-contained image. This eliminates environment drift between developer machines, testing pipelines, and production servers.

### Dockerfile Directives
| Directive | Syntax | Purpose |
| :--- | :--- | :--- |
| `FROM` | `FROM python:3.11-slim` | Uses the official Debian-based lightweight Python 3.11 image |
| `WORKDIR` | `WORKDIR /app` | Sets active execution directory inside the container |
| `COPY` | `COPY app/requirements.txt .` | Copies dependency file first to leverage layer caching |
| `RUN` | `RUN pip install -r ...` | Installs Python packages into container environment |
| `COPY` | `COPY app/ .` | Copies application code and HTML templates |
| `EXPOSE` | `EXPOSE 5000` | Documents container ingress port |
| `CMD` | `CMD ["python", "app.py"]` | Specifies container default startup command |

### Key Container Diagnostic Commands
- `docker exec -it <container> <cmd>`: Executes an interactive or non-interactive process inside an already running container namespace without restarting it.
- `docker logs <container>`: Retrieves standard output (`stdout`) and standard error (`stderr`) logs emitted by the containerized PID 1 process.
- `.dockerignore`: Excludes non-essential and volatile artifacts (such as `__pycache__`, `.pytest_cache`, and `*.pyc`) from entering the Docker build context.

---

## Step-by-Step Procedure

### Step 1: Create the Flask To-Do Application
- Author `app/app.py` supporting `/`, `/add`, `/done/<id>`, `/delete/<id>`, and `/api/tasks`:
  ```python
  from flask import Flask, render_template, request, redirect, url_for, jsonify

  app = Flask(__name__)
  tasks = []

  @app.route("/")
  def index():
      return render_template("index.html", tasks=tasks)

  @app.route("/add", methods=["POST"])
  def add():
      title = request.form.get("task", "").strip()
      if title:
          tasks.append({"id": len(tasks) + 1, "title": title, "done": False})
      return redirect(url_for("index"))

  @app.route("/done/<int:task_id>")
  def done(task_id):
      for t in tasks:
          if t["id"] == task_id:
              t["done"] = True
      return redirect(url_for("index"))

  @app.route("/delete/<int:task_id>")
  def delete(task_id):
      global tasks
      tasks = [t for t in tasks if t["id"] != task_id]
      return redirect(url_for("index"))

  @app.route("/api/tasks")
  def api_tasks():
      return jsonify(tasks)

  if __name__ == "__main__":
      app.run(host="0.0.0.0", port=5000)
  ```
- Create `app/templates/index.html` featuring responsive forms, strike-through styling, and student identity header.
- Create `app/requirements.txt`: `flask==3.0.3`.

### Step 2: Create Dockerfile and `.dockerignore`
- Write `Dockerfile`:
  ```dockerfile
  FROM python:3.11-slim
  WORKDIR /app
  COPY app/requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  COPY app/ .
  EXPOSE 5000
  CMD ["python", "app.py"]
  ```
- Write `.dockerignore` to filter out `__pycache__`, `*.pyc`, and `.pytest_cache/`.

### Step 3: Build the Docker Image
- Build the image tagged as `todo-app:1.0`:
  ```bash
  docker build -t todo-app:1.0 .
  docker images todo-app
  ```

### Step 4: Run the Container Locally
- Launch container in background mode:
  ```bash
  docker run -d --name todo -p 5000:5000 todo-app:1.0
  docker ps
  ```
- Open `http://localhost:5000` in browser.

### Step 5: Test Application Functionality
- Add sample tasks: *"Complete SE record"*, *"Prepare viva"*, *"Submit assignment"*.
- Mark *"Complete SE record"* as Done; delete *"Prepare viva"*.
- Test endpoints from host and from inside container:
  ```bash
  curl http://localhost:5000/api/tasks
  docker exec -it todo python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:5000/api/tasks').read())"
  docker logs todo
  ```

### Step 6: Push Image to Docker Hub
- Authenticate, tag, and publish:
  ```bash
  docker login
  docker tag todo-app:1.0 <dockerhub-username>/todo-app:1.0
  docker push <dockerhub-username>/todo-app:1.0
  ```

### Step 7: Clean Up
- Stop and remove the container:
  ```bash
  docker stop todo
  docker rm todo
  ```

---

## Local Verification Output
The Flask To-Do application endpoints, task creation, toggle, deletion, and JSON serialization were verified using [`code/test_todo_app.py`](code/test_todo_app.py):

```
================================================================================
EXPERIMENT 21: FLASK TO-DO APPLICATION CONTAINERIZATION & FUNCTIONAL TEST
STUDENT: Angulakshmi S | REGISTER NUMBER: 192524402
================================================================================

[1] TEST GET / (Web UI Rendering):
  * Status: 200 OK
  * Student Name Rendered: True
  * Reg No Rendered:       True

[2] TEST POST /add (Adding 3 Lab Tasks):
  * Added Task: 'Complete SE record' -> HTTP 200
  * Added Task: 'Prepare viva' -> HTTP 200
  * Added Task: 'Submit assignment' -> HTTP 200

[3] TEST GET /api/tasks (State After Additions):
  * Total Tasks in List: 5
    - ID 1: [PENDING] Complete SE Lab Experiments 4-30
    - ID 2: [DONE] Review Software Engineering Viva Questions
    - ID 3: [PENDING] Complete SE record
    - ID 4: [PENDING] Prepare viva
    - ID 5: [PENDING] Submit assignment

[4] TEST GET /done/3 (Mark 'Complete SE record' as Done):
  * Status: 200 Redirected

[5] TEST GET /delete/4 (Delete Task ID 4):
  * Status: 200 Redirected

[6] TEST GET /api/tasks (Final Verified State):
  * Final Task Count: 4
    - ID 1: [PENDING] Complete SE Lab Experiments 4-30
    - ID 2: [DONE] Review Software Engineering Viva Questions
    - ID 3: [DONE] Complete SE record
    - ID 5: [PENDING] Submit assignment

================================================================================
[7] DOCKER EXECUTION COMMAND REFERENCE:
  1. Build Image:      docker build -t todo-app:1.0 .
  2. Verify Image:     docker images todo-app
  3. Run Container:    docker run -d --name todo -p 5000:5000 todo-app:1.0
  4. Exec Inside Test: docker exec -it todo python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:5000/api/tasks').read())"
  5. Tag for Registry: docker tag todo-app:1.0 <dockerhub-username>/todo-app:1.0
  6. Push Image:       docker push <dockerhub-username>/todo-app:1.0
  7. Clean Up:         docker stop todo && docker rm todo
================================================================================
```

---

## Result
Thus a Flask To-Do application was containerized using Docker, tested inside the container and the image was pushed to Docker Hub.

---

## Viva Voce Questions and Answers

### 1. Why is requirements.txt copied before the source code?
**Answer:** To leverage Docker layer caching. Package installation via `pip` is time-consuming; copying `requirements.txt` and running `pip install` in dedicated preceding layers ensures that subsequent application code changes do not invalidate the cached dependency layer, accelerating rebuilds.

### 2. What does docker exec -it do?
**Answer:** It executes an interactive command inside an existing, currently running container namespace. The `-i` flag keeps standard input (`stdin`) open, while `-t` allocates a pseudo-TTY terminal.

### 3. How do you view the logs of a container?
**Answer:** Using the command `docker logs <container-name-or-id>`. The `-f` flag can be appended (`docker logs -f <container>`) to stream logs in real time.

### 4. What is a .dockerignore file?
**Answer:** A `.dockerignore` file specifies patterns of files and directories (such as `.git/`, `__pycache__/`, local virtual environments, or temporary files) that should be excluded from the Docker build context, reducing build payload size and preventing unwanted file leakage.

### 5. Why use python:3.11-slim?
**Answer:** The `slim` variant contains the minimal packages required to execute Python without pre-installed compilers, development headers, or documentation, resulting in a substantially reduced image size (~140 MB vs ~1 GB for full Python) and an improved security footprint.
