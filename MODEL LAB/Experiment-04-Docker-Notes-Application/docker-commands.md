# Docker Commands, Verification & Docker Hub Guide

## 1. Local Environment Status Note

> **ENVIRONMENT STATUS:** The Node.js Express Notes application was successfully verified locally using native Node.js (`test_api.js`: 16/16 test assertions passed).  
> In the current host environment, Docker CLI is not installed or added to PATH (`The term 'docker' is not recognized`).  
> All configuration files (`Dockerfile`, `.dockerignore`, `docker-compose.yml`) are fully constructed and follow official Docker/Node.js production specifications. When you launch Docker Desktop on your machine, execute the commands below.

---

## 2. Docker Container Lifecycle Commands

### Step 1: Build the Docker Image Locally
Navigate to the `Q4_Docker_Notes_Application` directory and build the container image:
```bash
cd Q4_Docker_Notes_Application
docker build -t notes-app:1.0.0 .
```
- `-t notes-app:1.0.0` tags the built image with name `notes-app` and version `1.0.0`.
- `.` sets the current directory as the build context.

### Step 2: Verify the Image Was Created
```bash
docker images
```
*Expected Output:*
```text
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
notes-app    1.0.0     a1b2c3d4e5f6   10 seconds ago   135MB
```

### Step 3: Run the Container
Run the container in detached mode with port forwarding:
```bash
docker run -d -p 3000:3000 --name notes-container notes-app:1.0.0
```
- `-d`: Run container in background (detached).
- `-p 3000:3000`: Map host port 3000 to container port 3000.
- `--name notes-container`: Assign a human-readable name.

### Step 4: Verify Container Status
```bash
docker ps
```
*Expected Output:*
```text
CONTAINER ID   IMAGE             COMMAND                  STATUS         PORTS                    NAMES
8f9e0d1c2b3a   notes-app:1.0.0   "docker-entrypoint.s…"   Up 5 seconds   0.0.0.0:3000->3000/tcp   notes-container
```

### Step 5: Check Container Startup Logs
```bash
docker logs notes-container
```
*Expected Output:*
```text
====================================================
 Notes Express API listening on http://0.0.0.0:3000
 Ready for HTTP client & Docker container requests
====================================================
```

---

## 3. Testing the Application

### A. Testing from Outside the Container (Host Machine via curl or browser)

1. **Test Health Endpoint:**
   ```bash
   curl http://localhost:3000/
   ```
   *Expected Response:*
   ```json
   {
     "status": "UP",
     "application": "Notes REST API",
     "version": "1.0.0",
     "message": "Server is healthy and ready to handle requests.",
     "containerEnvironment": "Docker Container"
   }
   ```

2. **List All Notes:**
   ```bash
   curl http://localhost:3000/notes
   ```

3. **Add a New Note (POST Valid):**
   ```bash
   curl -X POST http://localhost:3000/notes \
     -H "Content-Type: application/json" \
     -d "{\"title\":\"Docker Notes\",\"content\":\"Application is successfully containerized with Alpine Linux.\"}"
   ```
   *Expected Response (HTTP 201 Created):*
   ```json
   {
     "message": "Note added successfully.",
     "note": {
       "id": 3,
       "title": "Docker Notes",
       "content": "Application is successfully containerized with Alpine Linux.",
       "createdAt": "2026-11-22T14:30:00.000Z"
     }
   }
   ```

4. **Test POST Validation (Invalid Empty Note):**
   ```bash
   curl -X POST http://localhost:3000/notes \
     -H "Content-Type: application/json" \
     -d "{\"title\":\"Bad Note\",\"content\":\"\"}"
   ```
   *Expected Response (HTTP 400 Bad Request):*
   ```json
   {
     "error": "Bad Request",
     "message": "Note content is required and cannot be empty."
   }
   ```

---

### B. Testing Inside the Container (`docker exec`)

To test the application from within the container's isolated network:
```bash
# Open interactive shell inside the container
docker exec -it notes-container sh

# Inside the Alpine Linux container shell:
wget -qO- http://localhost:3000/notes

# Exit container shell
exit
```

---

## 4. Container Cleanup Commands

```bash
# Stop the running container
docker stop notes-container

# Remove the container instance
docker rm notes-container

# (Optional) Remove the image
docker rmi notes-app:1.0.0
```

---

## 5. Docker Hub Preparation & Instructions

> **IMPORTANT:** In strict compliance with instructions, **NO image was pushed to Docker Hub** during this lab session. Follow the steps below when you are ready to publish.

### Step 1: Log in to Docker Hub
```bash
docker login
# Enter your Docker Hub username and password/token when prompted
```

### Step 2: Tag the Image with Your Docker Hub Username
```bash
docker tag notes-app:1.0.0 <your-dockerhub-username>/notes-app:1.0.0
docker tag notes-app:1.0.0 <your-dockerhub-username>/notes-app:latest
```

### Step 3: Push the Image to Docker Hub
```bash
docker push <your-dockerhub-username>/notes-app:1.0.0
docker push <your-dockerhub-username>/notes-app:latest
```

### Step 4: Verify on Docker Hub
Open your browser and navigate to:
`https://hub.docker.com/r/<your-dockerhub-username>/notes-app`
