# Use the official Python image from Docker Hub
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install RabbitMQ and dependencies
RUN apt-get update && apt-get install -y rabbitmq-server

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run when the container starts
CMD rabbitmq-server & celery -A tasks worker --loglevel=INFO & streamlit run app.py