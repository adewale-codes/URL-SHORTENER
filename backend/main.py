from fastapi import FastAPI, Depends, HTTPException
from app.routes import url_shortener, user
from app.db.database import SessionLocal, get_db
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from cachetools import TTLCache
import logging
from time import sleep

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    try:
        cache_key = "some_unique_key"

        logger.info(f"Checking cache for key: {cache_key}")

        cached_result = cache.get(cache_key)
        if cached_result:
            return {"message": "Result from cache", "data": cached_result}

        result = expensive_operation()

        logger.info(f"Expensive operation result: {result}")

        cache[cache_key] = result

        return {"message": "Result not in cache", "data": result}
    except Exception as e:
        logger.error(f"Error in cached_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def expensive_operation():
    sleep(5)

    return {"result": "Some data"}
