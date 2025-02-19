from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm
from app.core.oauth import oauth
from app.core.deps import get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.crud import user as user_crud
from app.schemas.token import Token
from app.models.user import User
from app.schemas.user import UserCreate

# Налаштування JWT
SECRET_KEY = "your-secret-key"  # В продакшені використовуйте безпечний ключ
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

FACEBOOK_CLIENT_ID = "1430506701265979"
FACEBOOK_CLIENT_SECRET = "8fb9479aa5ca2d8dd83421e26eec7a4c"

def create_access_token(user_id: int):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    data = {"sub": str(user_id), "exp": expire}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

router = APIRouter()

@router.get("/login/{provider}")
async def login(provider: str, request: Request):
    if provider not in ["facebook", "twitter"]:
        raise HTTPException(status_code=400, detail="Unsupported provider")
    
    client = oauth.create_client(provider)
    redirect_uri = request.url_for(f'auth_{provider}')
    return await client.authorize_redirect(request, redirect_uri)

@router.get("/auth/facebook")
async def auth_facebook(request: Request, db: Session = Depends(get_db)):
    client = oauth.create_client('facebook')
    token = await client.authorize_access_token(request)
    
    # Отримуємо дані користувача
    resp = await client.get('me', token=token)
    profile = resp.json()
    
    # Зберігаємо користувача в БД
    user = user_crud.get_or_create_user(
        db,
        email=profile.get('email'),
        social_accounts={'facebook': token},
        profile_data=profile
    )
    
    return {"access_token": create_access_token(user.id)}

@router.get("/auth/twitter")
async def auth_twitter(request: Request, db: Session = Depends(get_db)):
    client = oauth.create_client('twitter')
    token = await client.authorize_access_token(request)
    
    # Отримуємо дані користувача
    resp = await client.get('account/verify_credentials.json', token=token)
    profile = resp.json()
    
    # Зберігаємо користувача в БД
    user = user_crud.get_or_create_user(
        db,
        email=profile.get('email'),
        social_accounts={'twitter': token},
        profile_data=profile
    )
    
    return {"access_token": create_access_token(user.id)}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    OAuth2 compatible token login.
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signup", response_model=Token)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Create new user.
    """
    # Check if user exists
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    db_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        interests=user_in.interests
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create access token
    access_token = create_access_token(subject=db_user.id)
    return {"access_token": access_token, "token_type": "bearer"} 