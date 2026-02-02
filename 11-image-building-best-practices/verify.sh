#!/bin/bash
# ============================================
# Module 11: Best Practices — Verify
# ============================================
# Checks for multi-stage Dockerfile and .dockerignore.
# Usage: bash verify.sh (from project root)
# ============================================

PASS=0
FAIL=0

echo ""
echo "=== Module 11: Image Best Practices Verification ==="
echo ""

# Check for multi-stage Dockerfile
printf "  %-35s " "Multi-stage Dockerfile"
MULTISTAGE="../app/Dockerfile.multistage"
DOCKERFILE="../app/Dockerfile"

if [ -f "$MULTISTAGE" ]; then
    FROM_COUNT=$(grep -ci "^FROM" "$MULTISTAGE")
    if [ "$FROM_COUNT" -ge 2 ]; then
        echo "PASS (Dockerfile.multistage with $FROM_COUNT stages)"
        PASS=$((PASS + 1))
    else
        echo "FAIL — Dockerfile.multistage needs multiple FROM instructions"
        FAIL=$((FAIL + 1))
    fi
elif [ -f "$DOCKERFILE" ]; then
    FROM_COUNT=$(grep -ci "^FROM" "$DOCKERFILE")
    if [ "$FROM_COUNT" -ge 2 ]; then
        echo "PASS (Dockerfile with $FROM_COUNT stages)"
        PASS=$((PASS + 1))
    else
        echo "FAIL — No multi-stage Dockerfile found"
        echo "         Create app/Dockerfile.multistage with 2+ FROM instructions"
        FAIL=$((FAIL + 1))
    fi
else
    echo "FAIL — No Dockerfile found"
    FAIL=$((FAIL + 1))
fi

# Check for .dockerignore
printf "  %-35s " ".dockerignore exists"
DOCKERIGNORE="../app/.dockerignore"
if [ -f "$DOCKERIGNORE" ]; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL — Create app/.dockerignore"
    FAIL=$((FAIL + 1))
fi

# Check .dockerignore content
printf "  %-35s " ".dockerignore excludes node_modules"
if [ -f "$DOCKERIGNORE" ] && grep -q "node_modules" "$DOCKERIGNORE"; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL — .dockerignore should exclude node_modules"
    FAIL=$((FAIL + 1))
fi

echo ""
echo "---"
echo "Results: $PASS/3 checks passed"

if [ "$PASS" -eq 3 ]; then
    echo ""
    echo "All checks passed! Try comparing image sizes:"
    echo "  docker build -t todo-app:single -f ../app/Dockerfile ../app"
    echo "  docker build -t todo-app:multi -f ../app/Dockerfile.multistage ../app"
    echo "  docker images | grep todo-app"
fi
