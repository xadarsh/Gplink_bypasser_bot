FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy all files from the root of your repo to /app in the container
COPY . /app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (ensure these are set on Koyeb as well)
ENV BOT_TOKEN=${BOT_TOKEN}
ENV API_ID=${API_ID}
ENV API_HASH=${API_HASH}

# Run the bot when the container starts (updated to app.py)
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
