import logging
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.security import get_password_hash, verify_password
from app.utils.jwt import create_jwt_token
from fastapi import HTTPException, status
from sqlalchemy import or_
import secrets
from datetime import datetime, timedelta

def get_user_by_username(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()

def create_user(username: str, password: str, email: str, db: Session):
    existing_user = get_user_by_username(username, db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    hashed_password = get_password_hash(password)
    user = User(username=username, hashed_password=hashed_password, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(identifier: str, password: str, db: Session):
    logging.debug(f"Attempting to authenticate user with identifier: {identifier}")
    
    user = get_user_by_identifier(identifier, db)
    if user and verify_password(password, user.hashed_password):
        logging.info(f"User {identifier} authenticated successfully")
        return {"access_token": create_jwt_token({"sub": user.username})}
    
    logging.warning(f"Authentication failed for user {identifier}")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

def get_user_by_identifier(identifier: str, db: Session):
    return db.query(User).filter(or_(User.username == identifier, User.email == identifier)).first()

def generate_reset_token():
    return secrets.token_urlsafe()

def set_reset_token(user: User, db: Session):
    user.reset_token = generate_reset_token()
    user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
    db.commit()
    return user.reset_token

def get_user_by_reset_token(token: str, db: Session):
    return db.query(User).filter(User.reset_token == token).first()

def reset_password(user: User, new_password: str, db: Session):
    user.hashed_password = get_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expires = None
    db.commit()