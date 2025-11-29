"""
RagilmalikGitCloner - Git Configuration Module
Handles Git executable detection (system vs bundled)

Author: Ragilmalik
"""

import os
import sys
import shutil
from typing import Tuple, Optional


def is_git_installed() -> bool:
    """
    Check if git is installed on the system path

    Returns:
        True if git command works, False otherwise
    """
    return shutil.which("git") is not None


def get_bundled_git_path() -> Optional[str]:
    """
    Get path to bundled MinGit if it exists

    Returns:
        Path to git.exe in bundled folder, or None if not found
    """
    # Get base path (handling PyInstaller temp folder)
    if getattr(sys, 'frozen', False):
        # Running as compiled .exe
        base_path = sys._MEIPASS
    else:
        # Running from source
        base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    # Check for git_portable/cmd/git.exe
    # Relative to project root
    bundled_git_path = os.path.join(base_path, 'git_portable', 'cmd', 'git.exe')

    if os.path.exists(bundled_git_path):
        return bundled_git_path
    
    # Try finding it in root if not found in nested structure
    bundled_git_path_alt = os.path.join(base_path, '..', 'git_portable', 'cmd', 'git.exe')
    if os.path.exists(bundled_git_path_alt):
        return os.path.abspath(bundled_git_path_alt)

    return None


def get_git_executable() -> Tuple[str, str, bool]:
    """
    Determine the best git executable to use

    Returns:
        (git_path, source, is_valid)
        source: 'bundled', 'system', or 'none'
    """
    # 1. Check for bundled MinGit (Priority for portability)
    bundled_path = get_bundled_git_path()
    if bundled_path:
        return bundled_path, 'bundled', True

    # 2. Check for system Git
    if is_git_installed():
        return 'git', 'system', True

    # 3. None found
    return '', 'none', False


def configure_git_environment():
    """
    Configure GitPython to use the correct git executable
    MUST be called before importing git or using GitPython
    """
    git_path, source, is_valid = get_git_executable()

    if is_valid and source == 'bundled':
        # Set GIT_PYTHON_GIT_EXECUTABLE env var
        os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = git_path
        # Add git cmd to PATH just in case
        git_dir = os.path.dirname(git_path)
        os.environ['PATH'] = git_dir + os.pathsep + os.environ['PATH']
        print(f"[Config] Using bundled Git: {git_path}")
    elif is_valid and source == 'system':
        print("[Config] Using system Git")
    else:
        print("[Config] No Git executable found!")


def initialize_git() -> Tuple[bool, str]:
    """
    Initialize Git and verify it works

    Returns:
        (success, message)
    """
    try:
        configure_git_environment()
        
        # Test import
        import git
        
        # Test command execution
        try:
            git.Git().version()
            return True, "Git initialized successfully"
        except Exception as e:
            return False, f"Git executable found but failed to run: {e}"

    except ImportError:
        return False, "GitPython module not found"
    except Exception as e:
        return False, f"Git initialization failed: {e}"


def get_git_status_report() -> str:
    """
    Get a detailed status report of Git configuration

    Returns:
        Multi-line string with status
    """
    git_path, source, is_valid = get_git_executable()
    
    report = []
    report.append(f"Git Source: {source.upper()}")
    report.append(f"Executable Path: {git_path if git_path else 'Not found'}")
    
    if is_valid:
        try:
            import git
            version = git.Git().version()
            report.append(f"Git Version: {version}")
        except:
            report.append("Git Version: Unknown (Error execution)")
    else:
        report.append("Status: CRITICAL ERROR - Git not found")
        report.append("")
        report.append("TROUBLESHOOTING:")
        report.append("1. Ensure 'git_portable' folder exists next to the application")
        report.append("2. Or install Git for Windows globally")
        
    return "\n".join(report)


def get_missing_git_instructions() -> str:
    """
    Get user-friendly instructions when Git is missing

    Returns:
        Instruction string
    """
    return """
CRITICAL ERROR: Git not found!

RagilmalikGitCloner needs 'git' to work.

SOLUTIONS:
1. [RECOMMENDED] Ensure the 'git_portable' folder is in the same directory as this application.
   This application comes with a bundled portable Git. Do not delete that folder!

2. Install Git for Windows manually from https://git-scm.com/download/win

After fixing, please restart the application.
"""


def get_setup_instructions() -> str:
    """
    Instructions for first-time setup if using source
    """
    return """
RagilmalikGitCloner could not find Git on this system.

If you are a user:
- Ensure you have extracted the FULL zip file.
- The 'git_portable' folder MUST be next to RagilmalikGitCloner.exe.

If you are a developer:
- Run 'python download_mingit.py' to fetch the portable Git.
- Or install Git on your system and add it to PATH.
"""