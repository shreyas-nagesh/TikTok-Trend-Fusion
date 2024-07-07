# Choose base arm64 image
FROM --platform=linux/arm64 debian:12

# Update the base image
RUN apt-get update && apt-get upgrade -y

# Install python3
RUN apt-get install python3 python3-venv -y

# Create python virtual environment
RUN python3 -m venv /venv

# Ensure the virtual environment's binaries are in the PATH
ENV PATH="/venv/bin:$PATH"

# Set work directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install dependencies
RUN apt-get install flac -y

# Install the python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
