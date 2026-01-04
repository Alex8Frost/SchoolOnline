from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return await auth_service.register_user(user_data)


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return await auth_service.login_user(user_data)


@router.get("/google")
async def google_auth():
    return {
        "message": "Google OAuth endpoint - to be implemented",
        "redirect": "Google OAuth URL will be here"
    }


@router.get("/google/callback")
async def google_callback():
    return {
        "message": "Google OAuth callback - to be implemented"
    }
