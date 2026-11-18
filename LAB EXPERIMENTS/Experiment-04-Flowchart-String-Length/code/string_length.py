"""
Experiment 04: Flowchart to Find the Length of a String using RAPTOR
Student: Angulakshmi S (Reg No: 192524402)
Course: CSA10 - Software Engineering
Course Outcome: CO1

This Python script models the exact execution logic of the RAPTOR flowchart:
Symbols modeled:
1. Start (Program Entry)
2. Input: Prompt "Enter a String:" -> Variable `str`
3. Assignment: `length <- Length_Of(str)`
4. Output: "Total Number of Characters = " + length
5. End (Program Exit)
"""

import sys

def length_of(s: str) -> int:
    """
    Simulates RAPTOR's built-in Length_Of() function.
    Returns the count of characters in string s.
    """
    # In RAPTOR, Length_Of(str) counts the total number of characters
    count = 0
    for _ in s:
        count += 1
    return count

def run_flowchart(input_str: str) -> int:
    print("==================================================")
    print("      RAPTOR Flowchart Simulation: String Length   ")
    print("==================================================")
    print(f"Input: Enter a String: {input_str}")
    
    # Assignment: length <- Length_Of(str)
    length = length_of(input_str)
    
    # Output: Total Number of Characters = <length>
    print(f"Output: Total Number of Characters = {length}")
    print("==================================================")
    return length

def main():
    if len(sys.argv) > 1:
        test_input = sys.argv[1]
    else:
        test_input = "SoftwareEngineering"
    
    run_flowchart(test_input)
    
    # Run test suite of academic test cases
    print("\n--- Additional Test Cases Verification ---")
    test_suite = [
        "SoftwareEngineering",
        "Saveetha School of Engineering",
        "CSA10-Software-Engineering",
        "AI & Data Science",
        "Hello World!",
        ""
    ]
    for idx, test in enumerate(test_suite, start=1):
        res = length_of(test)
        print(f"Test {idx:02d} | Input: '{test}' | Length: {res}")

if __name__ == "__main__":
    main()
