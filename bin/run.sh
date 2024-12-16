#!/bin/bash
VERSION=1.0.0

export IP_LOCAL=$MY_POD_IP

echo "--------IP_LOCAL-------"
echo "-----" $IP_LOCAL "-----"

cd /opt/service

fastapi run
