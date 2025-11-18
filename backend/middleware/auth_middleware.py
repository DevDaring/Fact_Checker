from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict
from backend.services.auth_service import AuthService

security = HTTPBearer()

class AuthMiddleware:
    """Authentication middleware for protected routes"""

    @staticmethod
    async def verify_token(credentials: HTTPAuthorizationCredentials) -> Dict:
        """
        Verify JWT token and return user

        Args:
            credentials: HTTP authorization credentials

        Returns:
            User dictionary

        Raises:
            HTTPException: If token is invalid or expired
        """
        token = credentials.credentials

        user = AuthService.get_current_user(token)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    @staticmethod
    async def verify_admin(credentials: HTTPAuthorizationCredentials) -> Dict:
        """
        Verify JWT token and check if user is admin

        Args:
            credentials: HTTP authorization credentials

        Returns:
            Admin user dictionary

        Raises:
            HTTPException: If token is invalid, expired, or user is not admin
        """
        user = await AuthMiddleware.verify_token(credentials)

        if not AuthService.verify_admin(user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required",
            )

        return user

    @staticmethod
    def get_token_from_header(authorization: Optional[str]) -> Optional[str]:
        """
        Extract token from Authorization header

        Args:
            authorization: Authorization header value

        Returns:
            Token string or None
        """
        if not authorization:
            return None

        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None

        return parts[1]
