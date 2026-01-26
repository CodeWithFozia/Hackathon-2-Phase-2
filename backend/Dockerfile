# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 7860 (Hugging Face Spaces default)
EXPOSE 7860

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV API_HOST=0.0.0.0
ENV API_PORT=7860

# Run the application
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]
