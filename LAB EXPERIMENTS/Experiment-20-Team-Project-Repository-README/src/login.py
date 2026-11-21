"""
Module: Login Authentication
Author: Angulakshmi S (Reg No: 192524402)
Role: Student 1 (Feature Branch: feature-login)
Course: CSA10 - Software Engineering
"""

def login(username, password):
    """Validate user credentials against registered student authentication directory."""
    users = {
        "admin": "admin123",
        "student": "pass123",
        "angulakshmi": "pass192524402"
    }
    if users.get(username) == password:
        return "Login successful"
    return "Invalid credentials"

if __name__ == "__main__":
    print("Testing Login Authentication Module:")
    print("Test 1 (Valid):", login("angulakshmi", "pass192524402"))
    print("Test 2 (Invalid):", login("admin", "wrongpass"))
