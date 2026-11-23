# Part B — Analysis: Dockerfile Instructions, Build Context, Container Verification & Ephemeral Storage

**Course:** Software Engineering (CSA10)  
**Question:** Q4 Part B (10 Marks)  
**Topic:** Line-by-Line Dockerfile Analysis, .dockerignore Role, In-Container Testing & Container Storage Lifecycles  

---

## Question:
> *"Explain each instruction in your Dockerfile and why a .dockerignore file is used. State how you verified the application inside the container and what happens to the notes when the container is removed."*

---

## 1. Line-by-Line Explanation of the Dockerfile Instructions

Our Dockerfile was written following industry containerization best practices (minimal image size, layer caching, non-root security):

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY . .
EXPOSE 3000
USER node
CMD ["node", "server.js"]
```

| Dockerfile Instruction | Technical Purpose & Best Practice Rationale |
| :--- | :--- |
| **`FROM node:20-alpine`** | Sets the parent base image. Using **Alpine Linux** reduces image size from ~1.1 GB (standard Debian Node) down to ~130 MB, minimizing storage, speeding up build/pull times, and drastically reducing the attack surface. |
| **`WORKDIR /app`** | Sets the default execution directory inside the container. If `/app` does not exist, Docker creates it automatically. All subsequent instructions (`COPY`, `RUN`, `CMD`) run inside this path. |
| **`COPY package*.json ./`** | Copies `package.json` and `package-lock.json` into `/app` **before** copying application code. This enables **Docker Layer Caching**: as long as dependencies have not changed, Docker reuses the cached `node_modules` layer during rebuilds, avoiding redundant downloads. |
| **`RUN npm install --production`** | Executes the package installation inside the container during image build time. The `--production` flag ensures development dependencies are omitted, keeping the image lean. |
| **`COPY . .`** | Copies the application source files (`server.js`, etc.) from the host project into the container's `/app` directory. |
| **`EXPOSE 3000`** | Serves as documentation informing Docker and operators that the container process listens on network port 3000. (Note: port binding on the host still requires `-p 3000:3000` during `docker run`). |
| **`USER node`** | Security hardening. By default, Docker containers run as `root`. Dropping root privileges to the built-in unprivileged `node` user prevents potential container breakout vulnerabilities. |
| **`CMD ["node", "server.js"]`** | Specifies the default command executed when the container starts. Unlike `RUN` (which runs at image build time), `CMD` executes at container runtime. |

---

## 2. Why a `.dockerignore` File is Used

When `docker build` executes, the Docker CLI bundles the current directory into a tarball called the **Build Context** and sends it over to the Docker daemon.

The `.dockerignore` file defines exclusion rules for files and folders that must **never** be sent to the build daemon.

### Critical Reasons for `.dockerignore`:
1. **Preventing Host OS Binary Pollution (`node_modules`):**  
   If the developer has `node_modules` installed on a Windows or macOS host, copying them into an Alpine Linux container can cause crashes due to incompatible native C++ binary addons. `.dockerignore` forces `npm install` to compile fresh, Linux-compatible binaries inside the container.
2. **Build Speed and Network Performance:**  
   `node_modules` and `.git` folders contain tens of thousands of tiny files. Excluding them reduces the build context size from hundreds of megabytes to a few kilobytes, accelerating build times.
3. **Security and Secret Leakage Prevention:**  
   Files such as `.env`, private SSH keys, test tokens, and local development logs are prevented from being accidentally baked into the public container image.
4. **Cache Invalidation Avoidance:**  
   Changes to local log files, test scripts, or git commits will not trigger cache invalidation for Docker's build layers.

---

## 3. How to Verify the Application Inside the Container

Verification of a containerized application is conducted across two dimensions:

### A. Host-to-Container Verification (Outside the Container)
1. **Container State Inspection:**  
   Run `docker ps` to verify that the container status is `Up` and port `3000->3000/tcp` is actively forwarded.
2. **Container Runtime Logs:**  
   Run `docker logs notes-container` to confirm that Node.js initialized and output:
   `"Notes Express API listening on http://0.0.0.0:3000"`.
3. **HTTP Endpoint Probing:**  
   Send HTTP requests to the exposed host port:
   - `curl http://localhost:3000/` $\rightarrow$ Checks health (HTTP 200).
   - `curl http://localhost:3000/notes` $\rightarrow$ Checks array retrieval.
   - `curl -X POST http://localhost:3000/notes ...` $\rightarrow$ Tests creation and validation.

### B. In-Container Direct Verification (Inside the Container Shell)
To inspect the environment directly from within the container's isolated network namespace:
1. Open an interactive shell inside the running container:
   ```bash
   docker exec -it notes-container sh
   ```
2. Verify processes running inside container:
   ```sh
   ps aux
   # Displays node server.js running under UID node (non-root)
   ```
3. Test internal network loopback connectivity using `wget`:
   ```sh
   wget -qO- http://localhost:3000/notes
   ```
   This returns the JSON notes list directly from the container's internal localhost, verifying that the Express socket is listening on `0.0.0.0`.

---

## 4. What Happens to Notes When the Container is Removed?

### A. The Ephemeral Nature of Container In-Memory Storage
In our application, notes are stored in an in-memory JavaScript array (`let notes = [...]`).
- In Docker's architecture, each container instance consists of read-only image layers plus a temporary, thin **writable container layer** and RAM allocated by the host OS.
- **When the container is stopped (`docker stop`):** The process pauses, but the writable layer persists on disk.
- **When the container is removed (`docker rm`):** The entire writable layer and RAM allocation are **permanently destroyed**. All notes created during runtime are **irrecoverably lost**. The next container spun up from the same image will reset back to the initial hardcoded notes.

### B. How Persistent Storage is Implemented in Production
To guarantee data durability across container restarts, upgrades, and removals, software engineers use **Docker Persistent Storage**:
1. **Docker Named Volumes:**
   ```bash
   docker volume create notes-storage
   docker run -d -p 3000:3000 -v notes-storage:/app/data --name notes-api notes-app:1.0.0
   ```
   Data written to `/app/data` is stored directly on the host file system managed by Docker, completely independent of the container lifecycle.
2. **External Database Containers / Managed Services:**
   In production architectures, state is decoupled from compute by connecting the Express application via environment variables (`DATABASE_URL`) to an external persistent database (such as MongoDB, PostgreSQL, or Redis).

---

## 5. Key Summary for Lab Viva

| Topic | Key Viva Takeaway |
| :--- | :--- |
| **`FROM node:20-alpine`** | Ultra-lightweight Linux distribution (~130 MB); highly secure and fast. |
| **Layer Caching** | Copying `package*.json` before source code prevents re-running `npm install` on every small code change. |
| **`.dockerignore`** | Prevents host `node_modules` and secret files from polluting the container build context. |
| **`USER node`** | Adheres to least privilege; avoids running the web process as `root`. |
| **In-Container Test** | `docker exec -it <id> sh` followed by `wget -qO- http://localhost:3000/notes`. |
| **Storage Lifecycle** | In-memory notes are **ephemeral** and deleted when the container is removed; **Named Volumes** or external databases are required for persistence. |
