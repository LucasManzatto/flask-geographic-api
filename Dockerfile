# Dockerfile

# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files to the container
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 5000

# Command to start the Flask app
CMD ["python", "app.py"]