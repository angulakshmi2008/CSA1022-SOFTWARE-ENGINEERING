"""
Unit Test Suite for Q1: Simple Signup Function
Tested against Software Engineering Practical Lab Specifications
"""

import unittest
import sys
import os

# Ensure the local directory is in Python path for seamless execution
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from signup import signup


class TestSignupFunction(unittest.TestCase):
    """
    Test suite verifying all functional requirements and boundary conditions
    for the signup() function.
    """

    # -------------------------------------------------------------
    # 1. Valid Input Scenarios
    # -------------------------------------------------------------
    def test_valid_signup_standard(self):
        """Verify valid registration with strong credentials."""
        result = signup("john_doe", "SecurePass2026")
        self.assertTrue(result["success"])
        self.assertEqual(result["username"], "john_doe")
        self.assertIn("Signup successful", result["message"])

    def test_password_boundary_exactly_six_characters(self):
        """Boundary Value Analysis: Exactly 6 characters must be accepted."""
        result = signup("alice", "123456")
        self.assertTrue(result["success"])
        self.assertIn("Signup successful", result["message"])

    def test_username_with_surrounding_whitespace(self):
        """Verify usernames with leading/trailing spaces are trimmed properly."""
        result = signup("  robert  ", "ValidPass99")
        self.assertTrue(result["success"])
        self.assertEqual(result["username"], "robert")

    # -------------------------------------------------------------
    # 2. Username Validation Scenarios
    # -------------------------------------------------------------
    def test_empty_username(self):
        """Verify empty username is rejected."""
        result = signup("", "ValidPass123")
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Username is required.")

    def test_whitespace_only_username(self):
        """Verify whitespace-only username is rejected."""
        result = signup("    ", "ValidPass123")
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Username is required.")

    def test_none_username(self):
        """Verify None username is rejected."""
        result = signup(None, "ValidPass123")
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Username is required.")

    def test_non_string_username(self):
        """Verify non-string username is rejected."""
        result = signup(12345, "ValidPass123")
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Username must be a valid text string.")

    # -------------------------------------------------------------
    # 3. Password Validation Scenarios
    # -------------------------------------------------------------
    def test_empty_password(self):
        """Verify empty password is rejected."""
        result = signup("alice", "")
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Password is required.")

    def test_none_password(self):
        """Verify None password is rejected."""
        result = signup("alice", None)
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Password is required.")

    def test_password_shorter_than_six_characters_boundary_minus_one(self):
        """Boundary Value Analysis: 5 characters (1 below minimum) must be rejected."""
        result = signup("alice", "12345")
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Password must be at least 6 characters long.")

    def test_password_single_character(self):
        """Verify 1-character password is rejected."""
        result = signup("alice", "a")
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Password must be at least 6 characters long.")

    def test_password_three_characters(self):
        """Verify 3-character password is rejected."""
        result = signup("alice", "abc")
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Password must be at least 6 characters long.")

    def test_non_string_password(self):
        """Verify non-string password is rejected."""
        result = signup("alice", 12345678)
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Password must be a valid text string.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
