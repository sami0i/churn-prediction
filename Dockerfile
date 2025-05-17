# Use a stable base with build tools and shared libraries
FROM python:3.10-slim

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies and clean up to reduce image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Upgrade pip and install wheel to speed up Python builds
RUN pip install --upgrade pip wheel

# Copy requirements early to leverage Docker caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy full project code
COPY . .

# Set environment variable to avoid hardcoding in scripts
ENV PYTHONPATH=/app/src

# Default command runs training mode
CMD ["python", "main.py", "--mode=train"]
