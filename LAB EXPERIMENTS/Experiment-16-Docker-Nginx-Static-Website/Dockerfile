# Use the lightweight official Nginx image
FROM nginx:alpine

# Remove the default Nginx index page
RUN rm -rf /usr/share/nginx/html/*

# Copy website files into the Nginx web root directory
COPY src/index.html src/style.css /usr/share/nginx/html/

# Document that Nginx listens on port 80 inside the container
EXPOSE 80

# Start Nginx in the foreground to keep the container running
CMD ["nginx", "-g", "daemon off;"]
