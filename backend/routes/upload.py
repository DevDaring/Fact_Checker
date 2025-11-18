from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials
from services.file_handler import FileHandler
from middleware.auth_middleware import AuthMiddleware, security
from utils.helpers import Helpers

router = APIRouter(prefix="/api/upload", tags=["File Upload"])

@router.post("/video")
async def upload_video(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Upload video file

    Args:
        file: Video file
        credentials: JWT token

    Returns:
        File ID and path
    """
    # Verify authentication
    user = await AuthMiddleware.verify_token(credentials)

    try:
        # Save file
        file_id, file_path = await FileHandler.save_upload_file(
            file=file,
            upload_type="video",
            user_id=user["user_id"]
        )

        return Helpers.create_response(
            success=True,
            message="Video uploaded successfully",
            data={
                "file_id": file_id,
                "file_path": file_path,
                "upload_type": "video"
            }
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading video: {str(e)}"
        )

@router.post("/audio")
async def upload_audio(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Upload audio file

    Args:
        file: Audio file
        credentials: JWT token

    Returns:
        File ID and path
    """
    # Verify authentication
    user = await AuthMiddleware.verify_token(credentials)

    try:
        # Save file
        file_id, file_path = await FileHandler.save_upload_file(
            file=file,
            upload_type="audio",
            user_id=user["user_id"]
        )

        return Helpers.create_response(
            success=True,
            message="Audio uploaded successfully",
            data={
                "file_id": file_id,
                "file_path": file_path,
                "upload_type": "audio"
            }
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading audio: {str(e)}"
        )

@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Upload image file

    Args:
        file: Image file
        credentials: JWT token

    Returns:
        File ID and path
    """
    # Verify authentication
    user = await AuthMiddleware.verify_token(credentials)

    try:
        # Save file
        file_id, file_path = await FileHandler.save_upload_file(
            file=file,
            upload_type="image",
            user_id=user["user_id"]
        )

        return Helpers.create_response(
            success=True,
            message="Image uploaded successfully",
            data={
                "file_id": file_id,
                "file_path": file_path,
                "upload_type": "image"
            }
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading image: {str(e)}"
        )
