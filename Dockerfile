FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies including ntpdate for time sync
RUN apt-get update && \
    apt-get install -y --no-install-recommends ntpdate gcc libffi-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# Sync time to fix Pyrogram msg_id issue
RUN ntpdate -u pool.ntp.org

# Optional: install TgCrypto for performance
RUN pip install --no-cache-dir tgcrypto

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . /app/

# Run the bot
CMD ["sh", "-c", "ntpdate -u pool.ntp.org && python app.py"]
