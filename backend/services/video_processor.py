import subprocess
import os
from pathlib import Path
from typing import Optional
from config.settings import settings
import uuid

class VideoProcessor:
    """Video processing service for audio extraction"""

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

        except subprocess.CalledProcessError as e:
            error_message = e.stderr.decode() if e.stderr else str(e)
            raise Exception(f"FFmpeg error during audio extraction: {error_message}")
        except Exception as e:
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

        except subprocess.CalledProcessError as e:
            error_message = e.stderr.decode() if e.stderr else str(e)
            raise Exception(f"FFmpeg error during audio conversion: {error_message}")
        except Exception as e:
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
