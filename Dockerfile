# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set environment variables for the application
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt first to install dependencies
COPY requirements.txt /app/

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app code into the container
COPY . /app/

# Expose the port (if necessary for web service)
# You might not need this if it's purely a bot and not a web service
# EXPOSE 8000  # Uncomment if necessary

# Run the Python application
CMD ["python", "app.py"]
