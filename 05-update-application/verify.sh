#!/bin/bash
# ============================================
# Module 05: Update Application — Verify
# ============================================
# Checks that the empty-state text was modified.
# Usage: bash verify.sh (from project root)
# ============================================

HTML_FILE="../app/src/static/index.html"
ORIGINAL_TEXT="No todos yet! Add one above to get started."

echo ""
echo "=== Module 05: Source Modification Verification ==="
echo ""

if [ ! -f "$HTML_FILE" ]; then
    echo "  ERROR: $HTML_FILE not found"
    exit 1
fi

printf "  %-35s " "Empty-state text modified"
if grep -q "$ORIGINAL_TEXT" "$HTML_FILE" 2>/dev/null; then
    echo "FAIL"
    echo ""
    echo "  The empty-state text still says:"
    echo "  \"$ORIGINAL_TEXT\""
    echo ""
    echo "  Change it to something different in app/src/static/index.html"
else
    echo "PASS"
    echo ""
    NEW_TEXT=$(grep -o 'id="empty-state">[^<]*' "$HTML_FILE" | sed 's/id="empty-state">//')
    echo "  New text: \"$NEW_TEXT\""
    echo ""
    echo "  Now rebuild: cd ../app && docker build -t todo-app ."
fi
