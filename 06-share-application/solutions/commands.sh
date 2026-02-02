#!/bin/bash
# ============================================
# Module 06: Share Application — Solution Commands
# ============================================
# Reference commands for tagging and pushing your image.
# Replace YOUR_USERNAME with your Docker Hub username.
# ============================================

# Step 1: Log in to Docker Hub
docker login

# Step 2: Tag your image
# Format: docker tag SOURCE_IMAGE USERNAME/REPOSITORY:TAG
docker tag todo-app YOUR_USERNAME/todo-app:1.0

# Step 3: Push to Docker Hub
docker push YOUR_USERNAME/todo-app:1.0

# Step 4: Verify on Docker Hub
# Visit: https://hub.docker.com/r/YOUR_USERNAME/todo-app

# Bonus: Test pulling on a "fresh machine"
# docker rmi todo-app YOUR_USERNAME/todo-app:1.0
# docker pull YOUR_USERNAME/todo-app:1.0
# docker run -dp 3000:3000 YOUR_USERNAME/todo-app:1.0
