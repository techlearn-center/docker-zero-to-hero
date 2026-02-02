#!/bin/bash
# ============================================
# Module 10: Docker Compose — Verify
# ============================================
# Validates the docker-compose.yml file structure.
# Usage: bash verify.sh (from project root)
# ============================================

COMPOSE="../docker-compose.yml"
PASS=0
FAIL=0

check() {
    local label="$1"
    local pattern="$2"

    printf "  %-35s " "$label"
    if grep -qE "$pattern" "$COMPOSE" 2>/dev/null; then
        echo "PASS"
        PASS=$((PASS + 1))
    else
        echo "FAIL"
        FAIL=$((FAIL + 1))
    fi
}

echo ""
echo "=== Module 10: Docker Compose Verification ==="
echo ""

if [ ! -f "$COMPOSE" ]; then
    echo "  ERROR: docker-compose.yml not found at project root"
    exit 1
fi

check "services: section" "^services:"
check "web (or app) service" "^\s+(web|app):"
check "build directive" "build:"
check "port mapping" "3000:3000"
check "mysql service" "^\s+mysql:"
check "MySQL image" "mysql:8"
check "MYSQL_HOST env var" "MYSQL_HOST"
check "depends_on" "depends_on"
check "volumes section" "^volumes:"
check "Named volume" "mysql-data"

echo ""
echo "---"
echo "Results: $PASS/10 checks passed"
echo ""

if [ "$PASS" -eq 10 ]; then
    echo "All checks passed! Run: docker compose up -d"
elif [ "$PASS" -ge 7 ]; then
    echo "Almost there! Review the failing checks."
else
    echo "Check the hints in the README for guidance."
fi
