"""
RagilmalikGitCloner - Error Handler Module
Formats error messages for GUI display

Author: Ragilmalik
"""

class ErrorFormatter:
    """Helper class to format common error messages"""

    @staticmethod
    def format_error(error_type: str, **kwargs) -> str:
        """
        Format error message based on type

        Args:
            error_type: Key for error template
            **kwargs: Variables to fill in template

        Returns:
            Formatted error string
        """
        templates = {
            'git_not_found': (
                "CRITICAL: Git not found!\n"
                "Please ensure 'git_portable' folder exists next to the app.\n"
                "Or install Git for Windows."
            ),
            'folder_exists': (
                "Folder already exists: {folder_name}\n"
                "Location: {folder_path}\n"
                "Skipping to prevent overwrite."
            ),
            'repo_not_found': (
                "Repository not found or private.\n"
                "URL: {repo_url}\n"
                "Check spelling or authentication."
            ),
            'permission_error': (
                "Permission denied!\n"
                "Cannot write to: {path}\n"
                "Details: {error}"
            ),
            'network_error': (
                "Network error during clone.\n"
                "Cause: {cause}\n"
                "Details: {error}"
            ),
            'disk_space_error': (
                "Insufficient disk space!\n"
                "Required: {required}, Available: {available}\n"
                "Details: {error}"
            ),
            'clone_failed': (
                "Clone failed unexpectedly.\n"
                "URL: {repo_url}\n"
                "Error: {error}"
            ),
            'unknown_error': (
                "An unknown error occurred.\n"
                "Details: {error}"
            )
        }

        template = templates.get(error_type, templates['unknown_error'])
        
        try:
            return template.format(**kwargs)
        except KeyError:
            return f"Error formatting message (Type: {error_type}). Raw: {str(kwargs)}"