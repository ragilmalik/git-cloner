"""
RagilGitClone - URL Parser Module
Extracts GitHub URLs from multiple file formats

Author: Ragilmalik
"""

import re
import csv
from typing import List, Set
from pathlib import Path


# GitHub URL regex pattern - matches both http and https
GITHUB_URL_PATTERN = r'https?://github\.com/[\w\-\.]+/[/w\-\.]+'


def normalize_url(url: str) -> str:
    """
    Normalize GitHub URL to ensure it ends with .git

    Args:
        url: GitHub repository URL

    Returns:
        Normalized URL with .git suffix

    Examples:
        >>> normalize_url("https://github.com/user/repo")
        'https://github.com/user/repo.git'
        >>> normalize_url("github.com/user/repo")
        'https://github.com/user/repo.git'
    """
    url = url.strip()

    # Add https:// if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    # Remove trailing slash
    url = url.rstrip('/')

    # Add .git if not present
    if not url.endswith('.git'):
        url += '.git'

    return url


def is_valid_github_url(url: str) -> bool:
    """
    Validate if URL is a valid GitHub repository URL

    Args:
        url: URL to validate

    Returns:
        True if valid GitHub URL, False otherwise
    """
    pattern = r'^https?://github\.com/[\w\-\.]+/[/w\-\.]+(\.git)?$' 
    return bool(re.match(pattern, url))


def parse_text_file(filepath: str) -> List[str]:
    """
    Extract GitHub URLs from plain text file

    Args:
        filepath: Path to text file

    Returns:
        List of normalized GitHub URLs
    """
    urls = set()

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find all GitHub URLs
        matches = re.findall(GITHUB_URL_PATTERN, content)
        for match in matches:
            urls.add(normalize_url(match))

    except Exception as e:
        print(f"Error parsing text file: {e}")

    return list(urls)


def parse_csv_file(filepath: str) -> List[str]:
    """
    Extract GitHub URLs from CSV file (all columns)

    Args:
        filepath: Path to CSV file

    Returns:
        List of normalized GitHub URLs
    """
    urls = set()

    try:
        with open(filepath, 'r', encoding='utf-8', newline='') as f:
            # Try to detect delimiter
            sample = f.read(1024)
            f.seek(0)

            sniffer = csv.Sniffer()
            try:
                delimiter = sniffer.sniff(sample).delimiter
            except:
                delimiter = ','

            reader = csv.reader(f, delimiter=delimiter)

            for row in reader:
                for cell in row:
                    # Search for GitHub URLs in each cell
                    matches = re.findall(GITHUB_URL_PATTERN, str(cell))
                    for match in matches:
                        urls.add(normalize_url(match))

    except Exception as e:
        print(f"Error parsing CSV file: {e}")

    return list(urls)


def parse_xlsx_file(filepath: str) -> List[str]:
    """
    Extract GitHub URLs from Excel file (all sheets, all columns)

    Args:
        filepath: Path to Excel file (.xlsx)

    Returns:
        List of normalized GitHub URLs
    """
    urls = set()

    try:
        import pandas as pd

        # Read all sheets
        excel_file = pd.ExcelFile(filepath)

        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(filepath, sheet_name=sheet_name)

            # Iterate through all cells
            for column in df.columns:
                for value in df[column].dropna():
                    # Search for GitHub URLs
                    matches = re.findall(GITHUB_URL_PATTERN, str(value))
                    for match in matches:
                        urls.add(normalize_url(match))

    except Exception as e:
        print(f"Error parsing XLSX file: {e}")

    return list(urls)


def parse_markdown_file(filepath: str) -> List[str]:
    """
    Extract GitHub URLs from Markdown file
    Extracts from both markdown links [text](url) and plain text URLs

    Args:
        filepath: Path to Markdown file

    Returns:
        List of normalized GitHub URLs
    """
    urls = set()

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract URLs from markdown links: [text](url)
        md_link_pattern = r'\[([^\]]+)\]\((' + GITHUB_URL_PATTERN + r')\)'
        md_matches = re.findall(md_link_pattern, content)
        for match in md_matches:
            urls.add(normalize_url(match[1]))

        # Extract plain text URLs
        plain_matches = re.findall(GITHUB_URL_PATTERN, content)
        for match in plain_matches:
            urls.add(normalize_url(match))

    except Exception as e:
        print(f"Error parsing Markdown file: {e}")

    return list(urls)


def extract_urls_from_file(filepath: str) -> List[str]:
    """
    Auto-detect file format and extract GitHub URLs

    Args:
        filepath: Path to file (txt, csv, xlsx, md, etc.)

    Returns:
        List of normalized GitHub URLs
    """
    path = Path(filepath)
    extension = path.suffix.lower()

    # Route to appropriate parser
    if extension in ['.txt', '.log']:
        return parse_text_file(filepath)
    elif extension == '.csv':
        return parse_csv_file(filepath)
    elif extension in ['.xlsx', '.xls']:
        return parse_xlsx_file(filepath)
    elif extension in ['.md', '.markdown']:
        return parse_markdown_file(filepath)
    else:
        # Try as text file for unknown extensions
        return parse_text_file(filepath)


def parse_manual_input(text: str) -> List[str]:
    """
    Parse manually entered URLs from multi-line text

    Args:
        text: Multi-line text with URLs (one per line or space-separated)

    Returns:
        List of normalized GitHub URLs
    """
    urls = []

    # Split by newlines and spaces
    lines = text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if it looks like a GitHub URL
        if 'github.com' in line.lower():
            normalized = normalize_url(line)
            if is_valid_github_url(normalized):
                urls.append(normalized)

    return urls


# Testing
if __name__ == "__main__":
    # Test normalize_url
    test_urls = [
        "https://github.com/user/repo",
        "github.com/user/repo",
        "http://github.com/user/repo.git",
        "https://github.com/user/repo/",
    ]

    print("URL Normalization Tests:")
    for url in test_urls:
        print(f"  {url} -> {normalize_url(url)}")

    print("\nManual Input Test:")
    manual_text = """
    https://github.com/torvalds/linux
    github.com/microsoft/vscode
    https://github.com/python/cpython
    """
    print(parse_manual_input(manual_text))