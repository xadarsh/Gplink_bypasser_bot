FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot.py script into the container
COPY app.py .

# Set environment variables (you can set these on Koyeb as well)
ENV BOT_TOKEN=${BOT_TOKEN}
ENV API_ID=${API_ID}
ENV API_HASH=${API_HASH}

# Run the bot when the container starts
CMD ["python", "bot.py"]
