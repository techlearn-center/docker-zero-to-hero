#!/bin/bash
# ============================================
# Module 00: Docker Installation Verification
# ============================================
# Run this script to confirm Docker is properly installed.
# Usage: bash verify.sh
# ============================================

PASS=0
FAIL=0

check() {
    local label="$1"
    local cmd="$2"

    printf "  %-30s " "$label"
    if eval "$cmd" > /dev/null 2>&1; then
        echo "PASS"
        PASS=$((PASS + 1))
    else
        echo "FAIL"
        FAIL=$((FAIL + 1))
    fi
}

echo ""
echo "=== Docker Installation Verification ==="
echo ""

check "Docker CLI installed" "docker --version"
check "Docker Compose installed" "docker compose version"
check "Docker daemon running" "docker info"
check "Can pull images" "docker pull hello-world"
check "Can run containers" "docker run --rm hello-world"

echo ""
echo "---"
echo "Results: $PASS passed, $FAIL failed"
echo ""

if [ "$FAIL" -eq 0 ]; then
    echo "All checks passed! You're ready for Module 01."
else
    echo "Some checks failed. See 00-get-docker/README.md for troubleshooting."
fi
