from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import UserCreate, UserResponse, UserLogin, TokenResponse
from database import get_db
from security import create_access_token
from services.user_service import register_user_service, authenticate_user_service


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return register_user_service(user, db)


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    current_user = authenticate_user_service(user.email, user.password, db)
    token = create_access_token(current_user.id)
    return {
        "access_token": token,
        "token_type": "bearer"
    }