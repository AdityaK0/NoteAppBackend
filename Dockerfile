# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /backend

# Install system dependencies


# Copy the requirements.txt into the container at /app
COPY requirements.txt /app/

# Install any Python dependencies (specified in requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container at /app
COPY . /app/

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Expose the port that the Django app will run on
EXPOSE 8000

# Command to run when the container starts
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
