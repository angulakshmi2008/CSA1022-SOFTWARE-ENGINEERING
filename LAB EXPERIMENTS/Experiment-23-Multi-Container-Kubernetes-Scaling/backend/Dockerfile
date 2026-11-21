FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

ENV DB_HOST=mysql-service \
    DB_USER=root \
    DB_NAME=college

CMD ["python", "app.py"]
