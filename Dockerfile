# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /backend


# Copy the requirements.txt into the container at /backend/
COPY requirements.txt /backend/

# Install any Python dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project code into the container
COPY . /backend/

# Set environment variables (optional, depending on your app's needs)
ENV PYTHONUNBUFFERED 1

# Expose port 8000
EXPOSE 8000

# Command to run when the container starts
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "manage:app"]
