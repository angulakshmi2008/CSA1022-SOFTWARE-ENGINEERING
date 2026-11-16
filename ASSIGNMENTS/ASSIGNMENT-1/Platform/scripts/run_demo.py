#!/usr/bin/env python3
import sys
import os

# Add root directory to python path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from Platform.src.cli import run_interactive_demo

if __name__ == "__main__":
    run_interactive_demo()
