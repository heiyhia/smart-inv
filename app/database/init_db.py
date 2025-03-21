from sqlalchemy.orm import Session
from app.config import ADMIN_USERNAME, ADMIN_PASSWORD, ADMIN_EMAIL
from app.services.user import create_user, get_user_by_username
from app.database.models import Base
from app.database.session import engine

def init_db(db: Session) -> None:
    """初始化数据库"""
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    # 创建管理员账户（如果不存在）
    admin = get_user_by_username(db, ADMIN_USERNAME)
    if not admin:
        create_user(
            db=db,
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            password=ADMIN_PASSWORD,
            is_admin=True
        ) 