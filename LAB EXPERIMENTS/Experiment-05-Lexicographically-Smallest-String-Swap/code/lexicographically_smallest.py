"""
Experiment 05: Lexicographically Smallest String by Swapping Two Characters using RAPTOR
Student: Angulakshmi S (Reg No: 192524402)
Course: CSA10 - Software Engineering
Course Outcome: CO1

Algorithm Logic:
1. Input string `str`, character `ch1`, character `ch2`.
2. Initialize loop counter i = 0 (or 1 in RAPTOR 1-based indexing), n = length(str).
3. Loop through the string:
   - If current character equals ch1, replace it with ch2.
   - Else if current character equals ch2, replace it with ch1.
4. Output the resulting modified string.
"""

import sys

def find_best_swap_pair(s: str):
    """
    Scans from left to right to find the optimal pair (ch1, ch2)
    to produce the lexicographically smallest string.
    """
    n = len(s)
    for i in range(n):
        # Find the smallest character strictly smaller than s[i] appearing after i
        min_char = s[i]
        for j in range(i + 1, n):
            if s[j] < min_char:
                min_char = s[j]
        if min_char < s[i]:
            return s[i], min_char
    return None, None

def swap_all_occurrences(s: str, ch1: str, ch2: str) -> str:
    """
    Executes the exact loop and selection structure from the RAPTOR flowchart.
    Swaps all occurrences of ch1 with ch2, and ch2 with ch1.
    """
    res = list(s)
    n = len(res)
    i = 0
    while i < n:
        if res[i] == ch1:
            res[i] = ch2
        elif res[i] == ch2:
            res[i] = ch1
        i += 1
    return "".join(res)

def run_experiment(s: str, ch1: str = None, ch2: str = None):
    print("======================================================================")
    print("  RAPTOR Flowchart Simulation: Lexicographically Smallest String Swap  ")
    print("======================================================================")
    print(f"Original String (str) : {s}")
    
    if ch1 is None or ch2 is None:
        c1, c2 = find_best_swap_pair(s)
        if c1 is None:
            print("String is already lexicographically minimal. No swap required.")
            print(f"Modified string       : {s}")
            return s
        ch1, ch2 = c1, c2
        print(f"Auto-selected swap pair: ch1 = '{ch1}', ch2 = '{ch2}'")
    else:
        print(f"Selected Swap Pair     : ch1 = '{ch1}', ch2 = '{ch2}'")
        
    modified = swap_all_occurrences(s, ch1, ch2)
    print(f"Modified string        : {modified}")
    print("======================================================================")
    return modified

def main():
    # Primary manual test case
    s = "ccad"
    ch1 = "c"
    ch2 = "a"
    run_experiment(s, ch1, ch2)
    
    # Academic verification test suite
    print("\n--- Additional Test Cases Verification ---")
    test_cases = [
        ("ccad", "c", "a"),
        ("software", None, None),
        ("engineering", None, None),
        ("bbaacc", "b", "a"),
        ("zyxwv", "z", "v"),
        ("abcde", None, None)
    ]
    
    for idx, (t_str, c1, c2) in enumerate(test_cases, start=1):
        if c1 and c2:
            res = swap_all_occurrences(t_str, c1, c2)
            print(f"Case {idx:02d} | Input: '{t_str}', ch1='{c1}', ch2='{c2}' -> Output: '{res}'")
        else:
            opt_c1, opt_c2 = find_best_swap_pair(t_str)
            if opt_c1:
                res = swap_all_occurrences(t_str, opt_c1, opt_c2)
                print(f"Case {idx:02d} | Input: '{t_str}' (swap '{opt_c1}' <-> '{opt_c2}') -> Output: '{res}'")
            else:
                print(f"Case {idx:02d} | Input: '{t_str}' (already minimal) -> Output: '{t_str}'")

if __name__ == "__main__":
    main()
