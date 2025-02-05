from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from app.core.oauth import oauth
from app.core.deps import get_db
from app.crud import user as user_crud

# Налаштування JWT
SECRET_KEY = "your-secret-key"  # В продакшені використовуйте безпечний ключ
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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