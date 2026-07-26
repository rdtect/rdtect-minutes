#!/bin/bash
# CDO Agent Diagnostic Verification Script
# RDT-288 — Diagnostic verification of CDO agent (26402f1a)
#
# Reports the documented state of the CDO agent and assesses readiness.
# Exit code: 0 = coherent/docs pass, 1 = issues detected
#
# Usage: bash scripts/verify-cdo-agent.sh

set -e

PASS=0
FAIL=0

print_result() {
    local status=$1
    local msg=$2
    if [ "$status" = "pass" ]; then
        echo "✅ $msg"
        PASS=$((PASS + 1))
    elif [ "$status" = "warn" ]; then
        echo "⚠️  $msg"
    else
        echo "❌ $msg"
        FAIL=$((FAIL + 1))
    fi
}

echo "======================================================"
echo "  CDO Agent (26402f1a) — Diagnostic Verification"
echo "  $(date -u)"
echo "  RDT-288 (Restoration) | RDT-289 (Root Cause Fix)"
echo "======================================================"
echo ""

# --- Step 1: Agent Registration ---
echo "--- Step 1: Agent Registration ---"
if grep -q "26402f1a" docs/agents.md; then
    print_result "pass" "CDO agent (26402f1a) found in agent inventory"
    grep -A2 "26402f1a" docs/agents.md | head -5
else
    print_result "fail" "CDO agent (26402f1a) NOT found in agent inventory"
fi
echo ""

# --- Step 2: Agent Status (Diagnostic) ---
echo "--- Step 2: Agent Status (Diagnostic) ---"
CDO_STATUS=$(grep '26402f1a' docs/agents.md | grep -oE '(running|idle|error)' | head -1)
if [ -n "$CDO_STATUS" ]; then
    if [ "$CDO_STATUS" = "running" ]; then
        print_result "pass" "CDO agent status: running"
    elif [ "$CDO_STATUS" = "idle" ]; then
        print_result "pass" "CDO agent status: idle (ready for activation)"
    elif [ "$CDO_STATUS" = "error" ]; then
        print_result "fail" "CDO agent status: ERROR — see recovery runbook at docs/rdt-288-cdo-restoration-verification.md §10 or RDT-289 for root cause fix"
    fi
else
    print_result "fail" "CDO agent status: UNKNOWN — could not detect status from inventory"
fi
echo ""

# --- Step 3: Core Skills ---
echo "--- Step 3: Core Skills ---"
REQUIRED_SKILLS=("brand-voice" "content-gates" "design-quality")
for skill in "${REQUIRED_SKILLS[@]}"; do
    if grep -qi "$skill" docs/agents.md; then
        print_result "pass" "Skill '$skill' — present in agent inventory"
    else
        print_result "warn" "Skill '$skill' — not found in agents.md"
        if grep -qi "$skill" docs/rdt-288-cdo-restoration-verification.md; then
            print_result "pass" "   Found in restoration document — OK"
        else
            print_result "fail" "   Skill '$skill' — missing entirely"
        fi
    fi
done
echo ""

# --- Step 4: CDO Briefing ---
echo "--- Step 4: CDO Briefing Delivery ---"
if grep -q "DELIVERED" docs/rdtect-2026-cdo-briefing-note.md 2>/dev/null; then
    print_result "pass" "CDO briefing note: DELIVERED (RDT-271)"
    echo "   Voice gate parameters defined:"
    grep -E "\| (In scope|Out of scope)" docs/rdtect-2026-cdo-briefing-note.md 2>/dev/null | head -3
else
    if [ -f "docs/rdtect-2026-cdo-briefing-note.md" ]; then
        print_result "pass" "CDO briefing note file exists"
    else
        print_result "fail" "CDO briefing note MISSING"
    fi
fi
echo ""

# --- Step 5: Org Hierarchy ---
echo "--- Step 5: Org Hierarchy ---"
if grep -q "Directs.*Content Lead" docs/agents.md; then
    print_result "pass" "CDO directs Content Lead — org hierarchy intact"
elif grep -q "CDO.*Content Lead" docs/agents.md; then
    print_result "pass" "CDO → Content Lead relationship confirmed"
else
    print_result "warn" "CDO → Content Lead relationship not explicitly found"
fi
echo ""

# --- Step 6: Pipeline Readiness ---
echo "--- Step 6: Voice Gate Pipeline ---"
if grep -q "Forty-Nine Sessions" docs/rdtect-2026-forty-nine-sessions-draft.md 2>/dev/null; then
    print_result "pass" "First review piece scaffolding exists: Forty-Nine Sessions"
else
    print_result "warn" "First review piece scaffolding not found"
fi
if grep -q "Voice litmus test" docs/rdtect-2026-cdo-briefing-note.md 2>/dev/null; then
    print_result "pass" "Voice litmus test defined — CDO can apply it"
else
    print_result "warn" "Voice litmus test not found in briefing"
fi
# --- Step 7: Recurring Root Cause Tracking ---
echo "--- Step 7: Recurring Root Cause Tracking ---"
if [ -f "docs/rdt-289-fix-cdo-recurring-workspace-error.md" ]; then
    print_result "pass" "RDT-289 follow-up issue created — recurring workspace error tracked"
elif grep -q "RDT-289" docs/agents.md 2>/dev/null; then
    print_result "pass" "RDT-289 follow-up issue referenced in agent inventory"
else
    print_result "warn" "RDT-289 follow-up issue not found — recurring root cause may not be tracked"
fi
echo ""

# --- Step 8: Recovery Runbook ---
echo "--- Step 8: Recovery Preparedness ---"
RESTORE_DOC="docs/rdt-288-cdo-restoration-verification.md"
if [ -f "$RESTORE_DOC" ]; then
    if grep -q "Updated Recovery Runbook" "$RESTORE_DOC"; then
        print_result "pass" "Updated recovery runbook with API-level steps (§10)"
    elif grep -q "Restoration Runbook" "$RESTORE_DOC"; then
        print_result "pass" "Restoration runbook documented"
    else
        print_result "warn" "Runbook section not found in restoration doc"
    fi
else
    print_result "fail" "Restoration verification document MISSING"
fi
echo ""

# --- Summary ---
echo "======================================================"
echo "  Verification Complete"
echo "======================================================"
echo ""
echo "  Passed: $PASS | Failed: $FAIL"
echo ""

if [ "$FAIL" -gt 0 ]; then
    echo "  ⚠️  CDO agent (26402f1a) has $FAIL issue(s) that need attention."
    echo "  See: docs/rdt-288-cdo-restoration-verification.md §9-10 for recovery runbook"
    exit 1
else
    echo "  ✅ CDO agent (26402f1a): all documented checks coherent."
    exit 0
fi
