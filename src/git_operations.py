"""
RagilmalikGitCloner - Git Operations Module
Handles repository cloning, size calculation, and metadata extraction
NOW WITH BUNDLED GIT SUPPORT AND ENHANCED ERROR HANDLING

Author: Ragilmalik
"""

import os
import re
from datetime import datetime
from typing import Dict, Tuple, Any
from pathlib import Path

# Import our modules
from git_config import initialize_git, get_git_executable
from error_handler import ErrorFormatter


# Initialize Git configuration (bundled or system)
_git_initialized = False
_git_init_message = ""


def ensure_git_initialized() -> Tuple[bool, str]:
    """
    Ensure Git is initialized before operations

    Returns:
        Tuple of (success, message)
    """
    global _git_initialized, _git_init_message

    if not _git_initialized:
        _git_initialized, _git_init_message = initialize_git()

    return _git_initialized, _git_init_message


def parse_repo_info(url: str) -> Tuple[str, str]:
    """
    Extract username and repository name from GitHub URL

    Args:
        url: GitHub repository URL

    Returns:
        Tuple of (username, repo_name)

    Examples:
        >>> parse_repo_info("https://github.com/torvalds/linux.git")
        ('torvalds', 'linux')
    """
    # Remove .git suffix if present
    url = url.replace('.git', '')

    # Extract username and repo name using regex
    pattern = r'github\.com/([^/]+)/([^/]+)'
    match = re.search(pattern, url)

    if match:
        username = match.group(1)
        repo_name = match.group(2)
        return username, repo_name

    return "unknown", "unknown"


def calculate_repo_size(repo_path: str) -> float:
    """
    Calculate total repository size in kilobytes (kB)

    Args:
        repo_path: Path to cloned repository

    Returns:
        Size in kB (kilobytes)
    """
    total_size = 0

    try:
        for dirpath, dirnames, filenames in os.walk(repo_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except OSError:
                    # Skip files that can't be accessed
                    pass

        # Convert bytes to kilobytes
        size_kb = total_size / 1024

        return round(size_kb, 2)

    except Exception as e:
        print(f"Error calculating size: {e}")
        return 0.0


def clone_repository(url: str, destination_folder: str) -> Dict[str, Any]:
    """
    Clone a GitHub repository and gather metadata

    NOW WITH BUNDLED GIT SUPPORT AND ENHANCED ERROR HANDLING!

    Args:
        url: GitHub repository URL (with .git suffix)
        destination_folder: Parent folder where repo will be cloned

    Returns:
        Dictionary with clone results:
        {
            'success': bool,
            'url': str,
            'username': str,
            'repo_name': str,
            'size_kb': float,
            'timestamp': str (DD-MM-YYYY HH:MM:SS),
            'error': str or None,
            'error_type': str or None (for error handling),
            'repo_path': str
        }
    """
    result = {
        'success': False,
        'url': url,
        'username': '',
        'repo_name': '',
        'size_kb': 0.0,
        'timestamp': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        'error': None,
        'error_type': None,
        'repo_path': ''
    }

    try:
        # First, ensure Git is initialized
        git_ok, git_message = ensure_git_initialized()
        if not git_ok:
            result['error'] = git_message
            result['error_type'] = 'git_not_found'
            return result

        # Parse repository info
        username, repo_name = parse_repo_info(url)
        result['username'] = username
        result['repo_name'] = repo_name

        # Create destination path
        repo_folder_name = repo_name.replace('.git', '')
        repo_path = os.path.join(destination_folder, repo_folder_name)
        
        # Check if folder already exists and rename if necessary
        if os.path.exists(repo_path):
            # Generate timestamp for safe filename (no colons)
            timestamp_suffix = datetime.now().strftime("%d-%m-%Y_%H-%M")
            new_folder_name = f"{repo_folder_name}_updated_{timestamp_suffix}"
            repo_path = os.path.join(destination_folder, new_folder_name)
            
            # Update repo_name for the report to indicate renaming
            # We keep the original repo name but append the new folder info
            result['repo_name'] = f"{repo_name} (Saved as: {new_folder_name})"
            repo_folder_name = new_folder_name
            
        result['repo_path'] = repo_path

        # Clone using GitPython
        try:
            from git import Repo
            from git.exc import GitCommandError

            print(f"Cloning {url} to {repo_folder_name}...")

            # Clone with depth=1 for faster cloning (shallow clone)
            Repo.clone_from(url, repo_path, depth=1)

            # Calculate size
            size_kb = calculate_repo_size(repo_path)
            result['size_kb'] = size_kb

            result['success'] = True
            print(f"Successfully cloned {repo_name} ({size_kb} kB)")

        except GitCommandError as git_error:
            error_msg = str(git_error)

            # Categorize the error
            if 'not found' in error_msg.lower() or '404' in error_msg:
                result['error'] = ErrorFormatter.format_error(
                    'repo_not_found',
                    repo_url=url,
                    username=username,
                    repo_name=repo_name
                )
                result['error_type'] = 'repo_not_found'

            elif 'timeout' in error_msg.lower():
                result['error'] = ErrorFormatter.format_error(
                    'network_error',
                    cause='Connection timeout',
                    error=error_msg
                )
                result['error_type'] = 'network_error'

            elif 'permission' in error_msg.lower() or 'denied' in error_msg.lower():
                result['error'] = ErrorFormatter.format_error(
                    'permission_error',
                    path=destination_folder,
                    error=error_msg
                )
                result['error_type'] = 'permission_error'

            else:
                result['error'] = ErrorFormatter.format_error(
                    'clone_failed',
                    repo_url=url,
                    error=error_msg
                )
                result['error_type'] = 'clone_failed'

            print(f"Error: Clone failed - {error_msg}")

            # Clean up partial clone if exists
            if os.path.exists(repo_path):
                try:
                    import shutil
                    shutil.rmtree(repo_path)
                except:
                    pass

        except Exception as git_error:
            error_msg = str(git_error)

            # Generic Git error
            result['error'] = ErrorFormatter.format_error(
                'clone_failed',
                repo_url=url,
                error=error_msg
            )
            result['error_type'] = 'clone_failed'
            print(f"Error: {error_msg}")

            # Clean up partial clone if exists
            if os.path.exists(repo_path):
                try:
                    import shutil
                    shutil.rmtree(repo_path)
                except:
                    pass

    except PermissionError as e:
        result['error'] = ErrorFormatter.format_error(
            'permission_error',
            path=destination_folder,
            error=str(e)
        )
        result['error_type'] = 'permission_error'
        print(f"Error: Permission denied - {str(e)}")

    except OSError as e:
        # Could be disk space, network, etc.
        error_msg = str(e)

        if 'space' in error_msg.lower():
            result['error'] = ErrorFormatter.format_error(
                'disk_space_error',
                required='Unknown',
                available='Check disk space',
                error=error_msg
            )
            result['error_type'] = 'disk_space_error'
        else:
            result['error'] = f"System error: {error_msg}"
            result['error_type'] = 'system_error'

        print(f"Error: {error_msg}")

    except Exception as e:
        result['error'] = f"Unexpected error: {str(e)}"
        result['error_type'] = 'unexpected_error'
        print(f"Error: {result['error']}")

    return result


def clone_repository_with_progress(url: str, destination_folder: str, progress_callback=None) -> Dict[str, Any]:
    """
    Clone repository with progress updates

    Args:
        url: GitHub repository URL
        destination_folder: Destination folder
        progress_callback: Optional callback function(message: str)

    Returns:
        Clone result dictionary
    """
    if progress_callback:
        progress_callback(f"Starting clone: {url}")

    result = clone_repository(url, destination_folder)

    if progress_callback:
        if result['success']:
            progress_callback(f"[OK] Success: {result['repo_name']} ({result['size_kb']} kB)")
        else:
            # Show brief error in progress
            error_brief = result.get('error_type', 'unknown error')
            progress_callback(f"[X] Failed: {result['repo_name']} - {error_brief}")

    return result


def test_git_configuration():
    """
    Test Git configuration and display results

    Returns:
        True if Git is working, False otherwise
    """
    print("=" * 70)
    print("Testing Git Configuration...")
    print("=" * 70)
    print()

    success, message = ensure_git_initialized()

    print(message)
    print()

    if success:
        git_path, source, _ = get_git_executable()
        print(f"Git executable: {git_path}")
        print(f"Git source: {source}")
        print()
        print("[OK] Git is ready for cloning operations!")
        return True
    else:
        print("[ERROR] Git initialization failed!")
        print()
        print("Please fix the issue above before using the application.")
        return False


# Testing
if __name__ == "__main__":
    # Test Git configuration
    test_git_configuration()

    print()
    print("=" * 70)
    print("Testing URL Parser...")
    print("=" * 70)
    print()

    # Test parse_repo_info
    test_urls = [
        "https://github.com/torvalds/linux.git",
        "https://github.com/microsoft/vscode.git",
        "github.com/python/cpython.git"
    ]

    for url in test_urls:
        username, repo_name = parse_repo_info(url)
        print(f"  {url}")
        print(f"    Username: {username}, Repo: {repo_name}")
        print()

    print("=" * 70)
    print("Timestamp Format Test")
    print("=" * 70)
    print(f"Current time: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")