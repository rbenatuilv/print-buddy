#!/bin/bash
cd ~/print-buddy || exit
git pull
docker build -t print-buddy .
docker stop print-buddy 2>/dev/null || true
docker rm print-buddy 2>/dev/null || true
docker run -d -p 8000:8000 --name print-buddy print-buddy
echo "✅ Backend redeployed!"