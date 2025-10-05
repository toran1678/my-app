from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Optional
import os

from app.db.database import get_db
from app.crud.user import authenticate_user, get_user_by_email
from app.schemas.user import Token, TokenData, UserResponse
from app.models.user import User

router = APIRouter()

# OAuth2 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")

# JWT 설정
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    JWT 액세스 토큰 생성
    
    Args:
        data: 토큰에 포함할 데이터 (예: {"sub": "user@example.com"})
        expires_delta: 토큰 만료 시간 (None이면 기본 15분)
        
    Returns:
        str: 인코딩된 JWT 토큰
    """
    to_encode = data.copy()
    
    # 토큰 만료 시간 설정
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    # 만료 시간을 페이로드에 추가
    to_encode.update({"exp": expire})
    
    # JWT 토큰 인코딩 및 반환
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    현재 사용자 가져오기
    
    Args:
        token: Authorization 헤더에서 추출된 JWT 토큰
        db: 데이터베이스 세션
        
    Returns:
        User: 인증된 사용자 객체
        
    Raises:
        HTTPException: 토큰이 유효하지 않거나 사용자를 찾을 수 없는 경우
    """
    # 인증 실패 시 반환할 예외 객체
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # JWT 토큰을 디코딩하여 페이로드 추출
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # 토큰에서 사용자 이메일 추출
        
        # 토큰에 이메일이 없으면 인증 실패
        if email is None:
            raise credentials_exception
            
        token_data = TokenData(email=email)
        
    except JWTError:
        # JWT 디코딩 실패 시 인증 실패
        raise credentials_exception
    
    # 데이터베이스에서 사용자 조회
    user = get_user_by_email(db, email=token_data.email)
    
    # 사용자가 존재하지 않으면 인증 실패
    if user is None:
        raise credentials_exception
        
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    현재 활성 사용자 가져오기
    
    Args:
        current_user: get_current_user에서 반환된 사용자 객체
        
    Returns:
        User: 활성 상태인 사용자 객체
        
    Raises:
        HTTPException: 사용자가 비활성 상태인 경우
    """
    # 사용자가 비활성 상태인지 확인
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return current_user

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """로그인 및 JWT 토큰 발급"""
    # 사용자 인증
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 토큰 만료 시간 설정
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # JWT 토큰 생성 (사용자 이메일을 sub로 포함)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # 토큰과 타입 반환
    return {"access_token": access_token, "token_type": "bearer"}

# 추가: JSON 형태의 로그인 엔드포인트 (디버깅용)
from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login", response_model=Token)
async def login_with_json(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """JSON 형태의 로그인 엔드포인트"""
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# 테스트용 사용자 생성
@router.post("/create-test-user")
async def create_test_user(db: Session = Depends(get_db)):
    from app.crud.user import create_user
    from app.schemas.user import UserCreate
    
    user_data = UserCreate(
        email='test@example.com',
        username='testuser',
        full_name='Test User',
        password='password123'
    )
    
    user = create_user(db, user_data)
    return {"message": f"테스트 사용자 생성 성공: {user.email}", "user_id": user.id}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """현재 사용자 정보 조회"""
    return current_user
