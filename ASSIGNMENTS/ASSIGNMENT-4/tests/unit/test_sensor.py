"""
Unit tests for sensor threshold evaluation and strict boundary conditions.
Matches Assignment 4 faculty specifications: U6, boundary 27.99, 28.00, 28.01.
"""

from app.services.sensor_service import sensor_breached


# ============================================================================
# U6: Sensor threshold strict greater-than: 28.00 -> False, 28.01 -> True
# ============================================================================
def test_u6_sensor_values_28_00_and_28_01():
    """
    U6: Evaluate 28.00 and 28.01 against default threshold 28.0.
    Faculty reference oracle:
    - 28.00 does NOT breach (False)
    - 28.01 breaches (True)
    """
    res_28_00 = sensor_breached(28.00, threshold=28.0)
    res_28_01 = sensor_breached(28.01, threshold=28.0)

    assert (res_28_00, res_28_01) == (False, True), (
        f"Strict greater-than failed: (28.00, 28.01) returned {(res_28_00, res_28_01)}, "
        f"expected (False, True)"
    )


# ============================================================================
# Three-point boundary testing around 28.0: 27.99, 28.00, 28.01
# ============================================================================
def test_sensor_boundary_three_point():
    """Verify 3-point boundary around threshold 28.0: 27.99, 28.00, 28.01."""
    assert sensor_breached(27.99, threshold=28.0) is False, "27.99 should not breach"
    assert sensor_breached(28.00, threshold=28.0) is False, "28.00 (equality) should not breach"
    assert sensor_breached(28.01, threshold=28.0) is True, "28.01 should breach"


# ============================================================================
# Configurable threshold testing
# ============================================================================
def test_custom_threshold_evaluation():
    """Verify custom campus threshold (e.g. Server Room 24.5C)."""
    custom_threshold = 24.5
    assert sensor_breached(24.50, threshold=custom_threshold) is False
    assert sensor_breached(24.51, threshold=custom_threshold) is True
    assert sensor_breached(30.00, threshold=custom_threshold) is True
