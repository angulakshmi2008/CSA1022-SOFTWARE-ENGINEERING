# Use official minimal Python runtime
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency requirements
COPY app/requirements.txt .

# Install dependencies without caching to keep image lightweight
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app/app.py .

# Expose internal application port
EXPOSE 5000

# Launch application listening on 0.0.0.0
CMD ["python", "app.py"]
