from sqlalchemy import (Column, String, Integer, DateTime, ForeignKey)
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    phone_number = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    country = Column(String, nullable=False)
    birthday = Column(String, nullable=False)
    reg_date = Column(DateTime, default=datetime.now())
    message_fk = relationship("Message", back_populates="user_fk", cascade="all, delete-orphan")
    post_fk = relationship("Post", back_populates="user_fk", cascade="all, delete-orphan")
    comment_fk = relationship("Comment", back_populates="user_fk", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, default="Аноним")
    user_id = Column(Integer, ForeignKey("users.id"))
    main_text = Column(String)
    date_mes = Column(DateTime, default=datetime.now())
    user_fk = relationship(User, back_populates="message_fk", lazy="select", cascade="all, delete", passive_deletes=True)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    main_text = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_date = Column(DateTime, default=datetime.now())
    user_fk = relationship(User, back_populates="post_fk", lazy="select", cascade="all, delete", passive_deletes=True)
    comment = relationship("Comment", back_populates="post_fk", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    main_text = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_fk = relationship(User, back_populates="comment_fk", lazy="select", cascade="all, delete", passive_deletes=True)
    post_fk = relationship(Post, back_populates="comment", lazy="select", single_parent=True)  # Убираем cascade здесь
