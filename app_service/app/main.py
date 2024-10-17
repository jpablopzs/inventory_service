import os
from sqlalchemy.orm import Session
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from app_service.app.core.database import initiate_database, close_database
#from app.auth.routes import (auth)

env = os.getenv("ENV", "development")

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    await initiate_database()
    yield
    await close_database()

# Crear un limitador
limiter = Limiter(key_func=get_remote_address)

if env == "production":
    app = FastAPI(docs_url=None, redoc_url=None)
else:
    app = FastAPI(lifespan=app_lifespan)

origins = [
    os.environ.get('CSRF_FRONT')
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Agregar middleware para manejar rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda request, exc: JSONResponse(
    {"message": "Too many requests"}, status_code=429))
app.add_middleware(SlowAPIMiddleware)
