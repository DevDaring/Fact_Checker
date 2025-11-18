import re
from typing import Optional

class Validators:
    """Input validation utilities"""

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format

        Args:
            email: Email address to validate

        Returns:
            True if email is valid
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))

    @staticmethod
    def validate_password(password: str) -> tuple[bool, Optional[str]]:
        """
        Validate password strength

        Args:
            password: Password to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"

        if len(password) > 128:
            return False, "Password must be less than 128 characters"

        # Optional: Add more password strength requirements
        # if not re.search(r'[A-Z]', password):
        #     return False, "Password must contain at least one uppercase letter"

        # if not re.search(r'[a-z]', password):
        #     return False, "Password must contain at least one lowercase letter"

        # if not re.search(r'[0-9]', password):
        #     return False, "Password must contain at least one digit"

        return True, None

    @staticmethod
    def validate_role(role: str) -> bool:
        """
        Validate user role

        Args:
            role: Role to validate

        Returns:
            True if role is valid
        """
        return role in ["User", "Admin"]

    @staticmethod
    def validate_upload_type(upload_type: str) -> bool:
        """
        Validate upload type

        Args:
            upload_type: Upload type to validate

        Returns:
            True if upload type is valid
        """
        return upload_type in ["video", "audio", "image"]

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename to prevent directory traversal

        Args:
            filename: Filename to sanitize

        Returns:
            Sanitized filename
        """
        # Remove directory separators and parent references
        filename = filename.replace('/', '').replace('\\', '')
        filename = filename.replace('..', '')

        # Remove any non-alphanumeric characters except dots, dashes, and underscores
        filename = re.sub(r'[^\w\-.]', '_', filename)

        return filename

    @staticmethod
    def validate_text_length(text: str, min_length: int = 1, max_length: int = 10000) -> tuple[bool, Optional[str]]:
        """
        Validate text length

        Args:
            text: Text to validate
            min_length: Minimum length
            max_length: Maximum length

        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(text) < min_length:
            return False, f"Text must be at least {min_length} characters"

        if len(text) > max_length:
            return False, f"Text must be less than {max_length} characters"

        return True, None
