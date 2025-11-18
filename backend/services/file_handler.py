import os
import uuid
from pathlib import Path
from typing import Tuple, Optional
from fastapi import UploadFile
from backend.config.settings import settings

class FileHandler:
    """File upload and management service"""

    @staticmethod
    def validate_file_size(file: UploadFile) -> bool:
        """
        Validate file size

        Args:
            file: Uploaded file

        Returns:
            True if file size is valid
        """
        # Check file size (if available)
        if hasattr(file, 'size') and file.size:
            if file.size > settings.MAX_FILE_SIZE_BYTES:
                return False
        return True

    @staticmethod
    def validate_file_extension(filename: str, upload_type: str) -> bool:
        """
        Validate file extension

        Args:
            filename: Name of the file
            upload_type: Type of upload (video, audio, image)

        Returns:
            True if extension is valid
        """
        ext = Path(filename).suffix.lower()

        if upload_type == "video":
            return ext in settings.ALLOWED_VIDEO_EXTENSIONS
        elif upload_type == "audio":
            return ext in settings.ALLOWED_AUDIO_EXTENSIONS
        elif upload_type == "image":
            return ext in settings.ALLOWED_IMAGE_EXTENSIONS

        return False

    @staticmethod
    def generate_unique_filename(original_filename: str, user_id: int) -> str:
        """
        Generate unique filename

        Args:
            original_filename: Original filename
            user_id: User ID

        Returns:
            Unique filename
        """
        ext = Path(original_filename).suffix
        unique_id = uuid.uuid4().hex[:12]
        timestamp = uuid.uuid1().time
        return f"{user_id}_{timestamp}_{unique_id}{ext}"

    @staticmethod
    async def save_upload_file(
        file: UploadFile,
        upload_type: str,
        user_id: int
    ) -> Tuple[str, str]:
        """
        Save uploaded file

        Args:
            file: Uploaded file
            upload_type: Type of upload (video, audio, image)
            user_id: User ID

        Returns:
            Tuple of (file_id, file_path)
        """
        # Validate file size
        if not FileHandler.validate_file_size(file):
            raise ValueError(f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB}MB")

        # Validate file extension
        if not FileHandler.validate_file_extension(file.filename, upload_type):
            raise ValueError(f"Invalid file extension for {upload_type} upload")

        # Determine upload folder
        if upload_type == "video":
            upload_folder = settings.VIDEO_UPLOAD_FOLDER
        elif upload_type == "audio":
            upload_folder = settings.AUDIO_UPLOAD_FOLDER
        elif upload_type == "image":
            upload_folder = settings.IMAGE_UPLOAD_FOLDER
        else:
            raise ValueError(f"Invalid upload type: {upload_type}")

        # Generate unique filename
        filename = FileHandler.generate_unique_filename(file.filename, user_id)
        file_path = upload_folder / filename

        # Save file
        try:
            contents = await file.read()
            with open(file_path, "wb") as f:
                f.write(contents)
        except Exception as e:
            raise Exception(f"Error saving file: {str(e)}")

        # Generate file ID
        file_id = f"{upload_type}_{Path(filename).stem}"

        return file_id, str(file_path)

    @staticmethod
    def delete_file(file_path: str) -> bool:
        """
        Delete a file

        Args:
            file_path: Path to the file

        Returns:
            True if successful
        """
        try:
            file = Path(file_path)
            if file.exists():
                file.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
            return False

    @staticmethod
    def get_file_info(file_path: str) -> dict:
        """
        Get file information

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with file information
        """
        try:
            file = Path(file_path)
            if not file.exists():
                return {}

            stat = file.stat()
            return {
                "filename": file.name,
                "size": stat.st_size,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "created": stat.st_ctime,
                "modified": stat.st_mtime,
                "extension": file.suffix
            }
        except Exception as e:
            print(f"Error getting file info: {e}")
            return {}

    @staticmethod
    def cleanup_old_temp_files(max_age_hours: int = 24):
        """
        Clean up old temporary files

        Args:
            max_age_hours: Maximum age in hours
        """
        import time
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600

        try:
            temp_folder = settings.TEMP_FOLDER
            for file in temp_folder.iterdir():
                if file.is_file():
                    file_age = current_time - file.stat().st_mtime
                    if file_age > max_age_seconds:
                        file.unlink()
                        print(f"Deleted old temp file: {file.name}")
        except Exception as e:
            print(f"Error cleaning up temp files: {e}")
