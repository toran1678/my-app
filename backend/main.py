import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pathlib import Path

from app.api.routes import auth, users
from app.models import Base
from app.db.database import engine

# 환경변수 로드
load_dotenv()

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="My App API",
    description="My App Backend API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
origins = [
    "http://localhost:3000",  # React Native Web
    "http://localhost:8081",  # Metro bundler
    "http://localhost:19006", # Expo web
    "http://localhost:19000", # Expo dev tools
    "http://10.0.2.2:3000",   # Android 에뮬레이터 - React Native Web
    "http://10.0.2.2:8081",   # Android 에뮬레이터 - Metro bundler
    "http://10.0.2.2:19006",  # Android 에뮬레이터 - Expo web
    "http://10.0.2.2:19000",  # Android 에뮬레이터 - Expo dev tools
    "exp://192.168.1.100:8081",  # Expo 실제 기기용 (IP는 환경에 맞게 조정)
]

# 환경변수에서 추가 허용 도메인 가져오기
if os.getenv("FRONTEND_URL"):
    origins.append(os.getenv("FRONTEND_URL"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 업로드 폴더를 정적 파일로 서빙
uploads_path = Path("uploads")
uploads_path.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 라우터 등록
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "My App API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        # reload=True if os.getenv("ENVIRONMENT") == "development" else False
    )