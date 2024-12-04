# Use an official Python image as the base
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt (assuming you have it)
COPY ./API/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port your application runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
