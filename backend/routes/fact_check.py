from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials
from backend.models.fact_check import FactCheckProcess, FactCheckResult
from backend.services.database import Database
from backend.services.speech_to_text import SpeechToTextService
from backend.services.gemini_service import GeminiService
from backend.services.video_processor import VideoProcessor
from backend.middleware.auth_middleware import AuthMiddleware, security
from backend.utils.helpers import Helpers
from pathlib import Path

router = APIRouter(prefix="/api/fact-check", tags=["Fact Checking"])

@router.post("/process", response_model=FactCheckResult)
async def process_fact_check(
    data: dict,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Process fact-check for uploaded file

    Args:
        data: File path and upload type
        credentials: JWT token

    Returns:
        Fact-check result with citations
    """
    # Verify authentication
    user = await AuthMiddleware.verify_token(credentials)

    file_path = data.get("file_path")
    upload_type = data.get("upload_type")

    if not file_path or not upload_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="file_path and upload_type are required"
        )

    try:
        extracted_text = None
        gemini_response = None
        citations = []

        # Initialize services
        speech_service = SpeechToTextService()
        gemini_service = GeminiService()

        # Process based on upload type
        if upload_type == "video":
            # Extract audio from video
            audio_path = VideoProcessor.extract_audio_from_video(file_path)

            # Transcribe audio
            extracted_text = speech_service.transcribe_audio(audio_path)

            # Clean up temporary audio file
            VideoProcessor.cleanup_temp_file(audio_path)

            # Fact-check the transcribed text
            result = gemini_service.fact_check_text(extracted_text)
            gemini_response = result["response"]
            citations = result["citations"]

        elif upload_type == "audio":
            # Convert audio to proper format if needed
            converted_audio = VideoProcessor.convert_audio_format(file_path)

            # Transcribe audio
            extracted_text = speech_service.transcribe_audio(converted_audio)

            # Clean up temporary file
            VideoProcessor.cleanup_temp_file(converted_audio)

            # Fact-check the transcribed text
            result = gemini_service.fact_check_text(extracted_text)
            gemini_response = result["response"]
            citations = result["citations"]

        elif upload_type == "image":
            # Fact-check image directly
            result = gemini_service.fact_check_image(file_path)
            gemini_response = result["response"]
            citations = result["citations"]
            extracted_text = None

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid upload type"
            )

        # Save fact-check to database
        fact_check = Database.create_fact_check(
            user_id=user["user_id"],
            upload_type=upload_type,
            file_path=file_path,
            extracted_text=extracted_text,
            gemini_response=gemini_response,
            citations=citations
        )

        return FactCheckResult(
            fact_check_id=fact_check["fact_check_id"],
            extracted_text=extracted_text,
            gemini_response=gemini_response,
            citations=citations,
            timestamp=fact_check["timestamp"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing fact-check: {str(e)}"
        )

@router.get("/result/{fact_check_id}")
async def get_fact_check_result(
    fact_check_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get fact-check result by ID

    Args:
        fact_check_id: Fact check ID
        credentials: JWT token

    Returns:
        Fact-check result
    """
    # Verify authentication
    user = await AuthMiddleware.verify_token(credentials)

    fact_check = Database.get_fact_check_by_id(fact_check_id)

    if not fact_check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fact check not found"
        )

    # Check if user owns this fact check or is admin
    if fact_check["user_id"] != user["user_id"] and user["role"] != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return Helpers.create_response(
        success=True,
        data=fact_check
    )
