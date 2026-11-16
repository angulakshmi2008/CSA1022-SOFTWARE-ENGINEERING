import unittest
from Platform.src.policy_service import RegionalPolicyService

class TestRegionalPolicies(unittest.TestCase):
    def setUp(self):
        self.policy_service = RegionalPolicyService()

    def test_north_region_calculations(self):
        """Verify Region North (12% tax, $15 shipping under $100)."""
        charges = self.policy_service.calculate_charges("REG-NORTH", 50.00)
        self.assertEqual(charges["tax_amount"], 6.00)  # 50 * 0.12
        self.assertEqual(charges["shipping_amount"], 15.00)
        self.assertEqual(charges["total_amount"], 71.00)
        self.assertEqual(charges["warehouse_id"], "WH-NORTH-01")

        # Test free shipping threshold ($100+)
        free_shipping_charges = self.policy_service.calculate_charges("REG-NORTH", 120.00)
        self.assertEqual(free_shipping_charges["shipping_amount"], 0.00)

    def test_south_region_calculations(self):
        """Verify Region South (8% tax, $12 shipping under $80)."""
        charges = self.policy_service.calculate_charges("REG-SOUTH", 50.00)
        self.assertEqual(charges["tax_amount"], 4.00)  # 50 * 0.08
        self.assertEqual(charges["shipping_amount"], 12.00)
        self.assertEqual(charges["total_amount"], 66.00)
        self.assertEqual(charges["warehouse_id"], "WH-SOUTH-02")

    def test_west_region_calculations(self):
        """Verify Region West (10% tax, $10 shipping under $75, 21-day return)."""
        charges = self.policy_service.calculate_charges("REG-WEST", 50.00)
        self.assertEqual(charges["tax_amount"], 5.00)  # 50 * 0.10
        self.assertEqual(charges["shipping_amount"], 10.00)
        self.assertEqual(charges["total_amount"], 65.00)
        self.assertEqual(charges["warehouse_id"], "WH-WEST-03")

        self.assertEqual(self.policy_service.get_return_window_days("REG-WEST"), 21)

    def test_regional_refund_thresholds(self):
        """Verify regional single-approver finance limits."""
        # North limit = $500
        self.assertTrue(self.policy_service.validate_refund_threshold("REG-NORTH", 450.00))
        self.assertFalse(self.policy_service.validate_refund_threshold("REG-NORTH", 550.00))

        # South limit = $400
        self.assertTrue(self.policy_service.validate_refund_threshold("REG-SOUTH", 380.00))
        self.assertFalse(self.policy_service.validate_refund_threshold("REG-SOUTH", 450.00))

if __name__ == "__main__":
    unittest.main()
