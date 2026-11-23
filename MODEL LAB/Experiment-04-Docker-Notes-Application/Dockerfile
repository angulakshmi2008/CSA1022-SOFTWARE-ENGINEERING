# ==============================================================================
# Dockerfile: Production-Ready Containerization for Node.js Express Notes App
# Base Image: Lightweight Node.js 20 on Alpine Linux
# ==============================================================================

# 1. Base Image: Use official Node.js Alpine image for minimal attack surface and size (~130MB)
FROM node:20-alpine

# 2. Set Environment Variables
ENV NODE_ENV=production \
    PORT=3000 \
    IS_DOCKER=true

# 3. Working Directory: Set root directory inside the container
WORKDIR /app

# 4. Dependency Layer Caching: Copy package manifests first
# This ensures that docker build reuses cached dependency layers if package.json hasn't changed.
COPY package*.json ./

# 5. Install production-only dependencies
RUN npm ci --only=production || npm install --production

# 6. Copy Application Source Code
COPY . .

# 7. Expose Port: Informs Docker that the container listens on port 3000 at runtime
EXPOSE 3000

# 8. Security: Run container as non-root user 'node' provided by official base image
USER node

# 9. Startup Command: Execute the Express server
CMD ["node", "server.js"]
