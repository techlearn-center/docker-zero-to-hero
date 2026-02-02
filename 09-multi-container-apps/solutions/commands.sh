#!/bin/bash
# ============================================
# Module 09: Multi-Container Apps — Solution Commands
# ============================================
# Reference commands for Docker networking with MySQL.
# ============================================

# Step 1: Create a network
docker network create todo-network

# Step 2: Start MySQL
docker run -d \
  --name mysql \
  --network todo-network \
  -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=todos \
  -v todo-mysql-data:/var/lib/mysql \
  mysql:8.0

# Wait for MySQL to initialize (~10 seconds)
echo "Waiting for MySQL to initialize..."
sleep 10

# Step 3: Start the app connected to MySQL
docker run -dp 3000:3000 \
  --name todo-app \
  --network todo-network \
  -e MYSQL_HOST=mysql \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=secret \
  -e MYSQL_DB=todos \
  todo-app

# Step 4: Verify
echo ""
echo "Checking containers..."
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "Checking network..."
docker network inspect todo-network --format '{{range .Containers}}{{.Name}} {{end}}'

echo ""
echo "App logs (check for 'Using MySQL persistence'):"
docker logs todo-app 2>&1 | tail -5

echo ""
echo "Open http://localhost:3000 to test!"
