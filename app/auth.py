from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
import app.models as models
import app.schemas as schemas
from app.utils import hash_password, verify_password, create_access_token, decode_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Request
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/auth/login')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/register', response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail='Email already registered')
    user_obj = models.User(email=user.email, password_hash=hash_password(user.password), role=user.role)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

@router.post('/login', response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_access_token({'id': user.id, 'email': user.email, 'role': user.role})
    return {'access_token': token}
