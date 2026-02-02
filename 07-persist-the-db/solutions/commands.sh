#!/bin/bash
# ============================================
# Module 07: Persist the DB — Solution Commands
# ============================================
# Reference commands for creating and using Docker volumes.
# ============================================

# Step 1: Create a named volume
docker volume create todo-db

# Step 2: Stop any existing container
docker rm -f $(docker ps -q --filter ancestor=todo-app) 2>/dev/null

# Step 3: Run with the volume mounted
docker run -dp 3000:3000 -v todo-db:/app/data todo-app

# Verify the volume exists
docker volume ls
docker volume inspect todo-db

# Test persistence:
# 1. Add todos at http://localhost:3000
# 2. docker rm -f $(docker ps -q --filter ancestor=todo-app)
# 3. docker run -dp 3000:3000 -v todo-db:/app/data todo-app
# 4. Todos should still be there!
