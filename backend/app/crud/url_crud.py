from sqlalchemy.orm import Session
from app.models.url import URL
import shortuuid
from fastapi import HTTPException
from app.utils.qr_code_generator import save_qr_code

def create_url(db: Session, original_url: str, custom_alias: str = None):
    short_url = shortuuid.uuid()[:8]

    if custom_alias:
        existing_url = db.query(URL).filter(URL.custom_alias == custom_alias).first()
        if existing_url:
            raise HTTPException(status_code=400, detail="Custom alias already exists")

    url_db = URL(original_url=original_url, short_url=short_url, custom_alias=custom_alias)
    
    db.add(url_db)
    db.commit()
    db.refresh(url_db)

    qr_code_path = save_qr_code(short_url)
    url_db.qr_code_path = qr_code_path

    db.commit()

    return url_db

def get_url_by_short_url(db: Session, short_url: str):
    return db.query(URL).filter(URL.short_url == short_url).first()

def get_url_analytics(db: Session, short_url: str):
    url = get_url_by_short_url(db, short_url)
    if url:
        url.click_count += 1
        db.commit()

        analytics_data = {"clicks": url.click_count, "location": "Sample Location"}
        return analytics_data
    return None

def get_link_history(db: Session, user_id: int):
    return (
        db.query(URL)
        .filter(URL.user_id == user_id)
        .all()
    )