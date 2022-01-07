from datetime import datetime

from sqlalchemy.orm import Session

from db.models import DBComment
from routers.schemas import CommentBase


def create(db: Session, request: CommentBase):
    new_comment = DBComment(
        comment=request.comment,
        username=request.username,
        post_id=request.post_id,
        timestamp=datetime.now()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def get_all(db: Session, post_id: int):
    return db.query(DBComment).filter(DBComment.post_id == post_id).all()
