import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Form, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from app.utils.jwt import create_jwt_token
from app.db.database import get_db
from app.crud.user_crud import create_user, authenticate_user, get_user_by_reset_token, set_reset_token, reset_password, get_user_by_identifier
from app.schemas import CreateUserRequest
import logging

load_dotenv()

router = APIRouter()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_SENDER = os.getenv("SMTP_SENDER", "your_email@gmail.com")

def send_reset_email(to_email, reset_token):
    subject = "Password Reset"
    body = f"Click the following link to reset your password: http://example.com/reset-password?token={reset_token}\n\nToken: {reset_token}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_SENDER
    msg["To"] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_SENDER, to_email, msg.as_string())
        print(f"Password reset email sent to: {to_email}")
    except Exception as e:
        print(f"Failed to send password reset email to {to_email}. Error: {str(e)}")

@router.post("/register/")
async def register_user(user: CreateUserRequest, db: Session = Depends(get_db)):
    user_db = create_user(user.username, user.password, user.email, db)
    token = create_jwt_token({"sub": user_db.username, "email": user_db.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
async def login_user(data: dict, db: Session = Depends(get_db)):
    identifier = data.get("identifier")
    password = data.get("password")
    try:
        token = authenticate_user(identifier, password, db)
        return {"access_token": token, "token_type": "bearer"}
    except HTTPException as e:
        return JSONResponse(content={"detail": str(e)}, status_code=e.status_code)

@router.post("/forgot-password")
async def forgot_password(username_or_email: str, db: Session = Depends(get_db)):
    user = get_user_by_identifier(username_or_email, db)
    if user:
        reset_token = set_reset_token(user, db)
        send_reset_email(user.email, reset_token)
        return {"message": "Password reset link sent to your email"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.post("/reset-password")
async def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    user = get_user_by_reset_token(token, db)
    if user:
        reset_password(user, new_password, db)
        new_token = create_jwt_token({"sub": user.username})
        return {"message": "Password reset successful", "new_access_token": new_token}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
