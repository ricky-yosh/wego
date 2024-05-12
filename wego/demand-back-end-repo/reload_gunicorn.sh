#!/bin/bash
# The purpose of this is to make reloading the backend of the demand cloud easier

echo -e "Reloading daemon..."
sudo systemctl daemon-reload

echo -e "Restarting gunicorn services..."
sudo systemctl restart demand-services
echo -e "   └─ Restarting demand-services service..."
sudo systemctl restart common-services
echo -e "   └─ Restarting common-services service..."
echo -e "        └─ NOTE: [IF RUNNING IN PROD] Ensure to check that the respective .service and .socket are active.\n"

echo -e "Restarting NGINX..."
sudo systemctl restart nginx

echo -e "Restarting mysql..."
sudo systemctl restart mysql

echo -e "Checking nginx health..."
sudo nginx -t

echo -e "~~~~ Check for any issues here: ~~~~"
sudo systemctl status mysql
sudo systemctl status nginx
sudo systemctl status demand-services.service
sudo systemctl status common-services.service
sudo systemctl status demand-services.socket
sudo systemctl status common-services.socket
