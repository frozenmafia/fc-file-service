#!/bin/bash
# Change directory to 'backend' directory
if [ ! -d "backend" ]; then
    mkdir backend
fi

cd backend

# Check if the repository exists, if not, clone it
if [ ! -d "fc-file-service" ]; then
    git clone https://github.com/frozenmafia/fc-file-service.git
fi

# Change directory to the cloned repository
cd fc-file-service

# Pull the latest changes from the repository
git pull

# Build the new Docker image for fc-file-service
sudo docker build -t fc-file-service-new .

# Check if the container exists
if sudo docker ps -a --format '{{.Names}}' | grep -Eq '^fc-file-service$'; then
    # Stop the existing container
    sudo docker stop fc-file-service

    # Remove the existing container
    sudo docker rm fc-file-service
fi

# Run the new Docker container for fc-file-service with restart options
sudo docker run -d --restart=always --name fc-file-service -p 8004:8004 fc-file-service-new
