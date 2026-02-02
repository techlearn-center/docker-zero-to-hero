#!/bin/bash
# ============================================
# Module 08: Use Bind Mounts — Verify
# ============================================
# Checks that nodemon is available for dev workflow.
# Usage: bash verify.sh (from project root)
# ============================================

echo ""
echo "=== Module 08: Bind Mount Dev Workflow Verification ==="
echo ""

# Check that nodemon is in devDependencies
printf "  %-35s " "nodemon in devDependencies"
if grep -q "nodemon" "../app/package.json" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL — nodemon should be in package.json devDependencies"
fi

# Check if dev script exists
printf "  %-35s " "dev script in package.json"
if grep -q '"dev"' "../app/package.json" 2>/dev/null; then
    echo "PASS"
else
    echo "FAIL — Add a \"dev\" script using nodemon to package.json"
fi

# Check if a container is running with bind mounts
printf "  %-35s " "Container with bind mount"
RUNNING=$(docker ps --format '{{.ID}}' --filter ancestor=todo-app 2>/dev/null | head -1)
if [ -n "$RUNNING" ]; then
    MOUNTS=$(docker inspect "$RUNNING" --format '{{range .Mounts}}{{.Type}} {{end}}' 2>/dev/null)
    if echo "$MOUNTS" | grep -q "bind"; then
        echo "PASS"
    else
        echo "INFO — Container running but no bind mount detected"
    fi
else
    echo "SKIP — No todo-app container running"
fi

echo ""
echo "  To test bind mounts, run the command from solutions/commands.sh"
