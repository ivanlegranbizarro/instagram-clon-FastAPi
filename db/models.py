from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class DBUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(128))
    posts = relationship('DBPost', backref='user')


class DBPost(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(256))
    image_url_type = Column(String(32))
    caption = Column(String(256))
    timestamp = Column(DateTime)
    creator_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('DBUser', back_populates='posts')
    comments = relationship('DBComment', back_populates='post')


class DBComment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String(256))
    creator_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    user = relationship('DBUser', back_populates='comments')
    post = relationship('DBPost', back_populates='comments')
    timestamp = Column(DateTime)
