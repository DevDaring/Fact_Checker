from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials
from typing import List
from models.fact_check import FactCheckResponse
from services.database import Database
from middleware.auth_middleware import AuthMiddleware, security
from utils.helpers import Helpers

router = APIRouter(prefix="/api/history", tags=["History"])

@router.get("/user")
async def get_user_history(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get current user's fact-check history

    Args:
        credentials: JWT token

    Returns:
        List of fact-checks
    """
    # Verify authentication
    user = await AuthMiddleware.verify_token(credentials)

    try:
        fact_checks = Database.get_user_fact_checks(user["user_id"])

        # Get comments for each fact check
        for fact_check in fact_checks:
            comments = Database.get_comments_by_fact_check(fact_check["fact_check_id"])

            # Add admin email to comments
            for comment in comments:
                admin = Database.get_user_by_id(comment["admin_id"])
                comment["admin_email"] = admin["email"] if admin else "Unknown"

            fact_check["admin_comments"] = comments

        return Helpers.create_response(
            success=True,
            data=fact_checks
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving history: {str(e)}"
        )

@router.get("/details/{fact_check_id}")
async def get_fact_check_details(
    fact_check_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get detailed information for a specific fact-check

    Args:
        fact_check_id: Fact check ID
        credentials: JWT token

    Returns:
        Detailed fact-check information
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

    # Get comments
    comments = Database.get_comments_by_fact_check(fact_check_id)

    # Add admin email to comments
    for comment in comments:
        admin = Database.get_user_by_id(comment["admin_id"])
        comment["admin_email"] = admin["email"] if admin else "Unknown"

    fact_check["admin_comments"] = comments

    return Helpers.create_response(
        success=True,
        data=fact_check
    )

@router.get("/user/{user_id}")
async def get_specific_user_history(
    user_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get fact-check history for a specific user (admin only)

    Args:
        user_id: User ID
        credentials: JWT token

    Returns:
        List of fact-checks
    """
    # Verify admin authentication
    admin = await AuthMiddleware.verify_admin(credentials)

    try:
        fact_checks = Database.get_user_fact_checks(user_id)

        # Get comments for each fact check
        for fact_check in fact_checks:
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
            detail=f"Error retrieving history: {str(e)}"
        )
