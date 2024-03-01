from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse, Response
from app.db.database import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from app.crud.url_crud import create_url, get_url_by_short_url, get_url_analytics, get_link_history
from app.utils.qr_code_generator import save_qr_code
from app.schemas import CreateURLRequest
from app.utils.jwt import decode_jwt_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create_url/")
async def create_url_endpoint(request: CreateURLRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_info = decode_jwt_token(token)
    url_db = create_url(db, request.original_url, request.custom_alias)
    
    save_qr_code(url_db.short_url)

    url_data = {
        "id": url_db.id,
        "original_url": url_db.original_url,
        "short_url": url_db.short_url,
        "custom_alias": url_db.custom_alias,
        "click_count": url_db.click_count,
    }
    response_data = {"url_data": url_data, "shortened_url": f"https://my-domain/{url_db.short_url}"}
    return JSONResponse(content=response_data)

@router.get("/get_url/{short_url}")
async def get_url_endpoint(short_url: str, db: Session = Depends(get_db)):
    url = get_url_by_short_url(db, short_url)
    if url:
        return url
    else:
        raise HTTPException(status_code=404, detail="URL not found")

@router.get("/get_url_analytics/{short_url}")
async def get_url_analytics_endpoint(short_url: str, db: Session = Depends(get_db)):
    analytics_data = get_url_analytics(db, short_url)
    if analytics_data:
        return analytics_data
    else:
        raise HTTPException(status_code=404, detail="URL not found")

@router.get("/get_link_history")
async def get_link_history_endpoint(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    user_info = decode_jwt_token(token)
    
    link_history = get_link_history(db, user_info['sub'])
    return link_history

@router.get("/get_qr_code/{short_url}")
async def get_qr_code_endpoint(short_url: str):
    qr_code_path = save_qr_code(short_url)
    return FileResponse(qr_code_path, media_type="image/png")

@router.get("/{short_url}", response_class=RedirectResponse)
async def redirect_to_original_url(short_url: str, db: Session = Depends(get_db)):
    url = get_url_by_short_url(db, short_url)
    if url:
        return RedirectResponse(url.original_url, status_code=307)
    else:
        raise HTTPException(status_code=404, detail="URL not found")