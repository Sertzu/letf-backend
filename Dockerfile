# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 8080 (or whatever port your Flask API runs on)
EXPOSE 5000

# Set environment variables for production
ENV FLASK_ENV=production

# Use gunicorn to serve the Flask app in production
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
