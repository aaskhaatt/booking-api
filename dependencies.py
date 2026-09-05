from security import create_access_token, decode_access_token
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from repositories.user_repository import get_user_by_id


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")
    
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    
    user = get_user_by_id(int(user_id), db)

    return user