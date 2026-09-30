"""
Authentication & Role-Based Access Control (RBAC) router and dependencies.

Supports 4 roles:
- Admin (Chief Officer / System Admin)
- Engineer (PWD / Maintenance Engineer)
- Police (Jaipur Traffic Police / Law Enforcement)
- Viewer (Public Citizen / Read-only Auditor)
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status

from backend.analytics.store import DEFAULT_USERS, store
from backend.schemas import AuthResponse, LoginRequest, User, UserRole

router = APIRouter(prefix="/auth", tags=["auth"])


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    x_user_role: Annotated[str | None, Header(alias="x-user-role")] = None,
) -> User:
    """Extract user from bearer token or explicit x-user-role demo header."""
    # 1. Check explicit header first (helpful for fast UI role switching)
    if x_user_role and x_user_role.lower() in DEFAULT_USERS:
        return DEFAULT_USERS[x_user_role.lower()]

    # 2. Check Authorization Bearer header
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1].strip().lower()
        if token in DEFAULT_USERS:
            return DEFAULT_USERS[token]

    # Default fallback for unauthenticated callers is VIEWER
    return DEFAULT_USERS["viewer"]


def require_roles(allowed_roles: list[UserRole]):
    """FastAPI dependency for RBAC role enforcement."""

    async def _role_checker(user: Annotated[User, Depends(get_current_user)]) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: role '{user.role.value}' is not authorized for this action. Allowed: {[r.value for r in allowed_roles]}.",
            )
        return user

    return _role_checker


@router.post("/login", response_model=AuthResponse, summary="User login")
async def login(req: LoginRequest) -> AuthResponse:
    """Authenticate and return user session."""
    username = req.username.lower().strip()
    if username in DEFAULT_USERS:
        user = DEFAULT_USERS[username]
        store.add_audit(
            user=user,
            action="USER_LOGIN_SUCCESS",
            resource_type="auth",
            resource_id=user.user_id,
            details=f"User {user.name} logged in with role {user.role.value}.",
        )
        return AuthResponse(access_token=username, user=user)

    # Allow fallback demo login for standard roles
    for role_key, user in DEFAULT_USERS.items():
        if role_key in username:
            return AuthResponse(access_token=role_key, user=user)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials. Try 'admin', 'engineer', 'police', or 'viewer'.",
    )


@router.get("/me", response_model=User, summary="Get current user profile")
async def get_me(user: Annotated[User, Depends(get_current_user)]) -> User:
    """Return profile of current active session."""
    return user
