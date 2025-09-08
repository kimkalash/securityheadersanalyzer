# 1. Base image
FROM python:3.12-slim

# 2. Set working directory inside the container
WORKDIR /app

# 3. Install system dependencies (needed for psycopg2 and others)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements first (to leverage Docker cache)
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the app code
COPY . .

# 7. Expose FastAPI port
EXPOSE 8000

# 8. Start FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
