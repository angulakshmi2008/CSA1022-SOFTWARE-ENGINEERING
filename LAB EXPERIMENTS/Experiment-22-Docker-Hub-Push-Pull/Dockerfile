FROM nginx:alpine

# Copy static website assets to default Nginx html serving directory
COPY src/index.html /usr/share/nginx/html/index.html

# Expose HTTP port
EXPOSE 80

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
