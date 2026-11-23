"""
Q1: Feature Branch and Pull Request for Signup
Implementation: Simple Signup Function with Username and Password Validation

Requirements from Question Paper:
- Function accepts username and password
- Username is required (cannot be empty or whitespace)
- Password must contain at least 6 characters
- Invalid input must return appropriate error messages
- Valid input must return a success response
"""

def signup(username: str, password: str) -> dict:
    """
    Validates user credentials and performs signup registration.

    Parameters:
        username (str): The chosen username.
        password (str): The chosen password.

    Returns:
        dict: A dictionary containing:
            - 'success' (bool): True if signup succeeds, False otherwise.
            - 'message' (str): A descriptive feedback message.
            - 'username' (str, optional): The cleaned username if successful.
    """
    # 1. Validate Username presence and type
    if username is None:
        return {
            "success": False,
            "message": "Username is required."
        }
    
    if not isinstance(username, str):
        return {
            "success": False,
            "message": "Username must be a valid text string."
        }
    
    cleaned_username = username.strip()
    if len(cleaned_username) == 0:
        return {
            "success": False,
            "message": "Username is required."
        }

    # 2. Validate Password presence and type
    if password is None:
        return {
            "success": False,
            "message": "Password is required."
        }

    if not isinstance(password, str):
        return {
            "success": False,
            "message": "Password must be a valid text string."
        }

    if len(password) == 0:
        return {
            "success": False,
            "message": "Password is required."
        }

    # 3. Validate Password Length (minimum 6 characters required)
    if len(password) < 6:
        return {
            "success": False,
            "message": "Password must be at least 6 characters long."
        }

    # 4. Valid Signup - Return success response
    return {
        "success": True,
        "message": f"Signup successful! Welcome, {cleaned_username}.",
        "username": cleaned_username
    }


def interactive_demo():
    """Provides a beginner-friendly interactive terminal demonstration."""
    print("=" * 60)
    print(" SIMATS Engineering - Software Engineering Lab (CSA10)")
    print(" Question 1: Simple Signup Service Demonstration")
    print("=" * 60)

    # Preset sample demonstrations
    sample_cases = [
        ("Valid User (len >= 6)", "alice", "Secret123"),
        ("Boundary Case (len == 6)", "bob", "abcdef"),
        ("Empty Username", "", "Secret123"),
        ("Empty Password", "charlie", ""),
        ("Short Password (< 6 chars)", "david", "pass1"),
        ("Whitespace Username", "   ", "ValidPass123"),
    ]

    print("\n--- Running Automated Preset Demonstrations ---")
    for desc, u, p in sample_cases:
        result = signup(u, p)
        status = "SUCCESS [PASS]" if result["success"] else "REJECTED [EXPECTED]"
        print(f"[{status}] Case: {desc}")
        print(f"   Input    -> Username: '{u}', Password: '{p}'")
        print(f"   Response -> Success: {result['success']}, Message: \"{result['message']}\"\n")

    print("-" * 60)
    print("Interactive Testing (Enter credentials or press Ctrl+C to exit):")
    try:
        user_in = input("Enter Username: ")
        pass_in = input("Enter Password: ")
        res = signup(user_in, pass_in)
        print("\nResult:")
        print(f"  Success : {res['success']}")
        print(f"  Message : {res['message']}")
    except (KeyboardInterrupt, EOFError):
        print("\nDemonstration concluded.")


if __name__ == "__main__":
    interactive_demo()
