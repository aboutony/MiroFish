# Use Python 3.11 as the stable base for 2026
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies for ChromaDB and Neo4j drivers
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Install 'uv' for high-speed dependency management (as per your lock files)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files first for better caching
COPY pyproject.toml .
COPY uv.lock .

# Install the necessary libraries for our local engine
# Includes: requests (market data), FastAPI (API), ChromaDB (local memory), 
# PyJWT/Argon2 (Security), Neo4j (GraphRAG)
RUN uv pip install --system requests fastapi uvicorn chromadb pyjwt pwdlib[argon2] python-multipart neo4j

# Copy the rest of the application code
COPY . .

# Expose the API port defined in our .env
EXPOSE 5001

# Command to run the Stock Market Predictor Backend
# Points to app.main:app based on your folder structure
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5001"]
