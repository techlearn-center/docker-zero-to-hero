#!/bin/bash
# ============================================
# Module 06: Share Application — Verify
# ============================================
# Checks that the image has been properly tagged.
# Usage: bash verify.sh (from project root)
# ============================================

echo ""
echo "=== Module 06: Image Sharing Verification ==="
echo ""

# Check if todo-app image exists
printf "  %-35s " "todo-app image exists"
if docker images --format '{{.Repository}}:{{.Tag}}' 2>/dev/null | grep -q "^todo-app"; then
    echo "PASS"
else
    echo "FAIL — Build the image first: cd ../app && docker build -t todo-app ."
fi

# Check if a tagged version exists (username/todo-app:tag pattern)
printf "  %-35s " "Image tagged with username"
TAGGED=$(docker images --format '{{.Repository}}:{{.Tag}}' 2>/dev/null | grep -E "^[a-z0-9]+/todo-app:")
if [ -n "$TAGGED" ]; then
    echo "PASS"
    echo ""
    echo "  Tagged image found: $TAGGED"
else
    echo "FAIL"
    echo ""
    echo "  No tagged image found matching USERNAME/todo-app:TAG"
    echo "  Run: docker tag todo-app YOUR_USERNAME/todo-app:1.0"
fi

echo ""
echo "  To push: docker push YOUR_USERNAME/todo-app:1.0"
