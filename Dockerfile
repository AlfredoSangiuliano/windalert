# Use the official Python image as base
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the Python script to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the script when the container starts
CMD ["python", "windforecast.py"]