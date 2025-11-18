from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
from passlib.context import CryptContext
from backend.config.settings import settings
from backend.services.database import Database

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """Authentication and authorization service"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str) -> Optional[Dict]:
        """Decode and verify JWT token"""
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            return payload
        except JWTError:
            return None

    @staticmethod
    def authenticate_user(email: str, password: str, role: str) -> Optional[Dict]:
        """Authenticate a user"""
        # Get user from database
        user = Database.get_user_by_email(email)

        if not user:
            return None

        # Verify password
        if not AuthService.verify_password(password, user['password_hash']):
            return None

        # Verify role matches
        if user['role'] != role:
            return None

        # Update last login
        Database.update_last_login(user['user_id'])

        return user

    @staticmethod
    def register_user(email: str, password: str, role: str) -> Dict:
        """Register a new user"""
        # Check if user already exists
        existing_user = Database.get_user_by_email(email)
        if existing_user:
            raise ValueError("User with this email already exists")

        # Hash password
        password_hash = AuthService.hash_password(password)

        # Create user
        user = Database.create_user(email, password_hash, role)

        return user

    @staticmethod
    def get_current_user(token: str) -> Optional[Dict]:
        """Get current user from token"""
        payload = AuthService.decode_access_token(token)

        if not payload:
            return None

        user_id = payload.get("user_id")
        if not user_id:
            return None

        user = Database.get_user_by_id(user_id)
        return user

    @staticmethod
    def verify_admin(user: Dict) -> bool:
        """Verify if user is admin"""
        return user.get('role') == 'Admin'
