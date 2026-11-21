FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Set default application port
ENV PORT=5000
EXPOSE 5000

# Execute with production WSGI server
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
