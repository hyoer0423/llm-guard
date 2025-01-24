# Use the Python 3.11 slim image
FROM python:3.11-slim

# Install system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install torch && \
    pip install -r requirements.txt

# Create a non-root user and set user environment variables
RUN useradd -m -u 1000 user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Switch to the non-root user and set the working directory
USER user
WORKDIR $HOME/app

# Copy the application to the user's directory
COPY --chown=user src/ $HOME/app

# Expose the port the app runs on
EXPOSE 8000

# Specify the default command
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
