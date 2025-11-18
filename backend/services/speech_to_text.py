import os
from pathlib import Path
from google.cloud import speech_v1
from google.oauth2 import service_account
from config.settings import settings

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

    def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribe audio file to text

        Args:
            audio_file_path: Path to the audio file

        Returns:
            Transcribed text
        """
        if not self.client:
            raise Exception("Speech-to-Text client not initialized. Please check GCP credentials.")

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

    def transcribe_audio_long(self, audio_file_path: str) -> str:
        """
        Transcribe long audio file using async recognition

        Args:
            audio_file_path: Path to the audio file

        Returns:
            Transcribed text
        """
        if not self.client:
            raise Exception("Speech-to-Text client not initialized. Please check GCP credentials.")

        # For files longer than 1 minute, use long-running recognition
        # This would require uploading to Google Cloud Storage
        # For now, we'll use the synchronous method with chunking if needed

        return self.transcribe_audio(audio_file_path)
