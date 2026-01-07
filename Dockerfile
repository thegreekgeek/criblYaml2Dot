# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install graphviz
RUN apt-get update && apt-get install -y graphviz

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables for the Cribl API.
# These should be set when running the container.
ENV CRIBL_BASE_URL="http://localhost:9000"
ENV CRIBL_AUTH_TOKEN=""

# Run app.py when the container launches
CMD ["python", "app.py"]
