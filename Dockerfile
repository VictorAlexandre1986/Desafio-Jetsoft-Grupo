# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /workdir

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

EXPOSE 5000

CMD ["python", "run.py"]
