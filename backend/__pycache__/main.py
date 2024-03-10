from fastapi import FastAPI, Depends, HTTPException
from app.routes import url_shortener, user
from app.db.database import SessionLocal
from app.db.database import get_db
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=300)

app = FastAPI(debug=True)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(url_shortener.router, prefix="")
app.include_router(user.router, prefix="/user")

@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"message": "Hello World! Welcome to my scissors app"}

@app.get("/cached_endpoint")
def cached_endpoint():
    cache_key = "some_unique_key"

    cached_result = cache.get(cache_key)
    if cached_result:
        return {"message": "Result from cache", "data": cached_result}

    result = another_operation()

    cache[cache_key] = result

    return {"message": "Result not in cache", "data": result}

def another_operation():
    return {"result": "Some data"}

