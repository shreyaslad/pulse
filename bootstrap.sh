# Bootstraps an EC2 server with docker compose

# NOTE: Assumes that the EC2 instance is already setup with your server files
# and that those server files are in /server 

# Make the docker-compose stack automatically start with the server
sudo cp docker_boot.service /etc/systemd/system
sudo systemctl enable docker
sudo systemctl enable docker_boot
