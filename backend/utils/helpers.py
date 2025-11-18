from datetime import datetime
from typing import Any, Dict
import json

class Helpers:
    """General helper functions"""

    @staticmethod
    def format_timestamp(timestamp: datetime) -> str:
        """
        Format datetime to string

        Args:
            timestamp: Datetime object

        Returns:
            Formatted timestamp string
        """
        if isinstance(timestamp, str):
            return timestamp
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def parse_timestamp(timestamp_str: str) -> datetime:
        """
        Parse timestamp string to datetime

        Args:
            timestamp_str: Timestamp string

        Returns:
            Datetime object
        """
        try:
            return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        except:
            return datetime.now()

    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """
        Format file size in bytes to human-readable format

        Args:
            size_bytes: Size in bytes

        Returns:
            Formatted size string
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

    @staticmethod
    def safe_json_loads(json_str: str, default: Any = None) -> Any:
        """
        Safely parse JSON string

        Args:
            json_str: JSON string
            default: Default value if parsing fails

        Returns:
            Parsed JSON or default value
        """
        try:
            return json.loads(json_str)
        except:
            return default if default is not None else {}

    @staticmethod
    def safe_json_dumps(obj: Any, default: str = "{}") -> str:
        """
        Safely convert object to JSON string

        Args:
            obj: Object to convert
            default: Default value if conversion fails

        Returns:
            JSON string
        """
        try:
            return json.dumps(obj)
        except:
            return default

    @staticmethod
    def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
        """
        Truncate text to maximum length

        Args:
            text: Text to truncate
            max_length: Maximum length
            suffix: Suffix to add when truncated

        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix

    @staticmethod
    def remove_duplicates(items: list) -> list:
        """
        Remove duplicates from list while preserving order

        Args:
            items: List of items

        Returns:
            List without duplicates
        """
        seen = set()
        result = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result

    @staticmethod
    def create_response(
        success: bool,
        message: str = "",
        data: Any = None,
        error: str = None
    ) -> Dict:
        """
        Create standardized API response

        Args:
            success: Success status
            message: Response message
            data: Response data
            error: Error message

        Returns:
            Response dictionary
        """
        response = {
            "success": success,
            "message": message
        }

        if data is not None:
            response["data"] = data

        if error is not None:
            response["error"] = error

        return response
