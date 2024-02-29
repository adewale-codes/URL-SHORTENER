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