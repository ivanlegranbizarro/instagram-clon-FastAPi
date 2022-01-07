import random
import shutil
import string
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session

from auth.oauth2 import get_current_user
from routers.schemas import PostBase, PostDisplay, UserAuth
from db.database import get_db
from db import db_post
from typing import List

router = APIRouter(
    prefix="/post",
    tags=["post"]
)

image_url_types = ['absolute', 'relative']


@router.post('', response_model=PostDisplay)
def create(request: PostBase, db: Session = Depends(get_db),
           current_user: UserAuth = Depends(get_current_user)):
    if request.image_url_type in image_url_types:
        return db_post.create(db, request)
    raise HTTPException(status_code=422, detail="Invalid image_url_type")


@router.get('/all', response_model=List[PostDisplay])
def all_posts(db: Session = Depends(get_db)):
    return db_post.get_all(db)


@router.post('/image')
def upload_image(image: UploadFile = File(...), current_user: UserAuth = Depends(get_current_user)):
    letters = string.ascii_letters
    random_name = ''.join(random.choice(letters) for _ in range(6))
    new_name = f'_{random_name}.'
    filename = new_name.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'

    with open(path, 'wb') as f:
        shutil.copyfileobj(image.file, f)

    return {'filename': path}


@router.delete('/delete/{id}')
def delete(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_post.delete(db, id, current_user.id)
