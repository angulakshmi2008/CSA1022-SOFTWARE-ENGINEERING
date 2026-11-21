"""
Unit tests for priority classification, keyword triage, and matrix validation.
Matches Assignment 4 faculty specifications: U1, U2, U3, U4, U5, R1, R2.
"""

import pytest

from app.services.priority_service import (
    calculate_priority,
    classify_category,
)


# ============================================================================
# U1: High impact, High urgency -> M1
# ============================================================================
def test_u1_high_impact_high_urgency():
    """U1: High impact, high urgency must yield M1 priority."""
    result = calculate_priority(impact="High", urgency="High")
    assert result == "M1", f"Expected 'M1' for High/High, but got '{result}'"


# ============================================================================
# U2: Low impact, Low urgency -> M4
# ============================================================================
def test_u2_low_impact_low_urgency():
    """U2: Low impact, low urgency must yield M4 priority."""
    result = calculate_priority(impact="Low", urgency="Low")
    assert result == "M4", f"Expected 'M4' for Low/Low, but got '{result}'"


# ============================================================================
# U3: Invalid impact value -> Rejection
# ============================================================================
def test_u3_invalid_impact_value_rejected():
    """U3: Invalid impact value must be strictly rejected with ValueError."""
    with pytest.raises(ValueError, match="Invalid impact level"):
        calculate_priority(impact="Critical", urgency="High")

    with pytest.raises(ValueError, match="Invalid impact level"):
        calculate_priority(impact="Unknown", urgency="Low")

    with pytest.raises(ValueError, match="Invalid urgency level"):
        calculate_priority(impact="High", urgency="Immediate")


# ============================================================================
# U4: Water leak keyword classification -> Facilities
# ============================================================================
def test_u4_water_leak_classification_facilities():
    """U4: 'Water leak from lab ceiling' text must classify as Facilities."""
    description = "Water leak from lab ceiling onto workstation desks"
    category = classify_category(description)
    assert category == "Facilities", f"Expected 'Facilities', but got '{category}'"


# ============================================================================
# U5: Equal leak and projector evidence tie -> Manual Review
# ============================================================================
def test_u5_equal_leak_and_projector_evidence_manual_review():
    """U5: Equal evidence between leak and projector must result in Manual Review."""
    description = "Leak reported near classroom projector"
    # Contains 1 leak keyword ("leak") and 1 projector keyword ("projector") -> Tie (1 vs 1)
    category = classify_category(description)
    assert category == "Manual Review", f"Expected 'Manual Review' on tie, but got '{category}'"


# ============================================================================
# R1: High impact, Medium urgency -> M2 (Regression)
# ============================================================================
def test_r1_high_impact_medium_urgency_m2():
    """R1: High impact, medium urgency must yield M2 priority."""
    result = calculate_priority(impact="High", urgency="Medium")
    assert result == "M2", f"Expected 'M2' for High/Medium, but got '{result}'"


# ============================================================================
# R2: Unknown terminology -> Manual Review (Regression)
# ============================================================================
def test_r2_unknown_terminology_manual_review():
    """R2: Ambiguous or unknown maintenance terminology must be routed to Manual Review."""
    description = "The quantum flux capacitor oscillates uncontrollably"
    category = classify_category(description)
    assert category == "Manual Review", (
        f"Expected 'Manual Review' for unknown text, but got '{category}'"
    )


# ============================================================================
# Full 9-Cell Priority Matrix Verification
# ============================================================================
@pytest.mark.parametrize(
    "impact,urgency,expected",
    [
        ("High", "High", "M1"),
        ("High", "Medium", "M2"),
        ("High", "Low", "M3"),
        ("Medium", "High", "M2"),
        ("Medium", "Medium", "M3"),
        ("Medium", "Low", "M4"),
        ("Low", "High", "M3"),
        ("Low", "Medium", "M4"),
        ("Low", "Low", "M4"),
    ],
)
def test_complete_nine_cell_matrix(impact, urgency, expected):
    """Verify all 9 combinations in the configurable impact/urgency matrix."""
    assert calculate_priority(impact, urgency) == expected
