"""
Login Authentication Module
Experiment 29: Feature Branch (feature-login) and Pull Request

Author: Angulakshmi S (192524402)
Department: Computer Science and Engineering / AI & Data Science
Institution: Saveetha School of Engineering, SIMATS
"""

import hashlib
import hmac

# Secure password hashing simulation
USERS_DB = {
    "angulakshmi": {
        "reg_no": "192524402",
        "name": "Angulakshmi S",
        "role": "Administrator",
        "password_hash": hashlib.sha256("AdminSecure2026".encode("utf-8")).hexdigest()
    },
    "student01": {
        "reg_no": "192524403",
        "name": "Priya Sharma",
        "role": "Student",
        "password_hash": hashlib.sha256("PriyaPass123".encode("utf-8")).hexdigest()
    }
}

def authenticate(username, password):
    """
    Authenticate user credentials against hashed password database.
    Returns (success: bool, user_info: dict or error: str)
    """
    if not username or not password:
        return False, "Username and password are required."
    
    user = USERS_DB.get(username.lower())
    if not user:
        return False, "Invalid username or password."
    
    candidate_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    if hmac.compare_digest(user["password_hash"], candidate_hash):
        return True, {
            "name": user["name"],
            "reg_no": user["reg_no"],
            "role": user["role"]
        }
    return False, "Invalid username or password."

if __name__ == "__main__":
    print("=== Testing Login Authentication Module ===")
    test_user = "angulakshmi"
    test_pass = "AdminSecure2026"
    success, info = authenticate(test_user, test_pass)
    print(f"Login test for '{test_user}': Success={success}, Info={info}")
    
    # Test invalid credentials
    fail_success, fail_msg = authenticate(test_user, "WrongPassword")
    print(f"Login test invalid pass: Success={fail_success}, Message={fail_msg}")
