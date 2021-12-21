# Install the GIT package on centos7
sudo dnf install git -y

# Install Python
sudo dnf install python3 -y

# Install Postgres
sudo dnf install postgresql-server -y
sudo dnf module enable postgresql:12
sudo postgresql-setup --initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Pull the API repo from github
cd /opt
sudo git clone https://github.com/CloudBoltSoftware/cloudbolt-training-lab.git

# Install Requirements
pip3 install -r /opt/cloudbolt-training-lab/requirements/local.txt

# Set the postgresql database role
sudo -u postgres psql -c "create role centos;"
sudo -u postgres psql -c "ALTER ROLE centos WITH LOGIN;"
sudo -u postgres psql -c "create database cloudbolt_training_lab OWNER centos;"

# Migrate the database
python3 /opt/cloudbolt-training-lab/manage.py migrate

# Install NGINX to forward the port
sudo dnf install nginx -y
sudo systemctl start nginx
sudo touch /etc/nginx/conf.d/cars.conf
sudo cat  <<EOF > /etc/nginx/default.d/cars.conf
location /cars/ {
    proxy_pass http://0.0.0.0:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
EOF

# Change SElinux settings to allow HTTTP
sudo setsebool -P httpd_can_network_connect 1

# Run the API server
cd /opt/cloudbolt-training-lab
python3 manage.py runserver 0.0.0.0:8000
