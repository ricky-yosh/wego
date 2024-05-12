#!/bin/bash
# The purpose of this is to make reloading the backend of the supply cloud easier

echo -e "Reloading daemon..."
sudo systemctl daemon-reload

echo -e "Restarting gunicorn services..."
sudo systemctl restart supply-services
echo -e "   └─ Restarting supply-services service..."
sudo systemctl restart common-services
echo -e "   └─ Restarting common-services service..."
sudo systemctl restart map-services
echo -e "   └─ Restarting map-services service..."
echo -e "        └─ NOTE: [IF RUNNING IN PROD] Ensure to check that the respective .service and .socket are active.\n"

echo -e "Restarting NGINX..."
sudo systemctl restart nginx

echo -e "Restarting MongoDB..."
sudo systemctl restart mongod

echo -e "Checking nginx health..."
sudo nginx -t

echo -e "~~~~ Check for any issues here: ~~~~"
sudo systemctl status mongod
sudo systemctl status nginx
sudo systemctl status supply-services.service
sudo systemctl status common-services.service
sudo systemctl status map-services.service
sudo systemctl status supply-services.socket
sudo systemctl status common-services.socket
sudo systemctl status map-services.socket
