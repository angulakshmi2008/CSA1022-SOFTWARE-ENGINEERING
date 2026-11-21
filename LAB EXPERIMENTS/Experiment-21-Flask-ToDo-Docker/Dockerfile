# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set container working directory
WORKDIR /app

# Copy dependency definition first for layer caching
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and templates
COPY app/ .

# Document listening port
EXPOSE 5000

# Start Flask application
CMD ["python", "app.py"]
