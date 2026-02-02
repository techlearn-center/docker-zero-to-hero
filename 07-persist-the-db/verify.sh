#!/bin/bash
# ============================================
# Module 07: Persist the DB — Verify
# ============================================
# Checks that a Docker volume exists for data persistence.
# Usage: bash verify.sh
# ============================================

PASS=0
FAIL=0

echo ""
echo "=== Module 07: Volume Persistence Verification ==="
echo ""

# Check if todo-db volume exists
printf "  %-35s " "todo-db volume exists"
if docker volume inspect todo-db > /dev/null 2>&1; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL — Run: docker volume create todo-db"
    FAIL=$((FAIL + 1))
fi

# Check if a container is running with the volume
printf "  %-35s " "Container using volume"
RUNNING=$(docker ps --format '{{.ID}}' --filter ancestor=todo-app 2>/dev/null | head -1)
if [ -n "$RUNNING" ]; then
    MOUNTS=$(docker inspect "$RUNNING" --format '{{range .Mounts}}{{.Name}} {{end}}' 2>/dev/null)
    if echo "$MOUNTS" | grep -q "todo-db"; then
        echo "PASS"
        PASS=$((PASS + 1))
    else
        echo "FAIL — Container running but not using todo-db volume"
        FAIL=$((FAIL + 1))
    fi
else
    echo "SKIP — No todo-app container running"
    echo "         Run: docker run -dp 3000:3000 -v todo-db:/app/data todo-app"
fi

echo ""
echo "---"
echo "Results: $PASS passed, $FAIL failed"
