from fastapi import APIRouter, HTTPException, status, Depends
from models.user import UserLogin, UserCreate, TokenResponse, UserResponse
from services.auth_service import AuthService
from utils.validators import Validators
from utils.helpers import Helpers

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin):
    """
    User/Admin login endpoint

    Args:
        user_data: Login credentials (email, password, role)

    Returns:
        JWT token and user information
    """
    # Validate email
    if not Validators.validate_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Validate role
    if not Validators.validate_role(user_data.role):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Must be 'User' or 'Admin'"
        )

    # Authenticate user
    user = AuthService.authenticate_user(
        user_data.email,
        user_data.password,
        user_data.role
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email, password, or role"
        )

    # Create access token
    access_token = AuthService.create_access_token(
        data={"user_id": user["user_id"], "email": user["email"], "role": user["role"]}
    )

    # Prepare user response
    user_response = UserResponse(
        user_id=user["user_id"],
        email=user["email"],
        role=user["role"],
        created_at=user["created_at"],
        last_login=user["last_login"]
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    """
    User registration endpoint

    Args:
        user_data: Registration data (email, password, role)

    Returns:
        Created user information
    """
    # Validate email
    if not Validators.validate_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Validate password
    is_valid, error_message = Validators.validate_password(user_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message
        )

    # Validate role
    if not Validators.validate_role(user_data.role):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Must be 'User' or 'Admin'"
        )

    try:
        # Register user
        user = AuthService.register_user(
            user_data.email,
            user_data.password,
            user_data.role
        )

        return UserResponse(
            user_id=user["user_id"],
            email=user["email"],
            role=user["role"],
            created_at=user["created_at"],
            last_login=user["last_login"]
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/logout")
async def logout():
    """
    Logout endpoint (client-side token removal)

    Returns:
        Success message
    """
    return Helpers.create_response(
        success=True,
        message="Logged out successfully"
    )
