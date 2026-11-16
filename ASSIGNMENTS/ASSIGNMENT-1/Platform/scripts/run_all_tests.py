#!/usr/bin/env python3
import sys
import os
import unittest
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

def run_suite():
    print("=" * 75)
    print("  CSA10 SOFTWARE ENGINEERING - AUTOMATED TEST SUITE")
    print("  Validating Measurable Delivery Criteria: MSC-01 through MSC-05")
    print("=" * 75)

    test_dir = os.path.join(root_dir, "Platform", "tests")
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=test_dir, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    start_time = time.time()
    result = runner.run(suite)
    duration = time.time() - start_time

    print("\n" + "=" * 75)
    print("  TEST EXECUTION SUMMARY:")
    print(f"  Tests Run:     {result.testsRun}")
    print(f"  Passed:        {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  Failures:      {len(result.failures)}")
    print(f"  Errors:        {len(result.errors)}")
    print(f"  Time Elapsed:  {duration:.2f} seconds")
    print("=" * 75)

    if result.wasSuccessful():
        print("  >>> ALL ASSIGNMENT ACCEPTANCE TESTS PASSED (100% SUCCESS) <<<")
        sys.exit(0)
    else:
        print("  >>> TEST SUITE DETECTED FAILURES <<<")
        sys.exit(1)

if __name__ == "__main__":
    run_suite()
