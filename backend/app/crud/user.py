from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext
import bcrypt
from typing import Optional, List

# 비밀번호 해싱 설정 - bcrypt 문제 해결을 위한 설정
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto"
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """비밀번호 검증 - bcrypt 직접 사용"""
    # bcrypt는 72바이트로 제한되므로 UTF-8 인코딩 후 길이 확인
    password_bytes = plain_password.encode('utf-8')
    
    # 72바이트 제한 적용
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # bcrypt로 직접 검증
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def get_password_hash(password: str) -> str:
    """비밀번호 해싱 - bcrypt 직접 사용"""
    # bcrypt는 72바이트로 제한되므로 UTF-8 인코딩 후 길이 확인
    password_bytes = password.encode('utf-8')
    
    # 72바이트 제한 적용
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # bcrypt로 직접 해싱
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # bytes를 문자열로 변환
    return hashed.decode('utf-8')

def get_user(db: Session, user_id: int) -> Optional[User]:
    """ID로 사용자 조회"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """이메일로 사용자 조회"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """사용자명으로 사용자 조회"""
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """사용자 목록 조회"""
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> User:
    """사용자 생성"""
    # 이메일, 사용자명 중복 확인
    existing_user = db.query(User).filter(
        or_(User.email == user.email, User.username == user.username)
    ).first()
    
    if existing_user:
        if existing_user.email == user.email:
            raise ValueError("Email already registered")
        if existing_user.username == user.username:
            raise ValueError("Username already taken")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """사용자 정보 업데이트"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    """사용자 삭제"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """사용자 인증"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
