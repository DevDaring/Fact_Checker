import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in the root directory
ROOT_DIR = Path(__file__).parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

class Settings:
    """Application settings loaded from environment variables"""

    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # Google Cloud Platform
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "")
    GCP_CREDENTIALS_PATH: str = os.getenv("GCP_CREDENTIALS_PATH", "./gcp-credentials.json")

    # JWT Configuration
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

    # Server Configuration
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    FRONTEND_PORT: int = int(os.getenv("FRONTEND_PORT", "5173"))

    # CORS Configuration
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

    # File Upload Configuration
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
    MAX_FILE_SIZE_BYTES: int = MAX_FILE_SIZE_MB * 1024 * 1024

    ALLOWED_VIDEO_EXTENSIONS: list = os.getenv(
        "ALLOWED_VIDEO_EXTENSIONS",
        ".mp4,.avi,.mov,.mkv,.flv,.wmv"
    ).split(",")

    ALLOWED_AUDIO_EXTENSIONS: list = os.getenv(
        "ALLOWED_AUDIO_EXTENSIONS",
        ".mp3,.wav,.flac,.m4a,.aac,.ogg"
    ).split(",")

    ALLOWED_IMAGE_EXTENSIONS: list = os.getenv(
        "ALLOWED_IMAGE_EXTENSIONS",
        ".jpg,.jpeg,.png,.gif,.bmp,.webp"
    ).split(",")

    # Database Configuration (CSV-based)
    DATA_FOLDER: Path = ROOT_DIR / os.getenv("DATA_FOLDER", "./Data")
    UPLOAD_FOLDER: Path = ROOT_DIR / os.getenv("UPLOAD_FOLDER", "./Data/uploads")
    TEMP_FOLDER: Path = ROOT_DIR / os.getenv("TEMP_FOLDER", "./Data/temp")

    # CSV File Paths
    USERS_CSV: Path = DATA_FOLDER / "users.csv"
    FACT_CHECKS_CSV: Path = DATA_FOLDER / "fact_checks.csv"
    ADMIN_COMMENTS_CSV: Path = DATA_FOLDER / "admin_comments.csv"

    # Upload subdirectories
    VIDEO_UPLOAD_FOLDER: Path = UPLOAD_FOLDER / "videos"
    AUDIO_UPLOAD_FOLDER: Path = UPLOAD_FOLDER / "audio"
    IMAGE_UPLOAD_FOLDER: Path = UPLOAD_FOLDER / "images"

    # Ensure all directories exist
    @classmethod
    def initialize_directories(cls):
        """Create necessary directories if they don't exist"""
        directories = [
            cls.DATA_FOLDER,
            cls.UPLOAD_FOLDER,
            cls.TEMP_FOLDER,
            cls.VIDEO_UPLOAD_FOLDER,
            cls.AUDIO_UPLOAD_FOLDER,
            cls.IMAGE_UPLOAD_FOLDER,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

# Create settings instance
settings = Settings()

# Initialize directories on import
settings.initialize_directories()
