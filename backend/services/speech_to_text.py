import os
from pathlib import Path
from google.cloud import speech_v1
from google.oauth2 import service_account
from config.settings import settings
import wave
import contextlib

class SpeechToTextService:
    """Google Cloud Speech-to-Text service"""

    def __init__(self):
        """Initialize the Speech-to-Text client"""
        # Set up credentials - resolve path relative to project root
        credentials_path = Path(settings.GCP_CREDENTIALS_PATH)
        
        # If path is relative, make it relative to the project root
        if not credentials_path.is_absolute():
            # Get the project root (3 levels up from this file)
            project_root = Path(__file__).parent.parent.parent
            credentials_path = project_root / credentials_path
        
        if credentials_path.exists():
            # Use service account credentials
            credentials = service_account.Credentials.from_service_account_file(
                str(credentials_path)
            )
            self.client = speech_v1.SpeechClient(credentials=credentials)
        else:
            # Try to use default credentials (if running in GCP)
            try:
                self.client = speech_v1.SpeechClient()
            except Exception as e:
                print(f"Warning: Could not initialize Speech-to-Text client: File {credentials_path} was not found.")
                self.client = None

    def _get_audio_duration(self, audio_file_path: str) -> float:
        """
        Get the duration of an audio file in seconds
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Duration in seconds
        """
        try:
            with contextlib.closing(wave.open(audio_file_path, 'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = frames / float(rate)
                return duration
        except Exception as e:
            print(f"Warning: Could not determine audio duration: {e}")
            # If we can't determine duration, assume it might be long
            return 61.0  # Return >60 to trigger chunking

    def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribe audio file to text
        Automatically handles long audio files by chunking

        Args:
            audio_file_path: Path to the audio file

        Returns:
            Transcribed text
        """
        if not self.client:
            raise Exception("Speech-to-Text client not initialized. Please check GCP credentials.")

        # Check audio duration
        duration = self._get_audio_duration(audio_file_path)
        
        # If audio is longer than 60 seconds, use chunked transcription
        if duration > 60:
            return self._transcribe_long_audio(audio_file_path, duration)
        
        # For short audio, use synchronous recognition
        return self._transcribe_short_audio(audio_file_path)

    def _transcribe_short_audio(self, audio_file_path: str) -> str:
        """
        Transcribe short audio file (< 1 minute) using synchronous recognition
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Transcribed text
        """
        # Read audio file
        with open(audio_file_path, "rb") as audio_file:
            content = audio_file.read()

        audio = speech_v1.RecognitionAudio(content=content)

        # Configure recognition
        config = speech_v1.RecognitionConfig(
            encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True,
            audio_channel_count=1,
            enable_word_time_offsets=False,
        )

        # Try with auto-detect encoding if LINEAR16 fails
        try:
            response = self.client.recognize(config=config, audio=audio)
        except Exception as e:
            # Retry with different encoding
            config.encoding = speech_v1.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED
            response = self.client.recognize(config=config, audio=audio)

        # Combine all transcripts
        transcripts = []
        for result in response.results:
            if result.alternatives:
                transcripts.append(result.alternatives[0].transcript)

        if not transcripts:
            raise Exception("No transcription results found")

        return " ".join(transcripts)

    def _transcribe_long_audio(self, audio_file_path: str, duration: float) -> str:
        """
        Transcribe long audio file by splitting it into chunks
        
        Args:
            audio_file_path: Path to the audio file
            duration: Duration of the audio in seconds
            
        Returns:
            Transcribed text
        """
        import wave
        from pydub import AudioSegment
        import tempfile
        
        # Split audio into 50-second chunks (leaving margin for safety)
        chunk_duration_ms = 50 * 1000  # 50 seconds in milliseconds
        
        # Load audio file
        audio = AudioSegment.from_wav(audio_file_path)
        
        transcripts = []
        
        # Process audio in chunks
        for i, start_ms in enumerate(range(0, len(audio), chunk_duration_ms)):
            end_ms = min(start_ms + chunk_duration_ms, len(audio))
            chunk = audio[start_ms:end_ms]
            
            # Save chunk to temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                chunk_path = temp_file.name
                chunk.export(chunk_path, format='wav')
            
            try:
                # Transcribe chunk
                chunk_transcript = self._transcribe_short_audio(chunk_path)
                transcripts.append(chunk_transcript)
            finally:
                # Clean up temporary file
                os.unlink(chunk_path)
        
        return " ".join(transcripts)

    def transcribe_audio_long(self, audio_file_path: str) -> str:
        """
        Transcribe long audio file using async recognition
        (This method is kept for backward compatibility but now just calls transcribe_audio)

        Args:
            audio_file_path: Path to the audio file

        Returns:
            Transcribed text
        """
        return self.transcribe_audio(audio_file_path)
