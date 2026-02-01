# Use a slim Python image
FROM python:3.9-slim

# Install system dependencies needed for building llama-cpp-python
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    pkg-config \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Upgrade pip and install llama-cpp-python with specific flags to speed up compilation
RUN pip install --upgrade pip

# Install llama-cpp-python with optimizations to reduce build time
ENV CMAKE_ARGS="-DLLAMA_BLAS=OFF -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_EXAMPLES=OFF -DCMAKE_BUILD_TYPE=Release"
RUN pip install --no-cache-dir llama-cpp-python

# Install other requirements
RUN pip install --no-cache-dir fastapi uvicorn[standard]

# Copy the application
COPY app.py .

# Create a script to download the model at startup (since build time might be limited)
RUN echo 'import os
from llama_cpp import Llama

# Download the model at startup
llm = Llama.from_pretrained(
    repo_id="bartowski/Qwen2.5-Coder-0.5B-Instruct-abliterated-GGUF",
    filename="Qwen2.5-Coder-0.5B-Instruct-abliterated-Q3_K_L.gguf",
)
print("Model loaded successfully")
' > preload_model.py

# Expose port (Render expects port 10000 by default)
EXPOSE 10000

# Run the application with uvicorn, using the PORT environment variable
CMD ["sh", "-c", "python preload_model.py && uvicorn app:app --host 0.0.0.0 --port ${PORT:-10000}"]