FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose Flask port
EXPOSE 5000

# Optional: Set environment variable for API
ENV API_URL=http://gpt-sovits-api:9880

CMD ["python", "app.py"]
