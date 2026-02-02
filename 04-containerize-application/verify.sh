#!/bin/bash
# ============================================
# Module 04: Containerize Application — Verify
# ============================================
# Checks that app/Dockerfile is properly written.
# Usage: bash verify.sh (from project root)
# ============================================

DOCKERFILE="../app/Dockerfile"
PASS=0
FAIL=0

check() {
    local label="$1"
    local pattern="$2"

    printf "  %-35s " "$label"
    if grep -qiE "$pattern" "$DOCKERFILE" 2>/dev/null; then
        echo "PASS"
        PASS=$((PASS + 1))
    else
        echo "FAIL"
        FAIL=$((FAIL + 1))
    fi
}

echo ""
echo "=== Module 04: Dockerfile Verification ==="
echo ""

if [ ! -f "$DOCKERFILE" ]; then
    echo "  ERROR: $DOCKERFILE not found"
    echo "  Make sure you run this from the 04-containerize-application/ directory"
    exit 1
fi

check "FROM instruction" "^FROM\s+node"
check "WORKDIR instruction" "^WORKDIR\s+/app"
check "COPY package.json" "^COPY\s+package"
check "RUN npm install" "^RUN\s+npm\s+install"
check "COPY source files" "^COPY\s+\.\s+\."
check "EXPOSE 3000" "^EXPOSE\s+3000"
check "CMD instruction" "^CMD\s+"

echo ""
echo "---"
echo "Results: $PASS/7 checks passed"
echo ""

if [ "$PASS" -eq 7 ]; then
    echo "All checks passed! Try building: cd ../app && docker build -t todo-app ."
elif [ "$PASS" -ge 5 ]; then
    echo "Almost there! Review the failing checks above."
else
    echo "Check the hints in the README for guidance."
fi
