import subprocess
import os
import shutil
from pathlib import Path
from typing import Optional
from config.settings import settings
import uuid

class VideoProcessor:
    """Video processing service for audio extraction"""

    @staticmethod
    def check_ffmpeg_installed() -> bool:
        """
        Check if FFmpeg is installed and available in PATH

        Returns:
            True if FFmpeg is available, False otherwise
        """
        return shutil.which("ffmpeg") is not None

    @staticmethod
    def get_ffmpeg_install_message() -> str:
        """
        Get platform-specific FFmpeg installation instructions

        Returns:
            Installation instructions as a string
        """
        import platform
        system = platform.system()

        if system == "Windows":
            return (
                "FFmpeg is not installed or not in your system PATH.\n\n"
                "To install FFmpeg on Windows:\n"
                "1. Download FFmpeg from https://www.gyan.dev/ffmpeg/builds/\n"
                "2. Extract the ZIP file to a folder (e.g., C:\\ffmpeg)\n"
                "3. Add the 'bin' folder to your system PATH:\n"
                "   - Open 'Environment Variables' from System Properties\n"
                "   - Edit the 'Path' variable under System Variables\n"
                "   - Add the path to FFmpeg's bin folder (e.g., C:\\ffmpeg\\bin)\n"
                "4. Restart your terminal/IDE and try again\n\n"
                "Alternative: Install via Chocolatey: choco install ffmpeg"
            )
        elif system == "Darwin":  # macOS
            return (
                "FFmpeg is not installed.\n\n"
                "To install FFmpeg on macOS:\n"
                "1. Install Homebrew if you haven't: https://brew.sh/\n"
                "2. Run: brew install ffmpeg"
            )
        else:  # Linux
            return (
                "FFmpeg is not installed.\n\n"
                "To install FFmpeg on Linux:\n"
                "Ubuntu/Debian: sudo apt-get install ffmpeg\n"
                "Fedora: sudo dnf install ffmpeg\n"
                "Arch: sudo pacman -S ffmpeg"
            )

    @staticmethod
    def extract_audio_from_video(video_path: str, output_format: str = "wav") -> str:
        """
        Extract audio from video file using ffmpeg

        Args:
            video_path: Path to the video file
            output_format: Output audio format (default: wav)

        Returns:
            Path to the extracted audio file
        """
        # Generate unique output filename
        video_file = Path(video_path)
        output_filename = f"{video_file.stem}_{uuid.uuid4().hex[:8]}.{output_format}"
        output_path = settings.TEMP_FOLDER / output_filename

        try:
            # Check if FFmpeg is installed
            if not VideoProcessor.check_ffmpeg_installed():
                raise FileNotFoundError(VideoProcessor.get_ffmpeg_install_message())

            # Use ffmpeg to extract audio
            # -i: input file
            # -vn: disable video
            # -acodec: audio codec (pcm_s16le for WAV)
            # -ar: audio sample rate (16000 Hz for Speech-to-Text)
            # -ac: audio channels (1 for mono)
            # -y: overwrite output file if exists

            if output_format.lower() == "wav":
                # Extract as WAV with specific parameters for Speech-to-Text
                command = [
                    "ffmpeg",
                    "-i", str(video_path),
                    "-vn",  # No video
                    "-acodec", "pcm_s16le",  # PCM 16-bit little-endian
                    "-ar", "16000",  # 16kHz sample rate
                    "-ac", "1",  # Mono
                    "-y",  # Overwrite
                    str(output_path)
                ]
            else:
                # Extract with default settings
                command = [
                    "ffmpeg",
                    "-i", str(video_path),
                    "-vn",
                    "-acodec", "copy",
                    "-y",
                    str(output_path)
                ]

            # Run ffmpeg command
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )

            if not output_path.exists():
                raise Exception("Audio extraction failed: output file not created")

            return str(output_path)

        except FileNotFoundError as e:
            # FFmpeg not installed
            raise Exception(str(e))
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.decode() if e.stderr else str(e)
            raise Exception(f"FFmpeg error during audio extraction: {error_message}")
        except Exception as e:
            # Check if it's a "file not found" error (Windows or other OS)
            if "WinError 2" in str(e) or "No such file or directory" in str(e):
                raise Exception(VideoProcessor.get_ffmpeg_install_message())
            raise Exception(f"Error extracting audio from video: {str(e)}")

    @staticmethod
    def convert_audio_format(
        audio_path: str,
        output_format: str = "wav",
        sample_rate: int = 16000,
        channels: int = 1
    ) -> str:
        """
        Convert audio to a different format

        Args:
            audio_path: Path to the input audio file
            output_format: Output format (default: wav)
            sample_rate: Sample rate in Hz (default: 16000)
            channels: Number of channels (default: 1 for mono)

        Returns:
            Path to the converted audio file
        """
        audio_file = Path(audio_path)
        output_filename = f"{audio_file.stem}_converted_{uuid.uuid4().hex[:8]}.{output_format}"
        output_path = settings.TEMP_FOLDER / output_filename

        try:
            # Check if FFmpeg is installed
            if not VideoProcessor.check_ffmpeg_installed():
                raise FileNotFoundError(VideoProcessor.get_ffmpeg_install_message())

            command = [
                "ffmpeg",
                "-i", str(audio_path),
                "-acodec", "pcm_s16le",
                "-ar", str(sample_rate),
                "-ac", str(channels),
                "-y",
                str(output_path)
            ]

            subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )

            if not output_path.exists():
                raise Exception("Audio conversion failed: output file not created")

            return str(output_path)

        except FileNotFoundError as e:
            # FFmpeg not installed
            raise Exception(str(e))
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.decode() if e.stderr else str(e)
            raise Exception(f"FFmpeg error during audio conversion: {error_message}")
        except Exception as e:
            # Check if it's a "file not found" error (Windows or other OS)
            if "WinError 2" in str(e) or "No such file or directory" in str(e):
                raise Exception(VideoProcessor.get_ffmpeg_install_message())
            raise Exception(f"Error converting audio format: {str(e)}")

    @staticmethod
    def cleanup_temp_file(file_path: str):
        """
        Delete temporary file

        Args:
            file_path: Path to the file to delete
        """
        try:
            file = Path(file_path)
            if file.exists():
                file.unlink()
        except Exception as e:
            print(f"Warning: Could not delete temp file {file_path}: {e}")

    @staticmethod
    def get_video_info(video_path: str) -> dict:
        """
        Get video file information using ffprobe

        Args:
            video_path: Path to the video file

        Returns:
            Dictionary with video information
        """
        try:
            command = [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                str(video_path)
            ]

            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )

            import json
            info = json.loads(result.stdout.decode())
            return info

        except Exception as e:
            print(f"Error getting video info: {e}")
            return {}
