# Use the official PyTorch base image
FROM python:3.11-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the files
COPY . .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the app's port
EXPOSE 8000

# Start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]