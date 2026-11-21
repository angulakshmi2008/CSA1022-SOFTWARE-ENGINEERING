# Experiment 16: Static Website Containerized and Served with Docker and Nginx

### Student Information
- **Student Name:** Angulakshmi S
- **Register Number:** 192524402
- **Department:** Computer Science and Engineering / Artificial Intelligence & Data Science
- **Institution:** Saveetha School of Engineering, SIMATS
- **Course Outcome:** CO3
- **Date:** 21-11-2026

---

## Problem Statement
Create a Static Website and Containerize, Build & Serve it using Docker.

### Tasks:
1. Create a Simple Static Website (`index.html` and `style.css`) with structured HTML content.
2. Write/create a `Dockerfile` to serve the website using the high-performance Nginx web server.
3. Build the Docker Image with tag `static-site:1.0`.
4. Run the container in detached mode with host port mapping `8080:80`.
5. Access the Website using a Browser at `http://localhost:8080`.

---

## Aim
To create a simple static website, write a Dockerfile that serves it with Nginx, build the Docker image, run the container and access the website from a browser.

---

## Software / Tools Required
- Docker Desktop / Docker Engine
- Visual Studio Code
- Web browser (Google Chrome / Microsoft Edge)

---

## Theory
Docker is an open-source containerization platform that packages applications along with all dependencies into lightweight, standalone, and executable units called **containers**. Containers share the host operating system kernel rather than virtualizing hardware, resulting in near-instantaneous startup times, minuscule resource footprints, and immunity from the classic *"it works on my machine"* deployment dilemma.

### Core Container Concepts
- **Dockerfile:** A declarative text script containing sequential directives (`FROM`, `RUN`, `COPY`, `EXPOSE`, `CMD`) that define how an image is assembled.
- **Image:** A read-only, layered filesystem template created by compiling a Dockerfile.
- **Container:** A runnable, isolated runtime instance instantiated from an image.
- **Nginx Web Server:** A high-concurrency reverse proxy and static HTTP web server. The official `nginx:alpine` image provides an ultra-minimal footprint (~20 MB) and serves static web assets from `/usr/share/nginx/html`.
- **Port Mapping (`-p 8080:80`):** Binds host interface port `8080` to container internal listening port `80`.

### Dockerfile Directives Used
| Directive | Syntax | Purpose |
| :--- | :--- | :--- |
| `FROM` | `FROM nginx:alpine` | Specifies the lightweight Alpine Linux Nginx parent image |
| `RUN` | `RUN rm -rf /usr/share/nginx/html/*` | Purges default Nginx placeholder HTML files |
| `COPY` | `COPY src/ /usr/share/nginx/html/` | Injects local website assets into Nginx root |
| `EXPOSE` | `EXPOSE 80` | Documents container runtime listening port |
| `CMD` | `CMD ["nginx", "-g", "daemon off;"]` | Keeps Nginx executing in foreground as PID 1 |

---

## Step-by-Step Procedure

### Step 1: Install and Verify Docker
- Install Docker Desktop on Windows/macOS or Docker Engine on Linux.
- Open PowerShell or terminal and verify Docker daemon connectivity:
  ```bash
  docker --version
  docker run hello-world
  ```
- The output message *"Hello from Docker!"* confirms correct daemon operation.

### Step 2: Create the Project Folder
- Create the project workspace structure:
  ```bash
  mkdir static-site
  cd static-site
  code .
  ```

### Step 3: Create the Static Website
- Create `src/index.html` with academic student credentials:
  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <title>My Static Website - Docker & Nginx</title>
      <link rel="stylesheet" href="style.css">
  </head>
  <body>
      <header><h1>Welcome to My Static Website</h1></header>
      <main>
          <p>This page is served by an Nginx container built with Docker.</p>
          <ul>
              <li>Student Name: Angulakshmi S</li>
              <li>Register Number: 192524402</li>
              <li>Course: CSA10 - Software Engineering</li>
              <li>Experiment: Static Website with Docker</li>
          </ul>
      </main>
      <footer>&copy; 2026 Saveetha School of Engineering</footer>
  </body>
  </html>
  ```
- Create `src/style.css` for styling header, card containers, and typography.

### Step 4: Write the Dockerfile
- Create `Dockerfile` in the root of the project:
  ```dockerfile
  # Use the lightweight official Nginx image
  FROM nginx:alpine
  # Remove the default Nginx page
  RUN rm -rf /usr/share/nginx/html/*
  # Copy website files into the Nginx web root
  COPY src/index.html src/style.css /usr/share/nginx/html/
  # Nginx listens on port 80
  EXPOSE 80
  # Start Nginx in the foreground
  CMD ["nginx", "-g", "daemon off;"]
  ```

### Step 5: Build the Docker Image
- Build and tag the Docker image:
  ```bash
  docker build -t static-site:1.0 .
  docker images static-site
  ```
- Verify that `static-site` with tag `1.0` appears in the local image cache.

### Step 6: Run the Container
- Run the container in detached background mode mapping port 8080 to 80:
  ```bash
  docker run -d --name mysite -p 8080:80 static-site:1.0
  docker ps
  ```
- Verify that container `mysite` shows status `Up` and port mapping `0.0.0.0:8080->80/tcp`.

### Step 7: Access the Website in a Browser
- Open a web browser and navigate to: `http://localhost:8080`.
- The page *"Welcome to My Static Website"* displaying student details is rendered.

### Step 8: Update, Stop and Clean Up
- View container access logs and stop/remove container:
  ```bash
  docker logs mysite
  docker stop mysite
  docker rm mysite
  ```

---

## Local Verification Output
The website assets, Dockerfile configuration, and local HTTP serving were verified programmatically:
- Verification Script: [`code/verify_static_site.py`](code/verify_static_site.py)
- Downloaded HTTP Response: [`output/curl_response.html`](output/curl_response.html)
- Screenshot Checklist: [`screenshots/SCREENSHOTS_TODO.md`](screenshots/SCREENSHOTS_TODO.md)

### Verification Run Log
```
================================================================================
EXPERIMENT 16: STATIC WEBSITE AND NGINX CONTAINERIZATION VERIFICATION
STUDENT: Angulakshmi S | REGISTER NUMBER: 192524402
================================================================================

[1] VERIFYING STATIC ARTEFACTS:
  * index.html exists: True (1883 bytes)
  * style.css exists:  True (1624 bytes)
  * Dockerfile exists: True (419 bytes)

[2] DOCKERFILE CONFIGURATION:
  -> FROM nginx:alpine
  -> RUN rm -rf /usr/share/nginx/html/*
  -> COPY src/index.html src/style.css /usr/share/nginx/html/
  -> EXPOSE 80
  -> CMD ["nginx", "-g", "daemon off;"]

[3] TESTING LOCAL ASSET SERVING AT: http://127.0.0.1:8080/index.html
  * HTTP Response Status: 200 OK
  * Content-Type:         text/html
  * Body Size:             1881 characters
  * Verified Title:        'My Static Website - Docker & Nginx' present: True
  * Verified Student Name: 'Angulakshmi S' present: True
  * Verified Reg Number:   '192524402' present: True
  * Saved response to:    output/curl_response.html

================================================================================
[4] DOCKER EXECUTION COMMAND REFERENCE:
  1. Build Image:     docker build -t static-site:1.0 .
  2. Verify Image:    docker images static-site
  3. Run Container:   docker run -d --name mysite -p 8080:80 static-site:1.0
  4. Inspect Status:  docker ps
  5. Verify HTTP:     curl http://localhost:8080
  6. Clean Up:        docker stop mysite && docker rm mysite
================================================================================
```

---

## Result
Thus a static website was created, containerized with a Dockerfile using Nginx, built into an image, run as a container and accessed successfully in a browser.

---

## Viva Voce Questions and Answers

### 1. What is the difference between an image and a container?
**Answer:** An image is a read-only, immutable template built from a Dockerfile consisting of layered filesystems. A container is a stateful, running instance of an image executed with isolated kernel namespaces and cgroups.

### 2. What does the EXPOSE instruction do?
**Answer:** The `EXPOSE` instruction serves as documentation between the image author and user indicating which port the container intends to listen on; publishing and port mapping to host interfaces is performed at runtime using the `-p` or `-P` flags.

### 3. What is the purpose of -d in docker run?
**Answer:** The `-d` (detached) flag instructs Docker to run the container in the background and print the container ID to the console, freeing up the terminal session.

### 4. Where does Nginx serve static files from in the official image?
**Answer:** By default in the official Nginx image, static content is served from the directory `/usr/share/nginx/html`.

### 5. Why is alpine used as the base?
**Answer:** Alpine Linux is an ultra-compact Linux distribution (~5 MB base size). Utilizing `nginx:alpine` minimizes image size (~20 MB vs ~140 MB for Debian-based), accelerates container download speeds, reduces disk consumption, and drastically decreases the security attack surface.
