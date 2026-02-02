#!/bin/bash
# ============================================
# Module 08: Use Bind Mounts — Solution Commands
# ============================================
# Reference commands for development with bind mounts.
# Run from the PROJECT ROOT directory (not app/).
# ============================================

# Stop any existing container
docker rm -f $(docker ps -q --filter ancestor=todo-app) 2>/dev/null

# --- Linux / macOS ---
docker run -dp 3000:3000 \
  -v todo-db:/app/data \
  -v "$(pwd)/app:/app" \
  -v /app/node_modules \
  -w /app \
  todo-app sh -c "npm install && npx nodemon src/index.js"

# --- Windows (PowerShell) ---
# docker run -dp 3000:3000 `
#   -v todo-db:/app/data `
#   -v "${PWD}/app:/app" `
#   -v /app/node_modules `
#   -w /app `
#   todo-app sh -c "npm install && npx nodemon src/index.js"

# Flags explained:
#   -v todo-db:/app/data        Named volume for database (Module 07)
#   -v "$(pwd)/app:/app"        Bind mount: local app/ → container /app/
#   -v /app/node_modules        Anonymous volume: prevent overwrite of node_modules
#   -w /app                     Set working directory
#   sh -c "npm install && ..."  Install deps then start with nodemon

# Test it:
# 1. Open http://localhost:3000
# 2. Edit app/src/static/index.html
# 3. Save the file
# 4. Refresh the browser — change appears instantly!
