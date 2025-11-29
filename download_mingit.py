"""
RagilmalikGitCloner - MinGit Downloader
Downloads and extracts portable Git (MinGit) for Windows

Author: Ragilmalik
"""

import os
import urllib.request
import zipfile
import shutil
from pathlib import Path

# Configuration
MINGIT_URL = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/MinGit-2.43.0-64-bit.zip"
OUTPUT_DIR = "git_portable"
ZIP_NAME = "MinGit.zip"

def download_mingit():
    """Download and extract MinGit"""
    
    print("RagilmalikGitCloner - MinGit Downloader")
    print("=" * 40)

    # Create output directory
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"[+] Created directory: {OUTPUT_DIR}")
    else:
        print(f"[!] Directory exists: {OUTPUT_DIR} (skipping extraction if valid)")
        if os.path.exists(os.path.join(OUTPUT_DIR, 'cmd', 'git.exe')):
            print("[OK] MinGit already installed.")
            return

    # Download
    print(f"[-] Downloading MinGit from GitHub...")
    try:
        urllib.request.urlretrieve(MINGIT_URL, ZIP_NAME)
        print("[OK] Download complete.")
    except Exception as e:
        print(f"[ERROR] Download failed: {e}")
        return

    # Extract
    print("[-] Extracting files...")
    try:
        with zipfile.ZipFile(ZIP_NAME, 'r') as zip_ref:
            zip_ref.extractall(OUTPUT_DIR)
        print("[OK] Extraction complete.")
    except Exception as e:
        print(f"[ERROR] Extraction failed: {e}")
        return

    # Cleanup
    print("[-] Cleaning up...")
    try:
        os.remove(ZIP_NAME)
        print("[OK] Cleanup complete.")
    except:
        pass

    print("\n[SUCCESS] MinGit is ready!")
    print(f"Location: {os.path.abspath(OUTPUT_DIR)}")

if __name__ == "__main__":
    download_mingit()