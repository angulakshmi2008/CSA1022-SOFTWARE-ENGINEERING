"""
YouTube Video Downloader Utility
Experiment 30: Forking, Feature Branch and Pull Request to Original Repository

Original Project: 3-Simple-Python-Projects
Feature Contributor: Angulakshmi S (Register Number: 192524402)
Department: Computer Science and Engineering / AI & Data Science
Institution: Saveetha School of Engineering, SIMATS
"""

import os
import re

def display_project_info():
    """Display contributor and project enhancement metadata."""
    print("=" * 65)
    print("        YouTube Video Downloader - Enhanced Utility        ")
    print("=" * 65)
    print("  Feature: Project Information & Progress Tracking Interface")
    print("  Author : Angulakshmi S (Reg No: 192524402)")
    print("  Branch : feature-update | Upstream PR Contribution")
    print("  College: Saveetha School of Engineering, SIMATS")
    print("=" * 65)

def validate_url(url):
    """Validate YouTube URL format using regular expression."""
    pattern = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$'
    return bool(re.match(pattern, url.strip()))

def calculate_download_progress(bytes_downloaded, total_bytes):
    """Calculate progress percentage and human readable display string."""
    if total_bytes <= 0:
        return 0.0, "0%"
    percent = (bytes_downloaded / total_bytes) * 100.0
    return percent, f"{percent:.1f}% ({bytes_downloaded}/{total_bytes} bytes)"

def download_video(url, output_path="./downloads"):
    """Simulate robust video downloading pipeline."""
    if not validate_url(url):
        return False, "Invalid YouTube URL format."
    os.makedirs(output_path, exist_ok=True)
    display_project_info()
    print(f"Target URL: {url}")
    print(f"Target Save Directory: {output_path}")
    
    # Progress simulation
    total = 10485760 # 10MB
    for chunk in [2621440, 5242880, 7864320, 10485760]:
        pct, label = calculate_download_progress(chunk, total)
        print(f"  [DOWNLOADING] {label}")
    print("[SUCCESS] Video download completed successfully.")
    return True, os.path.join(output_path, "sample_video.mp4")

if __name__ == "__main__":
    display_project_info()
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    print("\nValidating test URL:", test_url, "->", validate_url(test_url))
    download_video(test_url, output_path="./test_downloads")
