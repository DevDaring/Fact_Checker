from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials
from typing import List
from models.comment import CommentCreate, CommentResponse
from services.database import Database
from middleware.auth_middleware import AuthMiddleware, security
from utils.helpers import Helpers

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get("/users")
async def get_all_users(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get all users (admin only)

    Args:
        credentials: JWT token

    Returns:
        List of all users
    """
    # Verify admin authentication
    admin = await AuthMiddleware.verify_admin(credentials)

    try:
        users = Database.get_all_users()

        # Remove password hashes
        for user in users:
            user.pop("password_hash", None)

        return Helpers.create_response(
            success=True,
            data=users
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving users: {str(e)}"
        )

@router.get("/fact-checks")
async def get_all_fact_checks(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get all fact-checks (admin only)

    Args:
        credentials: JWT token

    Returns:
        List of all fact-checks
    """
    # Verify admin authentication
    admin = await AuthMiddleware.verify_admin(credentials)

    try:
        fact_checks = Database.get_all_fact_checks()

        # Add user email to each fact check
        for fact_check in fact_checks:
            user = Database.get_user_by_id(fact_check["user_id"])
            fact_check["user_email"] = user["email"] if user else "Unknown"

            # Get comments for this fact check
            comments = Database.get_comments_by_fact_check(fact_check["fact_check_id"])
            fact_check["comments_count"] = len(comments)

        return Helpers.create_response(
            success=True,
            data=fact_checks
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving fact checks: {str(e)}"
        )

@router.get("/user-checks/{user_id}")
async def get_user_fact_checks(
    user_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get fact-checks for a specific user (admin only)

    Args:
        user_id: User ID
        credentials: JWT token

    Returns:
        List of user's fact-checks
    """
    # Verify admin authentication
    admin = await AuthMiddleware.verify_admin(credentials)

    try:
        fact_checks = Database.get_user_fact_checks(user_id)

        # Get user info
        user = Database.get_user_by_id(user_id)
        user_email = user["email"] if user else "Unknown"

        # Add comments for each fact check
        for fact_check in fact_checks:
            fact_check["user_email"] = user_email
            comments = Database.get_comments_by_fact_check(fact_check["fact_check_id"])

            # Add admin email to comments
            for comment in comments:
                admin_user = Database.get_user_by_id(comment["admin_id"])
                comment["admin_email"] = admin_user["email"] if admin_user else "Unknown"

            fact_check["admin_comments"] = comments

        return Helpers.create_response(
            success=True,
            data=fact_checks
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user fact checks: {str(e)}"
        )

@router.post("/comment", response_model=CommentResponse)
async def add_comment(
    comment_data: dict,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Add comment to a fact-check (admin only)

    Args:
        comment_data: Comment text and fact_check_id
        credentials: JWT token

    Returns:
        Created comment
    """
    # Verify admin authentication
    admin = await AuthMiddleware.verify_admin(credentials)

    fact_check_id = comment_data.get("fact_check_id")
    comment_text = comment_data.get("comment_text")

    if not fact_check_id or not comment_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="fact_check_id and comment_text are required"
        )

    # Check if fact check exists
    fact_check = Database.get_fact_check_by_id(fact_check_id)
    if not fact_check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fact check not found"
        )

    try:
        # Create comment
        comment = Database.create_comment(
            fact_check_id=fact_check_id,
            admin_id=admin["user_id"],
            comment_text=comment_text
        )

        return CommentResponse(
            comment_id=comment["comment_id"],
            fact_check_id=comment["fact_check_id"],
            admin_id=comment["admin_id"],
            admin_email=admin["email"],
            comment_text=comment["comment_text"],
            timestamp=comment["timestamp"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding comment: {str(e)}"
        )

@router.get("/comments/{fact_check_id}")
async def get_comments(
    fact_check_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get comments for a fact-check

    Args:
        fact_check_id: Fact check ID
        credentials: JWT token

    Returns:
        List of comments
    """
    # Verify authentication (user can view their own, admin can view all)
    user = await AuthMiddleware.verify_token(credentials)

    # Check if fact check exists and user has access
    fact_check = Database.get_fact_check_by_id(fact_check_id)
    if not fact_check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fact check not found"
        )

    # Check access
    if fact_check["user_id"] != user["user_id"] and user["role"] != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    try:
        comments = Database.get_comments_by_fact_check(fact_check_id)

        # Add admin email to comments
        for comment in comments:
            admin = Database.get_user_by_id(comment["admin_id"])
            comment["admin_email"] = admin["email"] if admin else "Unknown"

        return Helpers.create_response(
            success=True,
            data=comments
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving comments: {str(e)}"
        )
