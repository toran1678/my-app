# 모든 모델들을 여기서 import하여 Base.metadata.create_all()이 모든 테이블을 생성할 수 있도록 함
from app.db.database import Base
from app.models.user import User

__all__ = ["Base", "User"]
