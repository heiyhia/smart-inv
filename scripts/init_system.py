import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from app.database.models import Base
from app.database.session import engine, SessionLocal
from app.services.user import create_user, get_user_by_username
from app.config import ADMIN_USERNAME, ADMIN_PASSWORD, ADMIN_EMAIL

def init_database():
    """初始化数据库表"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def create_admin_user():
    """创建管理员用户"""
    db = SessionLocal()
    try:
        # 检查管理员是否已存在
        admin = get_user_by_username(db, ADMIN_USERNAME)
        if admin:
            print(f"Admin user '{ADMIN_USERNAME}' already exists!")
            return

        # 创建管理员用户
        admin = create_user(
            db=db,
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            password=ADMIN_PASSWORD,
            is_admin=True
        )
        print(f"Admin user '{ADMIN_USERNAME}' created successfully!")
    finally:
        db.close()

def main():
    """主函数"""
    print("Initializing system...")
    
    # 初始化数据库
    init_database()
    
    # 创建管理员用户
    create_admin_user()
    
    print("System initialization completed!")

if __name__ == "__main__":
    main() 