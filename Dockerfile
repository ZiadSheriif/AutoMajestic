# Use an existing docker image as a base
FROM ubuntu:latest

# Install wget
RUN apt-get update \
    && apt-get install -y wget

# Download the file
RUN wget https://gitlab.com/graphviz/graphviz/-/package_files/6164164/download -O graphviz.tar.gz


# Use a Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application source code into the container
COPY . .

# Expose the port that Flask will run on
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]
