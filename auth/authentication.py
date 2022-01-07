from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth.oauth2 import create_access_token
from db.database import get_db
from db.models import DBUser

from db.hashing import Hash

router = APIRouter(
    tags=["Authentication"]
)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.username == request.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"username": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        'user_id': user.id,
        'username': user.username
    }
