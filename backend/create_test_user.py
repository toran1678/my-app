# 사용자 생성 테스트 스크립트
import sys
sys.path.append('.')

from dotenv import load_dotenv
load_dotenv()

from app.db.database import SessionLocal
from app.crud.user import create_user
from app.schemas.user import UserCreate

# 데이터베이스 세션 생성
db = SessionLocal()

try:
    # 테스트 사용자 생성
    user_data = UserCreate(
        email='test@example.com',
        username='testuser',
        full_name='Test User',
        password='password123'
    )
    
    user = create_user(db, user_data)
    print(f'✅ 사용자 생성 성공: {user.email}')
    
except Exception as e:
    print(f'❌ 사용자 생성 실패: {e}')
    import traceback
    traceback.print_exc()
finally:
    db.close()
