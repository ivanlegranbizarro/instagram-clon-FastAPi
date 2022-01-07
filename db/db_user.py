from fastapi import HTTPException

from db.models import DBUser
from routers.schemas import UserBase
from sqlalchemy.orm.session import Session
from db.hashing import Hash


def create_user(db: Session, request: UserBase):
    new_user = DBUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_username(db: Session, username: str):
    user = db.query(DBUser).filter(DBUser.username == username).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")
