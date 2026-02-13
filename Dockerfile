# Multi-stage Dockerfile for Moonrise
# Optimized for Azure Container Apps with Scale to Zero

# Stage 1: Builder
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Pre-download Skyfield ephemeris to reduce cold start time
RUN python -c "from skyfield.api import load; load('de421.bsp')"

# Stage 2: Runtime
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /root/.skyfield /root/.skyfield

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY app/ ./app/
COPY config.py .
COPY run.py .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEPLOYMENT_PLATFORM=azure
ENV PORT=8080

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')" || exit 1

# Run with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "run:app"]
