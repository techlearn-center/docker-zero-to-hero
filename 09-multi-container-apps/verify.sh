#!/bin/bash
# ============================================
# Module 09: Multi-Container Apps — Verify
# ============================================
# Checks network, MySQL container, and app connectivity.
# Usage: bash verify.sh
# ============================================

PASS=0
FAIL=0

echo ""
echo "=== Module 09: Multi-Container Verification ==="
echo ""

# Check network exists
printf "  %-35s " "Docker network exists"
if docker network ls --format '{{.Name}}' 2>/dev/null | grep -q "todo-network"; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL — Run: docker network create todo-network"
    FAIL=$((FAIL + 1))
fi

# Check MySQL container
printf "  %-35s " "MySQL container running"
if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "mysql"; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL — Start MySQL: see solutions/commands.sh"
    FAIL=$((FAIL + 1))
fi

# Check app container
printf "  %-35s " "App container running"
if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "todo-app"; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL — Start app with MySQL env vars: see solutions/commands.sh"
    FAIL=$((FAIL + 1))
fi

# Check MYSQL_HOST env var on app
printf "  %-35s " "MYSQL_HOST configured"
APP_ID=$(docker ps -q --filter name=todo-app 2>/dev/null | head -1)
if [ -n "$APP_ID" ]; then
    if docker inspect "$APP_ID" --format '{{range .Config.Env}}{{println .}}{{end}}' 2>/dev/null | grep -q "MYSQL_HOST="; then
        echo "PASS"
        PASS=$((PASS + 1))
    else
        echo "FAIL — App missing MYSQL_HOST environment variable"
        FAIL=$((FAIL + 1))
    fi
else
    echo "SKIP — App container not running"
fi

echo ""
echo "---"
echo "Results: $PASS passed, $FAIL failed"
