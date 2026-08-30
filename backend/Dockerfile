# Use an official Python image
FROM python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Force Python stdout/stderr to be unbuffered
ENV PYTHONUNBUFFERED=1

# Use the project's uv-managed virtual environment
ENV PATH="/app/.venv/bin:$PATH"

ENV UV_NO_DEV=1

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files first for better Docker layer caching
COPY pyproject.toml uv.lock* ./

RUN useradd --create-home --shell /bin/bash appuser

# Install project dependencies
RUN uv sync --frozen --no-dev --no-install-project

# Copy the application source
COPY . .

# Install project and fix ownership
RUN uv sync --frozen --no-dev \
    && chown -R appuser:appuser /app

USER appuser

# Expose the FastAPI port
EXPOSE 8000

# Start the FastAPI development server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]