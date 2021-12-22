#!/bin/bash
# Install the GIT package on centos7
sudo dnf install git -y

# Install Python
sudo dnf install python3 -y

# Install Postgres
sudo dnf install postgresql-server -y
sudo postgresql-setup --initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Pull the API repo from github
cd /opt
sudo git clone https://github.com/CloudBoltSoftware/cloudbolt-training-lab.git

# Create a virtual environment for the app
sudo /opt/cloudbolt-training-lab/venv/bin/python -m venv /opt/cloudbolt-training-lab/venv

# Install Requirements
sudo /opt/cloudbolt-training-lab/venv/bin/python -m pip install --upgrade pip
sudo /opt/cloudbolt-training-lab/venv/bin/python -m pip install -r /opt/cloudbolt-training-lab/requirements/local.txt

# Set the postgresql database role
sudo -u postgres psql -c "create role centos;"
sudo -u postgres psql -c "ALTER ROLE centos WITH LOGIN;"
sudo -u postgres psql -c "create database cloudbolt_training_lab OWNER centos;"

# Migrate the database
sudo python3 /opt/cloudbolt-training-lab/manage.py migrate

# Install NGINX to forward the port
sudo dnf install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx
sudo touch /etc/nginx/conf.d/cars.conf
sudo cp /opt/cloudbolt-training-lab/cloudbolt_training_lab/cars/scripts/nginx.conf /etc/nginx/nginx.conf
sudo nginx -s reload


# Configure NGINX SSL
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/nginx-selfsigned.key -out /etc/nginx/nginx-selfsigned.crt -subj "/C=EN/O=EN/OU=En/CN=*.*"

# Change SElinux settings to allow HTTTP
sudo setsebool -P httpd_can_network_connect 1

# Generate a shell script to run the API server
sudo touch /opt/runserver.sh
sudo chmod 777 /opt/runserver.sh
sudo cat << EOF > /opt/runserver.sh
#!/bin/bash
/opt/cloudbolt-training-lab/venv/bin/python3 /opt/cloudbolt-training-lab/manage.py runserver 0.0.0.0:8000
EOF

# Generate a service to run the API app
sudo touch /etc/systemd/system/runserver.service
sudo chmod 777 /etc/systemd/system/runserver.service
sudo cat << EOF > /etc/systemd/system/runserver.service
[Unit]
Description=Run script at startup after network becomes reachable
After=network.target

[Service]
User=centos
Type=simple
RemainAfterExit=yes
ExecStart=/opt/runserver.sh
TimeoutStartSec=0

[Install]
WantedBy=default.target
EOF

# Start the service
sudo systemctl daemon-reload
sudo systemctl enable runserver
sudo systemctl start runserver
